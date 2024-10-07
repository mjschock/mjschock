from typing import List

from composio import Action, App, action
from composio_openai import ComposioToolSet, WorkspaceType
from openai.types.chat import ChatCompletionToolParam
from openai.types.shared_params import FunctionDefinition

# Use following example to add your own custom tools


@action(toolname="cow", requires=["cowsay"])
def say(message: str) -> str:
    """
    Cow will say whatever you want it to say.

    :param message: Message string
    :return greeting: Formatted message.
    """
    import cowsay

    return cowsay.get_output_string("cow", message)


@action(toolname="get_weather", requires=["requests"])
def get_weather(location: str) -> str:
    """
    Get the current weather for a location.

    :param location: The location to get the weather for.
    :return weather: The current weather for the location.
    """
    import requests

    # print(f"Getting weather for {location}")

    response = requests.get(f"https://wttr.in/{location}?format=%C+%t")
    return response.text


# composio_toolset = ComposioToolSet(workspace_config=WorkspaceType.Docker())
composio_toolset = ComposioToolSet(workspace_config=WorkspaceType.Host())

# Get required tools
tools = [
    *composio_toolset.get_tools(
        actions=[
            # Action.GITHUB_CREATE_A_PULL_REQUEST,
            # Action.GMAIL_LIST_THREADS,
            # Action.TWITTER_USER_LOOKUP_ME,
            # Action.WEBTOOL_SCRAPE_WEBSITE_CONTENT,
            get_weather,
        ],
        # apps=[
            # App.FILETOOL,
            # App.SHELLTOOL,
        # ]
    ),
    # *composio_toolset.get_actions(
    #     actions=[
    #         get_weather,
    #         # say,  # This is just here as an example of a custom tool, you can remove it
    #         # Action.GITHUB_CREATE_A_PULL_REQUEST
    #     ]
    # ),
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
    )
    for tool in tools
]
