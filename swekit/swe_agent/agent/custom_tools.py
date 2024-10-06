from composio import action

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

    print(f"Getting weather for {location}")

    response = requests.get(f"https://wttr.in/{location}?format=%C+%t")
    return response.text
