"""CrewAI SWE Agent"""

import os

import dotenv
from composio_crewai import Action, App, ComposioToolSet, WorkspaceType
from crewai import Agent, Crew, LLM, Process, Task
from langchain_openai import ChatOpenAI

from custom_tools import say
from prompts import BACKSTORY, DESCRIPTION, EXPECTED_OUTPUT, GOAL, ROLE

# Load environment variables from .env
dotenv.load_dotenv()

# provider = "anthropic"
# provider = "github"
provider = "ollama"
# provider = "openai"

embedder = {
    "provider": "gpt4all",
    "config": {
        # "model": "all-MiniLM-L6-v2-f16.gguf",
        "model": "all-MiniLM-L6-v2.gguf2.f16.gguf",
    }
}

if provider == "anthropic":
    llm = LLM(
        api_key=os.environ["ANTHROPIC_API_KEY"],
        model="claude-3-sonnet-20240229",
    )

elif provider == "ollama":
    llm = LLM(
        base_url="http://localhost:11434",
        model="ollama/llama3.2:1b",
    )

elif provider == "openai":
    embedder = {
        "provider": "openai",
        "config": {
            "model": 'text-embedding-3-small'
        }
    }
    llm = ChatOpenAI(
        api_key=os.environ["OPENAI_API_KEY"],
        # model="gpt-4-1106-preview",
        model="gpt-3.5-turbo",
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
    backstory=BACKSTORY,
    goal=GOAL,
    # function_calling_llm=llm,
    llm=llm,
    role=ROLE,
    tools=tools,
    verbose=True,
)

task = Task(
    agent=agent,
    description=DESCRIPTION,
    expected_output=EXPECTED_OUTPUT,
)

crew = Crew(
    agents=[agent],
    cache=False,
    embedder=embedder,
    # manager_llm=llm,
    memory=True,
    process=Process.sequential,
    tasks=[task],
    verbose=True,
)
