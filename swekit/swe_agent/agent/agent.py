# """CrewAI SWE Agent"""
"""LangGraph SWE Agent"""

from datetime import datetime, timezone
import operator
import os
from typing import Dict, List, Literal, TypedDict, cast
from typing_extensions import Annotated

import dotenv
# from composio_crewai import Action, App, ComposioToolSet, WorkspaceType
# from composio_langchain.toolset import StructuredTool
# from composio_langgraph import Action, App, ComposioToolSet, WorkspaceType
from composio_openai import Action, App, ComposioToolSet, WorkspaceType
# from crewai import Agent, Crew, LLM, Process, Task
from llama_stack_client import LlamaStackClient
from llama_stack_client.types import UserMessage
from langchain_core.messages import AnyMessage, AIMessage, BaseMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.messages.base import messages_to_dict
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompt_values import ChatPromptValue
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langgraph.graph import END, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode
import openai
from openai.types.chat import ChatCompletionToolParam
from openai.types.shared_params import FunctionDefinition
from openai.types.shared_params.function_parameters import FunctionParameters
from openai.types.chat.chat_completion_tool_message_param import ChatCompletionToolMessageParam
from openai.types.chat.chat_completion_user_message_param import ChatCompletionUserMessageParam
from openai.types.chat.chat_completion_system_message_param import ChatCompletionSystemMessageParam
from openai.types.chat.chat_completion_function_message_param import ChatCompletionFunctionMessageParam
from openai.types.chat.chat_completion_assistant_message_param import ChatCompletionAssistantMessageParam
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam

from configuration import Configuration
from custom_tools import get_weather, say
from graph import route_model_output
from prompts import BACKSTORY, DESCRIPTION, EXPECTED_OUTPUT, GOAL, ROLE, SYSTEM_PROMPT
from state import InputState, State
from tools import TOOLS
from utils import load_chat_model

# Load environment variables from .env
dotenv.load_dotenv()


openai.base_url = "http://localhost:11434/v1"
openai.api_key = 'ollama'

# provider = "anthropic"
# provider = "github"
# provider = "ollama"
# # provider = "openai"

# embedder = {
#     "provider": "gpt4all",
#     "config": {
#         # "model": "all-MiniLM-L6-v2-f16.gguf",
#         "model": "all-MiniLM-L6-v2.gguf2.f16.gguf",
#     }
# }

# if provider == "anthropic":
#     # llm = LLM(
#     #     api_key=os.environ["ANTHROPIC_API_KEY"],
#     #     model="claude-3-sonnet-20240229",
#     # )
#     raise NotImplementedError("Anthropic is not yet supported")

# elif provider == "ollama":
#     # llm = LLM(
#     #     base_url="http://localhost:11434",
#     #     model="ollama/llama3.2:1b",
#     # )
#     # openai_client = openai.Client(
#     #     api_key="ollama",
#     #     base_url="http://localhost:11434/v1",
#     # )
#     # model = "llama3.2:1b"
#     # model = ChatOpenAI(
#     #     api_key="ollama",
#     #     base_url="http://localhost:11434/v1",
#     #     model="llama3.2:1b",
#     #     temperature=0,
#     # )
#     model = ChatOllama(
#         model="llama3.2:1b",
#         temperature=0,
#     )

# elif provider == "openai":
#     embedder = {
#         "provider": "openai",
#         "config": {
#             "model": 'text-embedding-3-small'
#         }
#     }
#     llm = ChatOpenAI(
#         api_key=os.environ["OPENAI_API_KEY"],
#         # model="gpt-4-1106-preview",
#         model="gpt-3.5-turbo",
#     )

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

# print(f"type(tools[0]): ", type(tools[0]))
# print(f"tools[0]: ", tools[0])


tools: List[ChatCompletionToolParam] = [
    ChatCompletionToolParam(
        function=FunctionDefinition(
            name=tool.get("function").get("name"),
            description=tool.get("function").get("description"),
            # parameters=FunctionParameters(
                
            # ),
            parameters=tool.get("function").get("parameters"),
            # strict=False,
        ),
        type=tool.get("type", "function"),
    ) for tool in tools
]

# raise Exception("stop")
# tools = [ChatCompletionToolParam]

class AgentState(TypedDict):
    # messages: Annotated[list[AnyMessage], operator.add]
    messages: Annotated[list[ChatCompletionMessageParam], operator.add]


class Agent:
    def __init__(self, model, tools, system=""):
        self.system = system
        graph = StateGraph(AgentState)
        graph.add_node("llm", self.call_openai)
        graph.add_node("action", self.take_action)
        graph.add_conditional_edges(
            "llm",
            self.exists_action,
            {True: "action", False: END}
        )
        graph.add_edge("action", "llm")
        graph.set_entry_point("llm")
        self.graph = graph.compile()
        # self.tools = {t.name: t for t in tools}
        # self.tools = {t.get("name"): t for t in tools}
        self.tools = tools
        # self.model = model.bind_tools(tools)
        self.model = model

    def exists_action(self, state: AgentState):
        result = state['messages'][-1]
        return len(result.tool_calls) > 0

    def call_openai(self, state: AgentState):
        messages = state['messages']
        if self.system:
            # messages = [SystemMessage(content=self.system)] + messages
            messages = [ChatCompletionSystemMessageParam(content=self.system, role="system")] + messages
        # message = self.model.invoke(messages)

        print('messages', messages)
        print('self.model', self.model)
        print('self.tools', self.tools)

        print('base_url', openai.base_url)
        print('api_key', openai.api_key)

        response = openai.chat.completions.create(
            # api_key="ollama",
            messages=messages,
            model=self.model,
            temperature=0,
            tools=self.tools,
        )

        print('response', response)
        message = response['choices'][0]

        return {'messages': [message]}

    def take_action(self, state: AgentState):
        tool_calls = state['messages'][-1].tool_calls
        results = []
        for t in tool_calls:
            print(f"Calling: {t}")
            if not t['name'] in self.tools:      # check for bad tool name from LLM
                print("\n ....bad tool name....")
                result = "bad tool name, retry"  # instruct LLM to retry if bad
            else:
                result = self.tools[t['name']].invoke(t['args'])
            # results.append(ToolMessage(tool_call_id=t['id'], name=t['name'], content=str(result)))
            results.append(ChatCompletionToolMessageParam(tool_call_id=t['id'], name=t['name'], content=str(result)))
        print("Back to the model!")
        return {'messages': results}

prompt = """You are a smart research assistant. Use the search engine to look up information. \
You are allowed to make multiple calls (either together or in sequence). \
Only look up information when you are sure of what you want. \
If you need to look up some information before asking a follow up question, you are allowed to do that!
"""

# model = ChatOpenAI(model="gpt-3.5-turbo")  #reduce inference cost
# model = ChatOllama(
#     model="llama3.2:1b",
#     temperature=0,
# )
model = "llama3.2:1b"

# abot = Agent(model, [tool], system=prompt)
abot = Agent(model, tools, system=prompt)

# print('tools', tools)

# for tool in tools:
#     print(f"type(tool): {type(tool)}")
#     print('=== tool ===')
#     print(tool)
#     # print('args_schema', tool.args_schema)
#     print('description:', tool.description)
#     print('name:', tool.name)
#     print("parameters:", tool.args)
#     print('')

#     _tool = openai.pydantic_function_tool(tool.args_schema, name=tool.name, description=tool.description)
#     print('=== _tool ===')
#     print(_tool)
#     break

# raise Exception("stop")

# tool_node = ToolNode(tools)
# tools_by_name = {tool.name: tool for tool in tools}
# tools_by_name = {tool.get("name"): tool for tool in tools}

# def tool_node(state: dict):
#     result = []

#     for tool_call in state["messages"][-1].tool_calls:
#         tool = tools_by_name[tool_call["name"]]
#         observation = tool.invoke(tool_call["args"])
#         result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))

#     return {"messages": result}


# async def call_model(
#     state: State, config: RunnableConfig
# ) -> Dict[str, List[AIMessage]]:
#     """Call the LLM powering our "agent".

#     This function prepares the prompt, initializes the model, and processes the response.

#     Args:
#         state (State): The current state of the conversation.
#         config (RunnableConfig): Configuration for the model run.

#     Returns:
#         dict: A dictionary containing the model's response message.
#     """
#     configuration = Configuration.from_runnable_config(config)

#     messages = state["messages"]
#     print(f"messages: {messages}")

#     # Create a prompt template. Customize this to change the agent's behavior.
#     # prompt = ChatPromptTemplate.from_messages(
#     #     [("system", configuration.system_prompt), ("placeholder", "{messages}")]
#     # )

#     # Initialize the model with tool binding. Change the model or add more tools here.
#     # model = load_chat_model(configuration.model).bind_tools(TOOLS)
#     # model = load_chat_model("ollama/llama3.2:1b").bind_tools(TOOLS)
#     # model = load_chat_model("ollama/llama3.2:1b")
#     # model = model.bind_tools(tools)
#     # model = ChatOllama(
#     #     model="llama3.2:1b",
#     #     temperature=0,
#     # ).bind_tools(tools)
#     # model = ChatOpenAI(
#     #     api_key="ollama",
#     #     base_url="http://localhost:11434/v1",
#     #     model="llama3.2:1b",
#     #     temperature=0,
#     # ).bind_tools(tools)

#     # Prepare the input for the model, including the current system time
#     # message_value: List[AnyMessage] = await prompt.ainvoke(
#     # chat_prompt_value: ChatPromptValue = await prompt.ainvoke(
#     #     {
#     #         "messages": state.messages,
#     #         # "system_time": datetime.now(tz=timezone.utc).isoformat(),
#     #         "tools": tools,
#     #     },
#     #     config,
#     # )

#     # # for key, value in message_value.items():
#     # #     print(f"{key}")

#     # # print(f"type(chat_prompt_value): {type(chat_prompt_value)}")

#     # chat_prompt_value_str = chat_prompt_value.to_string()
#     # # print(f"chat_prompt_value_str: {chat_prompt_value_str}")

#     # messages: List[BaseMessage] = chat_prompt_value.to_messages()
#     # # print(f"messages: {messages}")

#     # # for message in messages:
#     # #     print('=== message ===')
#     # #     print(message.pretty_repr(html=False))
#     # #     print(message.pretty_repr(html=True))
#     # #     print('=== message ===')

#     # messages_dict = messages_to_dict(messages)
#     # print(f"messages_dict: {messages_dict}")

#     # raise NotImplementedError("This is not yet supported")

#     # # for message in message_value:
#     # #     print(f"message: {message}")
#     # #     assert isinstance(message, AnyMessage), f"{type(message)} != AnyMessage"

#     # # print(f"message_value: {message_value}")
#     # # print(f"config: {config}")

#     # print('message_value', message_value)

#     # # Get the model's response
#     # response = cast(AIMessage, await model.ainvoke(message_value, config))

#     # # Handle the case when it's the last step and the model still wants to use a tool
#     # if state.is_last_step and response.tool_calls:
#     #     return {
#     #         "messages": [
#     #             AIMessage(
#     #                 id=response.id,
#     #                 content="Sorry, I could not find an answer to your question in the specified number of steps.",
#     #             )
#     #         ]
#     #     }

#     # # Return the model's response as a list to be added to existing messages
#     # return {"messages": [response]}


# # def call_model(state: MessagesState):
# #     # messages = state["messages"]
# #     # response = model_with_tools.invoke(messages)

# #     # print("messages", messages)
# #     # print(f"type(messages): {type(messages)}")
# #     # print(f"len(messages): {len(messages)}")
# #     # print(f"type(messages[-1]): {type(messages[-1])}")

# #     # raise NotImplementedError("This is not yet supported")

# #     # response = openai_client.chat.completions.create(
# #     #     model=model,
# #     #     messages=messages,
# #     #     tools=tools,
# #     # )

# #     configuration = Configuration.from_runnable_config(config)

# #     prompt = ChatPromptTemplate.from_messages( # https://github.com/langchain-ai/react-agent/blob/main/src/react_agent/graph.py#L40
# #         [("system", configuration.system_prompt), ("placeholder", "{messages}")]
# #         # messages
# #     )

# #     print(f"prompt: {prompt}")

# #     model = model.bind_tools(tools) # https://github.com/langchain-ai/react-agent/blob/main/src/react_agent/graph.py#L45C1-L45C67

# #     message_value = await prompt.ainvoke( # https://github.com/langchain-ai/react-agent/blob/main/src/react_agent/graph.py#L47
# #         {
# #             "messages": state.messages,
# #             "system_time": datetime.now(tz=timezone.utc).isoformat(),
# #         },
# #         config,
# #     )

# #     # response = model.invoke(messages)

# #     return {"messages": [response]}


# # def should_continue(state: MessagesState) -> Literal["tools", "__end__"]:
# def should_continue(state: State) -> Literal["tools", "__end__"]:
#     messages = state["messages"]
#     last_message = messages[-1]

#     if last_message.tool_calls:
#         return "tools"

#     return "__end__"

# # workflow = StateGraph(MessagesState)
# workflow = StateGraph(State, input=InputState, config_schema=Configuration)

# workflow.add_node("agent", call_model)
# workflow.add_node("tools", tool_node)

# workflow.add_edge("__start__", "agent")
# # workflow.add_conditional_edges("agent", should_continue)
# workflow.add_conditional_edges("agent", route_model_output)
# workflow.add_edge("tools", "agent")

# app = workflow.compile(
#     interrupt_before=[],  # Add node names here to update state before they're called
#     interrupt_after=[],  # Add node names here to update state after they're called
# )

# # Define agent
# # agent = Agent(
# #     backstory=BACKSTORY,
# #     goal=GOAL,
# #     # function_calling_llm=llm,
# #     llm=llm,
# #     role=ROLE,
# #     tools=tools,
#     verbose=True,
# )

# task = Task(
#     agent=agent,
#     description=DESCRIPTION,
#     expected_output=EXPECTED_OUTPUT,
# )

# crew = Crew(
#     agents=[agent],
#     cache=False,
#     embedder=embedder,
#     # manager_llm=llm,
#     memory=True,
#     process=Process.sequential,
#     tasks=[task],
#     verbose=True,
# )
