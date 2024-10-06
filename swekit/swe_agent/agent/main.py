import asyncio
from pprint import pprint

from composio import Action
from llama_stack_client.types import UserMessage
from langchain_core.messages import AIMessage, AnyMessage, SystemMessage, HumanMessage, ToolMessage
from openai.types.chat.chat_completion_tool_message_param import ChatCompletionToolMessageParam
from openai.types.chat.chat_completion_user_message_param import ChatCompletionUserMessageParam
from openai.types.chat.chat_completion_system_message_param import ChatCompletionSystemMessageParam
from openai.types.chat.chat_completion_function_message_param import ChatCompletionFunctionMessageParam
from openai.types.chat.chat_completion_assistant_message_param import ChatCompletionAssistantMessageParam
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam

# from agent import composio_toolset, crew
# from agent import app, composio_toolset, tools
from agent import abot, composio_toolset, tools
from inputs import from_github
from prompts import BACKSTORY, DESCRIPTION, EXPECTED_OUTPUT, GOAL, ROLE

from openai import OpenAI



async def main() -> None:
    """Run the agent."""
    # repo, issue = from_github()

    # app.get_graph().draw_png(output_file_path=f"agent_workflow.png")

    # for chunk in app.stream(
    # await app.stream(
    # async for chunk in app.stream(

    thread = {"configurable": {"thread_id": "1"}}

    chunk_count = 0

    # async for chunk in app.astream(
    async for chunk in abot.graph.astream(
        {
            "messages": [
                ChatCompletionUserMessageParam(
                    content=f"What's the weather like today in Oakland, CA?",
                    # name=
                    role="user",
                ),
            ],
            # "tools": tools,
        },
        thread,
        stream_mode="values",
    ):
        print(f"\n--- CHUNK {chunk_count} (BEGIN) ---\n")
        print(f'type(chunk["messages"][-1]): {type(chunk["messages"][-1])}')
        pprint(chunk["messages"][-1])
        print(f"\n--- CHUNK {chunk_count} (END) ---\n")
        chunk_count += 1
        # print(f"=== END CHUNK {chunk_count} ===")

#     # crew.kickoff(
#     #     inputs={
#     #         "repo": repo,
#     #         "issue": issue,
#     #     }
#     # )
#     # response = composio_toolset.execute_action(
#     #     action=Action.FILETOOL_GIT_PATCH,
#     #     params={},
#     # )
#     # data = response.get("data", {})
#     # if data.get("error") and len(data["error"]) > 0:
#     #     print("Error:", data["error"])
#     # elif data.get("patch"):
#     #     print("=== Generated Patch ===\n" + data["patch"])
#     # else:
#     #     print("No output available")


if __name__ == "__main__":
    # main()
    asyncio.run(main())
