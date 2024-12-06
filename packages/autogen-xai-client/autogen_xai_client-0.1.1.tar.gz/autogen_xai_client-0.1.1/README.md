# autogen-xai-client
This is an autogen>=0.4 extension for xai client integration.


## Disclaimer
- This project is still in a very early stage under development, please create issues in this github repo for bug reports.
- This project is a personal endeavor and is not affiliated with, endorsed by, or connected to any organization/employer in any way. The views, ideas, and opinions expressed in this project are solely my own and do not reflect those of others.

## Usage

### Prerequisites
- create a python environment with version `3.10` or above
- `pip install --upgrade autogen-xai-client`


### code snippets

Importing dependencies:

```python
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.task import Console, TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_xai_client import XAIChatCompletionClient
from autogen_xai_client.config import XAIClientConfiguration
```

Create a xai client

```python
xai_client = XAIChatCompletionClient(
    base_url="https://api.x.ai/v1",
    model="grok-beta",
    api_key="<api_key>",
)
```

Define an agent using the xai client and register a dummy tool for querying weather

```python
# Define a tool
async def get_weather(city: str) -> str:
    return f"The weather in {city} is 73 degrees and Sunny."


async def main() -> None:
    # Define an agent
    weather_agent = AssistantAgent(
        name="weather_agent",
        model_client=wx_client,
        tools=[get_weather],
    )

    # Define termination condition
    termination = TextMentionTermination("TERMINATE")

    # Define a team
    agent_team = RoundRobinGroupChat([weather_agent], termination_condition=termination)

    # Run the team and stream messages to the console
    stream = agent_team.run_stream(task="What is the weather in New York?")
    await Console(stream)


# NOTE: if running this inside a Python script you'll need to use asyncio.run(main()).
await main()
```
