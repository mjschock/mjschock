import asyncio
from pprint import pprint

from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langgraph.checkpoint.sqlite import SqliteSaver
from openai.types.chat.chat_completion_user_message_param import ChatCompletionUserMessageParam

from agent import Agent
from custom_tools import tools


memory = SqliteSaver.from_conn_string(":memory:")
memory = AsyncSqliteSaver.from_conn_string(":memory:")

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

async def main() -> None:
    """Run the agent."""

    agent = Agent(
        model,
        tools,
        checkpointer=memory,
        system_prompt=prompt,
    )

    # repo, issue = from_github()

    thread = {"configurable": {"thread_id": "1"}}

    chunk_count = 0

    async for chunk in agent.graph.astream(
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
