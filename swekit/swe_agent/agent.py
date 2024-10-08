"""Composio-LangGraph SWE Agent"""

import operator
from typing import TypedDict
from uuid import uuid4

import dotenv
from langgraph.graph import END, StateGraph
from openai import OpenAI, pydantic_function_tool
from openai.types.chat.chat_completion_assistant_message_param import (
    ChatCompletionAssistantMessageParam,
)
from openai.types.chat.chat_completion_message import ChatCompletionMessage
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from openai.types.chat.chat_completion_message_tool_call import (
    ChatCompletionMessageToolCall,
)
from openai.types.chat.chat_completion_system_message_param import (
    ChatCompletionSystemMessageParam,
)
from openai.types.chat.chat_completion_tool_message_param import (
    ChatCompletionToolMessageParam,
)
from openai.types.chat.chat_completion_user_message_param import (
    ChatCompletionUserMessageParam,
)
from typing_extensions import Annotated

from swe_agent.tools import composio_toolset

# Load environment variables from .env
dotenv.load_dotenv()


class Environment:
    def __init__(self, composio_toolset):
        self.composio_toolset = composio_toolset

    def step(self, actions):
        results = []

        for tool_call in actions:
            try:
                result = composio_toolset.execute_tool_call(
                    tool_call=tool_call,
                    entity_id=composio_toolset.entity_id,
                )

            except Exception as e:
                result = str(e)

            results.append(result)

        observations = results
        rewards = [0] * len(results)
        terminations = [False] * len(results)
        truncations = [False] * len(results)
        infos = [{}] * len(results)

        return observations, rewards, terminations, truncations, infos


env = Environment(composio_toolset)

"""
In previous examples we've annotated the `messages` state key
with the default `operator.add` or `+` reducer, which always
appends new messages to the end of the existing messages array.

Now, to support replacing existing messages, we annotate the
`messages` key with a customer reducer function, which replaces
messages with the same `id`, and appends them otherwise.
"""


# def reduce_messages(left: list[AnyMessage], right: list[AnyMessage]) -> list[AnyMessage]:
def reduce_messages(
    left: list[ChatCompletionMessageParam], right: list[ChatCompletionMessageParam]
) -> list[ChatCompletionMessageParam]:
    # assign ids to messages that don't have them
    for message in right:
        # if not message.id:
        if not message.get("id"):
            # message.id = str(uuid4())
            message["id"] = str(uuid4())

    # merge the new messages with the existing messages
    merged = left.copy()

    for message in right:
        for i, existing in enumerate(merged):
            # replace any existing messages with the same id
            # if existing.id == message.id:
            if existing.get("id") == message.get("id"):
                merged[i] = message
                break

        else:
            # append any new messages to the end
            merged.append(message)

    return merged


class AgentState(TypedDict):
    # messages: Annotated[list[ChatCompletionMessageParam], operator.add]
    messages: Annotated[list[ChatCompletionMessageParam], reduce_messages]


class Agent:
    def __init__(self, model, tools, checkpointer, system_prompt=""):
        graph = StateGraph(AgentState)

        graph.add_node("llm", self.step)
        graph.add_node("action", self.take_action)
        graph.add_conditional_edges(
            "llm", self.exists_action, {True: "action", False: END}
        )
        graph.add_edge("action", "llm")
        graph.set_entry_point("llm")

        self.graph = graph.compile(
            checkpointer=checkpointer,
            interrupt_before=["action"],
        )
        self.model = model
        self.tools = tools
        self.system_prompt = system_prompt

    def exists_action(self, state: AgentState):
        result = state["messages"][-1]

        # if result.tool_calls:
        if result.get("tool_calls"):
            return True

        return False

    def step(self, state: AgentState):
        messages = state["messages"]

        if self.system_prompt:
            messages = [
                ChatCompletionSystemMessageParam(
                    content=self.system_prompt, role="system"
                ),
            ] + messages

        client = OpenAI(
            api_key="ollama",
            base_url="http://localhost:11434/v1",
        )

        response = client.chat.completions.create(
            messages=messages,
            model="llama3.2:1b",
            temperature=0,
            tools=self.tools,
        )

        # message = response.choices[0].message
        message = response.choices[0].message.to_dict()

        return {
            "messages": [message],
        }

    def take_action(self, state: AgentState):
        latest_message = state["messages"][-1]
        # latest_message_tool_calls = latest_message.tool_calls
        latest_message_tool_calls = latest_message.get("tool_calls")

        actions = [
            ChatCompletionMessageToolCall(
                id=tool_call.get("id"),
                function=tool_call.get("function"),
                type=tool_call.get("type"),
            )
            for tool_call in latest_message_tool_calls
        ]

        observations, rewards, terminations, truncations, infos = env.step(
            # actions=latest_message_tool_calls
            actions=actions
        )

        chat_completion_tool_messages = [
            ChatCompletionToolMessageParam(
                content=str(result),
                role="tool",  # TODO: different role?
                # tool_call_id=tool_call.id,
                tool_call_id=tool_call.get("id"),
            )
            for tool_call, result in zip(latest_message_tool_calls, observations)
        ]

        return {"messages": chat_completion_tool_messages}
