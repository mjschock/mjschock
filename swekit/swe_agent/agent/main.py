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

client = OpenAI(
    api_key='ollama',
    base_url = 'http://localhost:11434/v1',
)

system_prompt = """
You run in a loop of Thought, Action, PAUSE, Observation.
At the end of the loop you output an Answer
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Observation will be the result of running those actions.

Your available actions are:

calculate:
e.g. calculate: 4 * 7 / 3
Runs a calculation and returns the number - uses Python so be sure to use floating point syntax if necessary

average_dog_weight:
e.g. average_dog_weight: Collie
returns average weight of a dog when given the breed

Example session:

Question: How much does a Bulldog weigh?
Thought: I should look the dogs weight using average_dog_weight
Action: average_dog_weight: Bulldog
PAUSE

You will be called again with this:

Observation: A Bulldog weights 51 lbs

You then output:

Answer: A bulldog weights 51 lbs
""".strip()

response = client.chat.completions.create(
  messages=[
    # {"role": "system", "content": "You are a helpful assistant."},
    {"role": "system", "content": system_prompt},
    # {"role": "user", "content": "Who won the world series in 2020?"},
    # {"role": "assistant", "content": "The LA Dodgers won in 2020."},
    # {"role": "user", "content": "Where was it played?"}
    {"role": "user", "content": "What's the weather like today in Oakland, CA?"}
  ],
  model="llama3.2:1b",
  tools=tools,
)

print(response.choices[0].message)

# async def main() -> None:
#     """Run the agent."""
#     repo, issue = from_github()

#     # app.get_graph().draw_png(output_file_path=f"agent_workflow.png")

#     # for chunk in app.stream(
#     # await app.stream(
#     # async for chunk in app.stream(

#     chunk_count = 0

#     # async for chunk in app.astream(
#     async for chunk in abot.graph.astream(
#         {
#             "messages": [
#                 # (
#                 #     "system",
#                 #     f"You are a {ROLE}. Your goal is as follows:\n\n{GOAL}\n\nHere is your backstory:\n\n{BACKSTORY}",
#                 # ),
#                 # AIMessage(
#                 #     content=f"You are a {ROLE}. Your goal is as follows:\n\n{GOAL}\n\nHere is your backstory:\n\n{BACKSTORY}",
#                 # ),
#                 # (
#                 #     "human",
#                 #     # "Star the Github Repository composiohq/composio",
#                 #     # "Get my information.",
#                 #     f"{EXPECTED_OUTPUT.format(repo=repo, issue=issue)}\n\nHere is the expected output:\n\n{EXPECTED_OUTPUT}",
#                 # )
#                 # HumanMessage(
#                 #     content=f"{EXPECTED_OUTPUT.format(repo=repo, issue=issue)}\n\nHere is the expected output:\n\n{EXPECTED_OUTPUT}",
#                 # ),
#                 # HumanMessage(
#                 #     # content=f"What's the weather like today?",
#                 #     content=f"What's the weather like today in Oakland, CA?",
#                 #     # content=f"What day and time is it?",
#                 #     # content=f"What's the weather like in London?",
#                 # ),
#                 # UserMessage(
#                 #     content=f"What's the weather like today in Oakland, CA?",
#                 # ),
#                 ChatCompletionUserMessageParam(
#                     content=f"What's the weather like today in Oakland, CA?",
#                     # name=
#                     role="user",
#                 ),
#             ],
#             # "tools": tools,
#         },
#         stream_mode="values",
#     ):
#         # chunk["messages"][-1].pretty_print()
#         print(f"=== BEGIN CHUNK {chunk_count} ===")
#         # for message in chunk["messages"]:
#             # message.pretty_print()
#         # chunk["messages"][-1].pretty_print()
#         pprint(chunk["messages"][-1])
#         print(f"=== END CHUNK {chunk_count} ===")

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


# if __name__ == "__main__":
#     # main()
#     asyncio.run(main())
