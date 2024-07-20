import os
from crewai import Crew
# from langchain_openai import Ollama
# from decouple import config

from textwrap import dedent
from agents import CustomAgents
from tasks import CustomTasks
# from IPython.display import Markdown,display
# from IPython.display import display, Markdown, Latex
from rich.console import Console
from rich.markdown import Markdown
# import sys


# This is the main class that you will use to define your custom crew.
# You can define as many agents and tasks as you want in agents.py and tasks.py

console=Console()

class CustomCrew:

    def __init__(self, topic):
        self.topic = topic
        

    def run(self):
        # Define your custom agents and tasks in agents.py and tasks.py
        agents = CustomAgents()
        tasks = CustomTasks()

        # Define your custom agents and tasks here
        content_planner = agents.content_planner(self.topic)
        content_writer = agents.content_writer(self.topic)
        content_editor= agents.content_editor(self.topic)

        # Custom tasks include agent name and variables as input
        task_plan = tasks.task_plan(
            content_planner,
            self.topic,
        )

        task_write = tasks.task_write(
            content_writer,
            self.topic,
        )

        task_edit = tasks.task_edit(
            content_editor,
            
        )

        # Define your custom crew here
        crew = Crew(
            agents=[content_planner, content_writer, content_editor],
            tasks=[task_plan, task_write, task_edit],
            verbose=True,
        )

        result = crew.kickoff()
        return result



# This is the main function that you will use to run your custom crew.
if __name__ == "__main__":
    
    topic = input(dedent("""Enter the topic on which you would like a blog post on: """))
    print(topic)
    custom_crew = CustomCrew(topic)
    result = custom_crew.run()

    print("\n\n########################")
    print("## Here is your AI generated blog:")
    print("########################\n")
    console.print(Markdown(result))