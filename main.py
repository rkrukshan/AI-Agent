from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_tool, wiki_tool, save_tool

# Load environment variables (.env)
load_dotenv()


# Define the Pydantic Output Schema
class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]


# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

# Setup Pydantic Parser
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

# Define Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a research assistant that will help generate a research paper. 
            Answer the user query and use the necessary tools.
            Wrap the output in this format and provide no other text:
            \n{format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

# Tools list
tools = [search_tool, wiki_tool, save_tool]

# Create Agent
agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)

# Agent Executor
agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools, 
    verbose=True
)

# Execution Flow
if __name__ == "__main__":
    user_query = input("What can I help you research? ")
    
    raw_response = agent_executor.invoke({"query": user_query})
    
    try:
        output_text = raw_response.get("output", "")
        if isinstance(output_text, list) and len(output_text) > 0:
            output_text = output_text[0].get("text", "")
            
        structured_response = parser.parse(output_text)
        print("\n--- Parsed Research Response ---")
        print(f"Topic: {structured_response.topic}")
        print(f"Summary: {structured_response.summary}")
        print(f"Sources: {structured_response.sources}")
        print(f"Tools Used: {structured_response.tools_used}")
        
    except Exception as e:
        print("\nError parsing response:", e)
        print("Raw Response:", raw_response)