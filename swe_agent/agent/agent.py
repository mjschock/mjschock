"""CrewAI SWE Agent"""

import os

import dotenv
from composio import LogLevel
from composio_crewai import Action, App, ComposioToolSet, WorkspaceType
from crewai import Agent, Crew, Process, Task
from custom_tools import say
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_openai import ChatOpenAI
from prompts import BACKSTORY, DESCRIPTION, EXPECTED_OUTPUT, GOAL, ROLE

# Load environment variables from .env
dotenv.load_dotenv()

# Initialize tool.
ollama_client = ChatOllama(
    model="llama3.2:1b",
    temperature=0,
)
openai_client = ChatOpenAI(
    api_key=os.environ["OPENAI_API_KEY"],  # type: ignore
    model="gpt-4-1106-preview",
)

composio_toolset = ComposioToolSet(
    logging_level=LogLevel.DEBUG,
    # output_in_file=True,
    workspace_config=WorkspaceType.Docker(),
)

# Get required tools
tools = [
    *composio_toolset.get_tools(
        actions=[
            # say,
            # Action.GITHUB_CREATE_A_PULL_REQUEST,
            # Action.GIT_GITHUB_CLONE_CMD,
            # Action.FILETOOL_GIT_CLONE,
            # Action.FILETOOL_GIT_PATCH,
        ],
        apps=[
            # App.GITHUB,
            App.FILETOOL,
            App.SHELLTOOL,
        ],
    ),
    # *composio_toolset.get_actions(
    #     actions=[
    #         say,  # This is just here as an example of a custom tool, you can remove it
    #         # Action.GITHUB_CREATE_A_PULL_REQUEST
    #     ]
    # ),
]

# Define agent
agent = Agent(
    backstory=BACKSTORY,
    goal=GOAL,
    llm=ollama_client,
    # llm=openai_client,
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
    embedder={
        "config": dict(
            model="all-minilm:latest",
        ),
        "provider": "ollama",
    },
    # embedder={"provider": "openai"},
    memory=True,
    process=Process.sequential,
    tasks=[task],
    verbose=True,
)
