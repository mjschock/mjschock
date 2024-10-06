"""LangGraph SWE Agent"""

import operator
from typing import List, TypedDict
from typing_extensions import Annotated

import dotenv
from composio_openai import ComposioToolSet, WorkspaceType
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, StateGraph
from openai import OpenAI
from openai.types.chat import ChatCompletion
from openai.types.chat import ChatCompletionToolParam
from openai.types.shared_params import FunctionDefinition
from openai.types.chat.chat_completion_tool_message_param import ChatCompletionToolMessageParam
from openai.types.chat.chat_completion_system_message_param import ChatCompletionSystemMessageParam
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam

from custom_tools import get_weather

# Load environment variables from .env
dotenv.load_dotenv()

# composio_toolset = ComposioToolSet(workspace_config=WorkspaceType.Docker())
composio_toolset = ComposioToolSet(workspace_config=WorkspaceType.Host())

# Get required tools
tools = [
    # *composio_toolset.get_tools(
    #     actions=[
    #         Action.GITHUB_CREATE_A_PULL_REQUEST,
    #         Action.TWITTER_USER_LOOKUP_ME,
    #         Action.WEBTOOL_SCRAPE_WEBSITE_CONTENT,
    #     ],
    #     apps=[
    #         App.FILETOOL,
    #         App.SHELLTOOL,
    #     ]
    # ),
    *composio_toolset.get_actions(
        actions=[
            get_weather,
            # say,  # This is just here as an example of a custom tool, you can remove it
            # Action.GITHUB_CREATE_A_PULL_REQUEST
        ]
    ),
]

tools: List[ChatCompletionToolParam] = [
    ChatCompletionToolParam(
        function=FunctionDefinition(
            name=tool.get("function").get("name"),
            description=tool.get("function").get("description"),
            parameters=tool.get("function").get("parameters"),
            # strict=False,
        ),
        type=tool.get("type", "function"),
    ) for tool in tools
]

class AgentState(TypedDict):
    messages: Annotated[list[ChatCompletionMessageParam], operator.add]


class Agent:
    def __init__(self, model, tools, checkpointer, system_prompt=""):
        graph = StateGraph(AgentState)

        graph.add_node("llm", self.step)
        graph.add_node("action", self.take_action)
        graph.add_conditional_edges(
            "llm",
            self.exists_action,
            {True: "action", False: END}
        )
        graph.add_edge("action", "llm")
        graph.set_entry_point("llm")

        # self.graph = graph.compile(checkpointer=checkpointer)
        self.graph = graph.compile()
        self.model = model
        self.tools = tools
        self.system_prompt = system_prompt

    def exists_action(self, state: AgentState):
        result = state['messages'][-1]

        if result.tool_calls:
            return True

        return False

    def step(self, state: AgentState):
        messages = state['messages']

        if self.system_prompt:
            messages = [
                ChatCompletionSystemMessageParam(
                    content=self.system_prompt, 
                    role="system"),
            ] + messages

        client = OpenAI(
            api_key='ollama',
            base_url = 'http://localhost:11434/v1',
        )

        response = client.chat.completions.create(
            messages=messages,
            model="llama3.2:1b",
            temperature=0,
            tools=tools,
        )

        message = response.choices[0].message

        return {
            'messages': [message],
        }

    def take_action(self, state: AgentState):
        latest_message = state['messages'][-1]
        latest_message_tool_calls = latest_message.tool_calls

        results = []

        for tool_call in latest_message_tool_calls:
            results.append(
                composio_toolset.execute_tool_call(
                    tool_call=tool_call,
                    entity_id=composio_toolset.entity_id,
                )
            )

        chat_completion_tool_messages = [
            ChatCompletionToolMessageParam(
                content=str(result),
                role="tool", # TODO: different role?
                tool_call_id=tool_call.id,
            ) for tool_call, result in zip(latest_message_tool_calls, results)
        ]

        return {'messages': chat_completion_tool_messages}

memory = SqliteSaver.from_conn_string(":memory:")
# memory = AsyncSqliteSaver.from_conn_string(":memory:")

model = "llama3.2:1b"

# https://github.com/meta-llama/llama-models/blob/main/models/llama3_2/text_prompt_format.md#zero-shot-function-calling-e2e-format
prompt = f"""You are an expert in composing functions. You are given a question and a set of possible functions.
Based on the question, you will need to make one or more function/tool calls to achieve the purpose.
If none of the function can be used, point it out. If the given question lacks the parameters required by the function,
also point it out. You should only return the function call in tools call sections.

If you decide to invoke any of the function(s), you MUST put it in the format of [func_name1(params_name1=params_value1, params_name2=params_value2...), func_name2(params)]
You SHOULD NOT include any other text in the response.

Here is a list of functions in JSON format that you can invoke:\n\n"""

prompt += '[\n'

for i, tool in enumerate(tools):
    prompt += '    {\n'

    prompt += f'        "name": "{tool.get("function").get("name")}",\n'
    prompt += f'        "description": "{tool.get("function").get("description")}",\n'

    prompt += '        "parameters": {\n'

    prompt += '            "type": "dict",\n' # TODO: object from field?
    prompt += '            "required": [\n'

    for j, parameter in enumerate(tool.get("function").get("parameters").get("required", [])):
        prompt += f'                "{parameter}"'

        if j < len(tool.get("function").get("parameters").get("required")) - 1:
            prompt += ','

        prompt += '\n'

    prompt += '            ],\n'

    prompt += '            "properties": {\n'

    for j, parameter in enumerate(tool.get("function").get("parameters").get("properties", [])):
        prompt += f'                "{parameter}": ' + '{\n'

        prompt += f'                    "type": "{tool.get("function").get("parameters").get("properties").get(parameter).get("type")}",\n'
        prompt += f'                    "description": "{tool.get("function").get("parameters").get("properties").get(parameter).get("description")}"'

        if "default" in tool.get("function").get("parameters").get("properties").get(parameter):
            prompt += ',\n'
            prompt += f'                    "default": "{tool.get("function").get("parameters").get("properties").get(parameter).get("default")}"\n'

        else:
            prompt += '\n'

        prompt += '                }'

        if j < len(tool.get("function").get("parameters").get("properties")) - 1:
            prompt += ','

        prompt += '\n'

    prompt += '            }\n'

    prompt += '        },\n'

    prompt += '    }'

    if i < len(tools) - 1:
        prompt += ','

    prompt += '\n'

prompt += ']\n'

abot = Agent(
    model,
    tools,
    checkpointer=memory,
    system_prompt=prompt,
)
