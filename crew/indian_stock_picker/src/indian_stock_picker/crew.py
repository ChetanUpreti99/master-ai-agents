#!/usr/bin/env python
import os
from datetime import datetime
from pydantic import BaseModel, Field
from typing import List
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from .tools.push_tool import PushNotificationTool

class ShortTermStock(BaseModel):
    ticker: str = Field(description="Stock ticker symbol")
    name: str = Field(description="Company name")
    reason: str = Field(description="Why it's trending short‑term")

class ShortTermStockList(BaseModel):
    stocks: List[ShortTermStock]

class LongTermStock(BaseModel):
    ticker: str = Field(description="Stock ticker symbol")
    name: str = Field(description="Company name")
    fundamentals: str = Field(description="Fundamental thesis for long‑term growth")

class LongTermStockList(BaseModel):
    stocks: List[LongTermStock]

@CrewBase
class StockPicker():
    """StockPicker crew for Indian short‑ and long‑term picks"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def trending_stock_finder(self) -> Agent:
        return Agent(
            config=self.agents_config['trending_stock_finder'],
            tools=[SerperDevTool()],
            memory=True
        )

    @agent
    def fundamental_stock_finder(self) -> Agent:
        return Agent(
            config=self.agents_config['fundamental_stock_finder'],
            tools=[SerperDevTool()]
        )

    @agent
    def stock_picker(self) -> Agent:
        return Agent(
            config=self.agents_config['stock_picker'],
            tools=[PushNotificationTool()],
            memory=True
        )

    @task
    def find_short_term_stocks(self) -> Task:
        return Task(
            config=self.tasks_config['find_short_term_stocks'],
            output_pydantic=ShortTermStockList
        )

    @task
    def find_long_term_stocks(self) -> Task:
        return Task(
            config=self.tasks_config['find_long_term_stocks'],
            output_pydantic=LongTermStockList
        )

    @task
    def pick_two_stocks(self) -> Task:
        return Task(
            config=self.tasks_config['pick_two_stocks']
        )

    @crew
    def crew(self) -> Crew:
        manager = Agent(
            config=self.agents_config['stock_picker'],  # reuse stock_picker as manager
            allow_delegation=True
        )
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.hierarchical,
            verbose=True,
            manager_agent=manager,
            memory=True
        )
