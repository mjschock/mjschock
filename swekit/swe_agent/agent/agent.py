"""Composio-LangGraph SWE Agent"""

import operator
from typing import TypedDict

import dotenv
from custom_tools import composio_toolset
from langgraph.graph import END, StateGraph
from openai import OpenAI
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from openai.types.chat.chat_completion_system_message_param import (
    ChatCompletionSystemMessageParam,
)
from openai.types.chat.chat_completion_tool_message_param import (
    ChatCompletionToolMessageParam,
)
from typing_extensions import Annotated

# Load environment variables from .env
dotenv.load_dotenv()


class Environment:
    def __init__(self, composio_toolset):
        self.composio_toolset = composio_toolset

    def step(self, actions):
        # latest_message = state['messages'][-1]
        # latest_message_tool_calls = latest_message.tool_calls

        results = []

        # for tool_call in latest_message_tool_calls:
        for tool_call in actions:
            results.append(
                composio_toolset.execute_tool_call(
                    tool_call=tool_call,
                    entity_id=composio_toolset.entity_id,
                )
            )

        # chat_completion_tool_messages = [
        #     ChatCompletionToolMessageParam(
        #         content=str(result),
        #         role="tool", # TODO: different role?
        #         tool_call_id=tool_call.id,
        #     # ) for tool_call, result in zip(latest_message_tool_calls, results)
        #     ) for tool_call, result in zip(actions, results)
        # ]

        # return {'messages': chat_completion_tool_messages}

        # return results
        observations = results
        rewards = [0] * len(results)
        terminations = [False] * len(results)
        truncations = [False] * len(results)
        infos = [{}] * len(results)

        return observations, rewards, terminations, truncations, infos


env = Environment(composio_toolset)


class AgentState(TypedDict):
    messages: Annotated[list[ChatCompletionMessageParam], operator.add]


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

        # self.graph = graph.compile(checkpointer=checkpointer)
        self.graph = graph.compile()
        self.model = model
        self.tools = tools
        self.system_prompt = system_prompt

    def exists_action(self, state: AgentState):
        result = state["messages"][-1]

        if result.tool_calls:
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

        message = response.choices[0].message

        return {
            "messages": [message],
        }

    def take_action(self, state: AgentState):
        latest_message = state["messages"][-1]
        latest_message_tool_calls = latest_message.tool_calls

        # results = []

        # for tool_call in latest_message_tool_calls:
        #     results.append(
        #         composio_toolset.execute_tool_call(
        #             tool_call=tool_call,
        #             entity_id=composio_toolset.entity_id,
        #         )
        #     )

        # results = env.step(actions=latest_message_tool_calls)
        observations, rewards, terminations, truncations, infos = env.step(
            actions=latest_message_tool_calls
        )

        chat_completion_tool_messages = [
            ChatCompletionToolMessageParam(
                content=str(result),
                role="tool",  # TODO: different role?
                tool_call_id=tool_call.id,
                # ) for tool_call, result in zip(latest_message_tool_calls, results)
            )
            for tool_call, result in zip(latest_message_tool_calls, observations)
        ]

        return {"messages": chat_completion_tool_messages}
