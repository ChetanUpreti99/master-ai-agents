from agents import Agent, WebSearchTool, trace, Runner, gen_trace_id, function_tool
from agents.model_settings import ModelSettings
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import asyncio
import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content
from typing import Dict
from IPython.display import display, Markdown

load_dotenv(override=True)

sendgrid_api_key = os.getenv('SENDGRID_API_KEY')

if sendgrid_api_key:
    print(f"Sendgrid API Key exists and begins {sendgrid_api_key[:3]}")
else:
    print("Sendgrid API Key not set")


async def main():
    INSTRUCTIONS = "You are a research assistant. Given a search term, you search the web for that term and \
produce a concise summary of the results. The summary must 2-3 paragraphs and less than 300 \
words. Capture the main points. Write succintly, no need to have complete sentences or good \
grammar. This will be consumed by someone synthesizing a report, so it's vital you capture the \
essence and ignore any fluff. Do not include any additional commentary other than the summary itself."

    search_agent = Agent(
        name="Search agent",
        instructions=INSTRUCTIONS,
        tools=[WebSearchTool(search_context_size="low")],
        model="gpt-4o-mini",
        model_settings=ModelSettings(tool_choice="required"),
    )

    message = "Latest AI Agent frameworks in 2025"
    with trace("Search"):
        result = await Runner.run(search_agent, message)
        print(result.final_output)
        

# asyncio.run(main())

async def main():
    HOW_MANY_SEARCHES = 3

    INSTRUCTIONS = f"You are a helpful research assistant. Given a query, come up with a set of web searches \
    to perform to best answer the query. Output {HOW_MANY_SEARCHES} terms to query for."

    class WebSearchItem(BaseModel):
        reason: str = Field(description="Your reasoning for why this search is important to the query.")

        query: str = Field(description="The search term to use for the web search.")

    class WebSearchPlan(BaseModel):
        searches: list[WebSearchItem] = Field(description="A list of web searches to perform to best answer the query.")    
    
    planner_agent = Agent(
        name="PlannerAgent",
        instructions=INSTRUCTIONS,
        model="gpt-4o-mini",
        output_type=WebSearchPlan,
    )

    message = "Latest AI Agent frameworks in 2025"

    with trace("Search"):
        result = await Runner.run(planner_agent, message)
        print(result.final_output)

asyncio.run(main())