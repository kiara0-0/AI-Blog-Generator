from crewai import Agent
from textwrap import dedent
from langchain_community.llms import Ollama
import os
import json
import requests
from langchain.tools import tool

class SearchTools():

  @tool("Search the internet")
  def search_internet(query):
    """Useful to search the internet
    about a a given topic and return relevant results"""
    top_result_to_return = 4
    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": query})
    headers = {
        'X-API-KEY': os.environ['SERPER_API_KEY'],
        'content-type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    # check if there is an organic key
    if 'organic' not in response.json():
      return "Sorry, I couldn't find anything about that, there could be an error with your serper api key."
    else:
      results = response.json()['organic']
      string = []
      for result in results[:top_result_to_return]:
        try:
          string.append('\n'.join([
              f"Title: {result['title']}", f"Link: {result['link']}",
              f"Snippet: {result['snippet']}", "\n-----------------"
          ]))
        except KeyError:
          next

      return '\n'.join(string)

llm = Ollama(
    model = "llama3",
    base_url = "http://localhost:11434",
    temperature =0.7 )

# This is an example of how to define custom agents.
# You can define as many agents as you want.
# You can also define custom tasks in tasks.py
class CustomAgents:

    def content_planner(self, topic):
        return Agent(
        role="Content Planner",
        goal=f"Plan engaging and factually accurate content on {topic}",
        backstory=f"""You're working on planning a blog article 
                about the topic: {topic}.
                You collect information that helps the 
                audience learn something 
                and make informed decisions. You have to prepare a detailed 
                outline and the relevant topics and sub-topics that has to be a part of the
                blogpost.
                Your work is the basis for 
                the Content Writer to write an article on this topic.""",
        llm=llm,
        tool=[SearchTools.search_internet],
        allow_delegation=False,
        verbose=True,
        # variables= {"topic": topic}
    )

    def content_writer(self, topic):
        return Agent(
        role="Content Writer",
        goal=f"""Write insightful and factually accurate
            opinion piece about the topic: {topic}""",
        backstory=f"""You're working on a writing 
                a new opinion piece about the topic: {topic}. 
                You base your writing on the work of 
                the Content Planner, who provides an outline 
                and relevant context about the topic. 
                You follow the main objectives and 
                direction of the outline, 
                as provided by the Content Planner. 
                You also provide objective and impartial insights 
                and back them up with information 
                provided by the Content Planner. 
                You acknowledge in your opinion piece 
                when your statements are opinions 
                as opposed to objective statements.""",
        allow_delegation=False,
        llm=llm,
        tool=[SearchTools.search_internet],
        verbose=True,
        # variables= {"topic": topic}
    )

    def content_editor(self, topic):
        return Agent(
        role="Editor",
        goal="""Edit a given blog post to align with 
            the most popular writing styles of the internet. """,
        backstory="""You are an editor who receives a blog post 
                from the Content Writer. 
                Your goal is to review the blog post 
                to ensure that it follows journalistic best practices,
                provides balanced viewpoints 
                when providing opinions or assertions, 
                and also avoids major controversial topics 
                or opinions when possible.""",
        llm=llm,
        tool=[SearchTools.search_internet],
        allow_delegation=False,
        verbose=True,
        # variables= {"topic": topic}
    )
