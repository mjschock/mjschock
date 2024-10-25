import asyncio
import json
import sqlite3
from pprint import pformat, pprint

# from agent import Agent
import aiosqlite
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from openai.types.chat.chat_completion_assistant_message_param import (
    ChatCompletionAssistantMessageParam,
)
from openai.types.chat.chat_completion_system_message_param import (
    ChatCompletionSystemMessageParam,
)
from openai.types.chat.chat_completion_user_message_param import (
    ChatCompletionUserMessageParam,
)
from swe_agent.tools import tools
from termcolor import colored

from swe_agent.agent import Agent

model = "llama3.2:1b"


async def main(thread_id: str = "1") -> None:
    """Run the agent."""

    # system_prompt = get_system_prompt(tools=tools)
    system_prompt = generate_system_prompt()

    # print("system_prompt:")
    # print(system_prompt)

    async with aiosqlite.connect("checkpoints.db") as conn:

        # conn = sqlite3.connect("checkpoints.sqlite")
        # memory = SqliteSaver(conn)
        memory = AsyncSqliteSaver(conn)

        agent = Agent(
            model,
            tools,
            checkpointer=memory,
            # system_prompt=system_prompt,
        )

        thread = {"configurable": {"thread_id": thread_id}}

        messages = [
            ChatCompletionSystemMessageParam(
                content=system_prompt,
                role="system",
            ),
            ChatCompletionAssistantMessageParam(
                content="Hello! How can I help you today?",
                role="assistant",
            ),
            # ChatCompletionUserMessageParam(
            #     content=f"What's the weather like today in Oakland, CA?",
            #     role="user",
            # ),
        ]

        pretty_print_conversation(messages)

        user_input = input("user:\n\n")
        print("")

        messages.append(
            ChatCompletionUserMessageParam(
                content=user_input,
                role="user",
            )
        )

        # pretty_print_conversation(messages[-1:])

        # for event in agent.graph.stream({"messages": messages}, thread):
        async for event in agent.graph.astream({"messages": messages}, thread):
            for v in event.values():
                # print(v["messages"])
                pretty_print_conversation(v["messages"])

        while (await agent.graph.aget_state(thread)).next:
            print("\n", (await agent.graph.aget_state(thread)).next, "\n")
            # _input = input("proceed? [modify, y, n]: ")
            _input = input("proceed? [modify, no, yes]: ")

            # if _input != "y":
            #     print("aborting")
            #     break

            if _input in ("m", "modify"):
                print("modifying...")
                # TODO: https://github.com/mjschock/deeplearning-ai/blob/main/ai-agents-in-langgraph/L5/Lesson_5_Student.ipynb
                raise NotImplementedError("The modify option is not yet implemented.")

            elif _input in ("n", "no"):
                print("aborting...")
                break

            print("")

            # for event in abot.graph.stream(None, thread):
            async for event in agent.graph.astream(None, thread):
                for v in event.values():
                    # print(v)
                    pretty_print_conversation(v["messages"])


def generate_system_prompt():
    # https://github.com/meta-llama/llama-models/blob/main/models/llama3_2/text_prompt_format.md#zero-shot-function-calling
    return """You are an expert in composing functions. You are given a question and a set of possible functions.
Based on the question, you will need to make one or more function/tool calls to achieve the purpose.
If none of the function can be used, point it out. If the given question lacks the parameters required by the function,
also point it out. You should only return the function call in tools call sections.

If you decide to invoke any of the function(s), you MUST put it in the format of [func_name1(params_name1=params_value1, params_name2=params_value2...), func_name2(params)]
You SHOULD NOT include any other text in the response.

Here is a list of functions in JSON format that you can invoke.

{tools}""".format(
        # tools=pformat(
        tools=json.dumps(
            list(
                map(
                    lambda tool: {
                        "name": tool.get("function").get("name"),
                        "description": tool.get("function").get("description"),
                        "parameters": {
                            "type": "dict",
                            "required": list(
                                tool.get("function")
                                .get("parameters")
                                .get("required", [])
                            ),
                            "properties": {
                                name: {
                                    "type": prop.get("type"),
                                    "description": prop.get("description"),
                                    "default": prop.get("default"),
                                }
                                for name, prop in tool.get("function")
                                .get("parameters")
                                .get("properties", {})
                                .items()
                            },
                        },
                    },
                    tools,
                )
            ),
            indent=4,
            # compact=True,
            # sort_dicts=False,
        )
    )


def pretty_print_conversation(
    messages,
):  # https://cookbook.openai.com/examples/how_to_call_functions_with_chat_models#utilities
    role_to_color = {
        "system": "red",
        "user": "green",
        "assistant": "blue",
        "tool": "magenta",
    }

    for message in messages:
        message_is_dict = type(message) == dict

        message_role = message.get("role") if message_is_dict else message.role
        message_content = message.get("content") if message_is_dict else message.content
        message_tool_calls = (
            message.get("tool_calls", [])
            if message_is_dict
            else message.tool_calls or []
        )

        if message_tool_calls:
            # print(colored(f"{message_tool_calls}\n", role_to_color[message_role]))
            print(
                colored(
                    f"{message_role}:\n\n{message_tool_calls}\n",
                    role_to_color[message_role],
                )
            )

        else:
            # print(colored(f"{message_content}\n", role_to_color[message_role]))
            print(
                colored(
                    f"{message_role}:\n\n{message_content}\n",
                    role_to_color[message_role],
                )
            )


if __name__ == "__main__":
    thread_id = "1"

    # TODO: Select a random thread from the following:
    # actions = composio_toolset.get_tools(actions=['GMAIL_LIST_THREADS'])
    # actions = composio_toolset.get_tools(actions=['GITHUB_LIST_REPOSITORY_ISSUES'])

    asyncio.run(main(thread_id=thread_id))
