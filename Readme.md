```markdown
# AI Research Assistant Agent

An intelligent, multi-tool AI Research Assistant built using **LangChain**, **Pydantic**, and LLM models (Anthropic Claude / OpenAI GPT). The agent processes natural language research queries, autonomously searches online sources (Wikipedia, DuckDuckGo), saves detailed reports to text files, and returns strictly structured Pydantic data.
to run app  ./venv/Scripts/python.exe main.py

---

## 📌 Features

- **Autonomous Tool Selection:** Automatically decides whether to use web search, Wikipedia, or file-saving tools based on user instructions.
- **Structured Pydantic Output:** Ensures responses follow a consistent, schema-backed format containing:
  - `topic`: Research headline/topic
  - `summary`: Comprehensive breakdown of findings
  - `sources`: Cited sources and links
  - `tools_used`: List of tools executed during the session
- **Multi-LLM Support:** Seamlessly switch between Anthropic Claude (`claude-3-5-sonnet`) and OpenAI (`gpt-4o-mini`).
- **File System Integration:** Generates timestamped `.txt` research output directly to the local directory.

---

## 📁 Project Structure

```text
.
├── main.py              # Main execution script, prompt template, schema, and agent loop
├── tools.py             # Custom and community tool definitions (Search, Wikipedia, Save to TXT)
├── requirements.txt     # Python dependencies with pinned compatible versions
└── .env                 # Environment file storing API key credentials

```

---

## 🛠️ Setup & Installation

### 1. Prerequisites

* Python `3.10` or higher installed.

### 2. Clone / Setup Project Folder

Create and navigate into your project folder:

```bash
mkdir ai-research-agent
cd ai-research-agent

```

### 3. Create & Activate Virtual Environment

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate

```

### 4. Install Dependencies

```bash
pip install -r requirements.txt

```

---

## 🔑 Environment Configuration

Create a `.env` file in the root project directory and add your LLM API keys:

```env
# If using Anthropic (Claude)
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# If using OpenAI (GPT)
# OPENAI_API_KEY=your_openai_api_key_here

```

---

## 🚀 Usage

Run the agent via the command line:

```bash
python main.py

```

### Example Prompt & Execution Loop

```text
What can I help you research? Tell me about quantum computing and save it to a file.

```

1. The agent queries **Wikipedia** and **DuckDuckGo** to collect up-to-date facts.
2. The agent executes `save_text_to_file` to write `research_output.txt`.
3. The final response is parsed and printed as structured data:

```text
--- Parsed Research Response ---
Topic: Quantum Computing Overview
Summary: Quantum computing leverages quantum mechanics principles like superposition and entanglement...
Sources: ['[https://en.wikipedia.org/wiki/Quantum_computing](https://en.wikipedia.org/wiki/Quantum_computing)']
Tools Used: ['wiki_tool', 'search', 'save_text_to_file']

```

---

## 🧰 Available Tools (`tools.py`)

1. **`search` (`DuckDuckGoSearchRun`)**: Real-time web search for recent events and generic information.
2. **`wiki_tool` (`WikipediaQueryRun`)**: Queries Wikipedia summaries for structured knowledge.
3. **`save_text_to_file`**: Custom Python function that writes timestamped research findings into a local text file.

```

```