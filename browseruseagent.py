from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio

async def main():
    agent = Agent(
        task="Find a round trip flight to airport OGG June 21-28 2025 on Alaska or Hawaiian airlines. Departing from PDX to OGG. 2 adults 2 children (8 and 10 years old). Present to me the cheapest option for flights that arrive before 3pm in OGG.",
        llm=ChatOpenAI(model="gpt-4o"),
    )
    result = await agent.run()
    print(result)

asyncio.run(main())