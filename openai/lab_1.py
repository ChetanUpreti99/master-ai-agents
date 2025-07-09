from dotenv import load_dotenv
from agents import Agent, Runner, trace
import asyncio


load_dotenv(override=True)


# Make an agent with name, instructions, model
agent = Agent(name="Jokester", instructions="You are a joke teller", model="gpt-4o-mini")

# Run the joke with Runner.run(agent, prompt) then print final_output
async def main():
    with trace("Telling a joke"):
        result = await Runner.run(agent, "Tell a joke about Autonomous AI Agents")
        print(result.final_output)

asyncio.run(main())