import asyncio
from pprint import pprint

from agent import Agent
from custom_tools import tools
from inputs import from_github
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from openai.types.chat.chat_completion_assistant_message_param import (
    ChatCompletionAssistantMessageParam,
)
from openai.types.chat.chat_completion_user_message_param import (
    ChatCompletionUserMessageParam,
)
from prompts import BACKSTORY, EXPECTED_OUTPUT, DESCRIPTION, GOAL, ROLE, SYSTEM_PROMPT, get_system_prompt

memory = SqliteSaver.from_conn_string(":memory:")
# memory = AsyncSqliteSaver.from_conn_string(":memory:")

model = "llama3.2:1b"


async def main(thread_id: str = "1") -> None:
    """Run the agent."""

    # system_prompt = get_system_prompt(tools=tools)
    system_prompt = SYSTEM_PROMPT.format(
        tools=list(
            map(
                lambda tool: {
                    "name": tool.get("function").get("name"),
                    "description": tool.get("function").get("description"),
                    "parameters": {
                        "type": "dict",
                        "required": list(
                            tool.get("function").get("parameters").get("required", [])
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
        )
    )

    print("system_prompt:")
    print(system_prompt)

    agent = Agent(
        model,
        tools,
        checkpointer=memory,
        system_prompt=system_prompt,
    )

    # repo, issue = from_github()
    # repo, issue_number, issue = from_github()

    thread = {"configurable": {"thread_id": thread_id}}

    chunk_count = 0

    async for chunk in agent.graph.astream(
        {
            "messages": [
                # ChatCompletionAssistantMessageParam(
                #     # content=f"""Role: {ROLE}\n\n{BACKSTORY}\n\n{GOAL}""",

                #     role="assistant",
                # ),
                ChatCompletionUserMessageParam(
                    content=f"What's the weather like today in Oakland, CA?",
                    # content=f"What's my latest email?",
                    # content=f"""{DESCRIPTION.format(issue=issue, repo=repo)}\n\nEXPECTED_OUTPUT:\n{EXPECTED_OUTPUT}""",
                    # content=f"""{DESCRIPTION.format(issue=issue, repo=repo)}\n\nPlease use a tool to generate a patch for the issue.""",
                    # content=f"""Please use a tool to generate a patch for {issue} issue in {repo}.""",
                    # content=f"""Please generate a patch for issue {issue_number} in the GitHub repository {repo}.\nThe issue is:\n{issue}""",
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
    thread_id = "1"

    # TODO: Select a random thread from the following:
    # actions = composio_toolset.get_tools(actions=['GMAIL_LIST_THREADS'])
    # actions = composio_toolset.get_tools(actions=['GITHUB_LIST_REPOSITORY_ISSUES'])

    asyncio.run(main(thread_id=thread_id))
