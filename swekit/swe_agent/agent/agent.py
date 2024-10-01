"""CrewAI SWE Agent"""

import os

import dotenv
from crewai import Agent, Crew, Process, Task
from langchain_anthropic import ChatAnthropic
from custom_tools import say
from langchain_openai import ChatOpenAI
from prompts import BACKSTORY, DESCRIPTION, EXPECTED_OUTPUT, GOAL, ROLE

from composio_crewai import Action, App, ComposioToolSet, WorkspaceType


# Load environment variables from .env
dotenv.load_dotenv()

# Initialize tool.
anthropic_client = ChatAnthropic(
    # https://docs.litellm.ai/docs/providers/anthropic
    api_key=os.environ["ANTHROPIC_API_KEY"],  # type: ignore
    max_tokens=4096,
    model="claude-3-sonnet-20240229",
)
openai_client = ChatOpenAI(
    api_key=os.environ["OPENAI_API_KEY"],  # type: ignore
    model="gpt-4-1106-preview",
)
composio_toolset = ComposioToolSet(workspace_config=WorkspaceType.Docker())

# Get required tools
tools = [
    *composio_toolset.get_tools(
        actions=[
            Action.GITHUB_CREATE_A_PULL_REQUEST,
            Action.TWITTER_USER_LOOKUP_ME,
            Action.WEBTOOL_SCRAPE_WEBSITE_CONTENT,
        ],
        apps=[
            App.FILETOOL,
            App.SHELLTOOL,
        ]
    ),
    *composio_toolset.get_actions(
        actions=[
            say,  # This is just here as an example of a custom tool, you can remove it
            # Action.GITHUB_CREATE_A_PULL_REQUEST
        ]
    ),
]

# Define agent
agent = Agent(
    role=ROLE,
    goal=GOAL,
    backstory=BACKSTORY,
    llm=anthropic_client,
    # llm=openai_client,
    tools=tools,
    verbose=True,
)

task = Task(
    description=DESCRIPTION,
    expected_output=EXPECTED_OUTPUT,
    agent=agent,
)

crew = Crew(
    agents=[agent],
    tasks=[task],
    process=Process.sequential,
    verbose=True,
    cache=False,
    memory=True,
)
