# importing all the neccassary libraries
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from agent_tools.tools import get_latest_news
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

# loading environment file
load_dotenv(override=True)


# creating outputparser
class short_summary(BaseModel):

    summary: str = Field(description="summary about the news")

    def to_dict(self):
        return {"summary": self.summary}


parser = PydanticOutputParser(pydantic_object=short_summary)


def Latest_news(topic: str):
    # connecting to openai chatmodel
    llm = ChatOpenAI(model="gpt-4o-mini")

    # creating dynamic prompt template
    template = """Provide me the lastest news about the following topic \n {topic_name}
    """

    prompt_template = PromptTemplate(template=template, input_variables=["topic_name"])

    final_prompt = prompt_template.format(topic_name=topic)

    # creating tools for agent
    agent_tools = [
        Tool(
            name="crawl google 3 news pages",
            func=get_latest_news,
            description="useful when you want to search for latest news",
        )
    ]

    # pulling react agent prompt from langchain hub
    react_promt = hub.pull("hwchase17/react")

    # creating agent
    agent = create_react_agent(llm=llm, tools=agent_tools, prompt=react_promt)

    # creating agent executor
    agent_exe = AgentExecutor(agent=agent, tools=agent_tools, verbose=True)

    result = agent_exe.invoke({"input": final_prompt})

    return result["output"]


if __name__ == "__main__":
    print("Daily News")
    print(Latest_news("andhra pradesh politics"))
