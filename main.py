from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from tools import search_tool, wiki_tool, save_tool
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint


# --- RICH CLI UI IMPORTS ---
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown

# Load environment variables (.env)
load_dotenv()

# Initialize Rich Console
console = Console()

# Define the Pydantic Output Schema
class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]


# Initialize Gemini LLM with your updated model
llm_endpoint = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-72B-Instruct", # trained model for tools
    temperature=0.1,
    max_new_tokens=512,
)
# conver that as a Chat Model
llm = ChatHuggingFace(llm=llm_endpoint)

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

# Agent Executor (Set verbose=False to keep the Rich UI clean)
agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools, 
    verbose=False
)

# Execution Flow
if __name__ == "__main__":
    console.rule("[bold cyan] AI Agentic Research Assistant")
    print("\n")
    
    # Styled Input Prompt
    user_query = Prompt.ask("[bold green]What can I help you research?[/bold green]")
    print("\n")
    
    # Animated Loading Spinner while the agent works
    with console.status("[bold yellow]Agent is autonomously browsing the web & wiki...[/bold yellow]", spinner="dots"):
        raw_response = agent_executor.invoke({"query": user_query})
    
    try:
        output_text = raw_response.get("output", "")
        if isinstance(output_text, list) and len(output_text) > 0:
            output_text = output_text[0].get("text", "")
            
        structured_response = parser.parse(output_text)
        
        # Build Markdown content for the UI Panel
        markdown_content = f"""
**Topic:** {structured_response.topic}

**Summary:** 
{structured_response.summary}

**Sources:** 
{', '.join(structured_response.sources) if structured_response.sources else 'None'}

**Tools Used:** 
{', '.join(structured_response.tools_used)}
        """
        
        # Display formatted output inside a rich UI Panel
        console.print(Panel(
            Markdown(markdown_content), 
            title="[bold cyan]Research Complete[/bold cyan]", 
            border_style="cyan",
            expand=False
        ))
        
    except Exception as e:
        console.print(f"\n[bold red]Error parsing response:[/bold red] {e}")
        console.print(Panel(str(raw_response), title="Raw Response", border_style="red"))