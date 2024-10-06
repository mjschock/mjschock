import asyncio
from pprint import pprint

from openai.types.chat.chat_completion_user_message_param import ChatCompletionUserMessageParam

from agent import abot
from inputs import from_github


async def main() -> None:
    """Run the agent."""
    # repo, issue = from_github()

    thread = {"configurable": {"thread_id": "1"}}

    chunk_count = 0

    async for chunk in abot.graph.astream(
        {
            "messages": [
                ChatCompletionUserMessageParam(
                    content=f"What's the weather like today in Oakland, CA?",
                    # name=
                    role="user",
                ),
            ],
        },
        thread,
        stream_mode="values",
    ):
        print(f"\n--- CHUNK {chunk_count} (BEGIN) ---\n")
        print(f'type(chunk["messages"][-1]): {type(chunk["messages"][-1])}')
        pprint(chunk["messages"][-1])
        print(f"\n--- CHUNK {chunk_count} (END) ---\n")
        chunk_count += 1

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
    asyncio.run(main())
