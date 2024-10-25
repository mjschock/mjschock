import warnings

from agent import composio_toolset, crew
from composio import Action
from inputs import from_github

warnings.filterwarnings("ignore")


def main() -> None:
    """Run the agent."""
    repo, issue = from_github()

    print('repo: "{}"'.format(repo))
    print('issue: "{}"'.format(issue))

    response = composio_toolset.execute_action(
        action=Action.FILETOOL_GIT_CLONE,
        params={
            # "commit_id": "",
            "destination": "/home/user",
            # "just_reset": True,
            "repo_name": repo,
        },
    )

    print("response:")
    print(response)

    # raise Exception("Stop here")

    data = response.get("data", {})

    assert data.get("success") is True, data.get("error")

    crew.kickoff(
        inputs={
            "repo": repo,
            "issue": issue,
        }
    )

    response = composio_toolset.execute_action(
        action=Action.FILETOOL_GIT_PATCH,
        params={},
    )

    data = response.get("data", {})

    print("data:")
    print(data)

    if data.get("error") and len(data["error"]) > 0:
        print("Error:", data["error"])

    elif data.get("patch"):
        print("=== Generated Patch ===\n" + data["patch"])

    else:
        print("No output available")


if __name__ == "__main__":
    main()
