from dotenv import load_dotenv  
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()


class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used:list[str]

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
parser = PydanticOutput(pydantic_object=ResearchResponse)

# response = llm.invoke("what is the meaning of life?")
# print(response.content)


