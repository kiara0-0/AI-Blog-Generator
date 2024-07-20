from crewai import Task
from textwrap import dedent
# This is an example of how to define custom tasks.
# You can define as many tasks as you want.
# You can also define custom agents in agents.py
class CustomTasks:

    def task_plan(self, agent, topic):
        return Task(
            description=(
        f"""1. Prioritize the latest trends, key players, 
            and noteworthy news on {topic}. Make sure to come up with interesting titles for each
            segement.
        2. Identify the target audience, considering 
            their interests and pain points.
        3. Develop a detailed content outline including 
            an introduction, key points, and a call to action
        4. Include SEO keywords and relevant data or sources."""
    ),
    expected_output="""A comprehensive content plan document 
        with an outline, audience analysis, 
        SEO keywords, and resources.""",
    agent=agent,
    # variables= {"topic": topic}
        )

    def task_write(self, agent, topic):
        return Task(
                description=(
            f"""1. Use the content plan to craft a compelling 
                blog post on {topic}.
            2. Incorporate SEO keywords naturally.
            3. Sections/Subtitles are properly named 
                in an engaging manner.
            4. Ensure the post is structured with an 
                engaging introduction, insightful body, 
                and a summarizing conclusion.
            5. Proofread for grammatical errors and 
                alignment with the brand's voice.\n"""
        ),
        expected_output="""A well-written blog post 
            in markdown format, ready for publication, 
            each section should have 2 or 3 paragraphs.""",
            agent=agent,
            
            # variables= {"topic": topic}
        )
    
    def task_edit(self, agent):
        return Task(
            description=("""Proofread the given blog post for 
                 grammatical errors and 
                 alignment with the brand's voice."""),
            expected_output="""A well-written blog post in markdown format, 
                    ready for publication, 
                    each section should have 2 or 3 paragraphs.""",
    agent=agent,
    # variables= {"topic": topic}
        )