# 🤖 AI Agentic Research Assistant

An intelligent, multi-tool AI Research Assistant built using **LangChain 1.3+**, **Pydantic V2**, and the **Hugging Face Inference API**. 

The agent processes natural language research queries, autonomously searches online sources (Wikipedia, DuckDuckGo), saves detailed reports to text files, and returns strictly structured Pydantic data.

---

## 📌 Features

- **Autonomous Tool Selection:** The agent automatically decides whether to use web search, Wikipedia, or file-saving tools based on user instructions.
- **Structured Pydantic Output:** Ensures responses follow a consistent, schema-backed JSON/Python format.
- **Hugging Face Integration:** Uses state-of-the-art open-source models (like Qwen 72B) via the Hugging Face serverless Inference API.
- **File System Integration:** Generates timestamped `.txt` research output directly to the local directory.
- **Rich UI:** Beautiful, colorful terminal UI with loading spinners and markdown panels.

---

## 📁 Project Structure

```text
.
├── main.py              # Main execution script, prompt template, schema, and agent loop
├── tools.py             # Custom tool definitions (Search, Wikipedia, Save to TXT)
├── requirements.txt     # Python dependencies with updated compatible versions
└── .env                 # Environment file storing API key credentials
```

---

## 🧠 How It Works (Execution Flow)

1. **Input**: User types a query into the terminal (e.g., *"Research Quantum Computing and save it"*).
2. **Thought Process**: The `AgentExecutor` sends the query to the LLM. The LLM evaluates available tools based on their descriptions.
3. **Action**: The LLM calls the `wikipedia` tool. The Python function fetches data.
4. **Observation**: The fetched data is stored in the agent's `{agent_scratchpad}` (short-term memory).
5. **Action 2**: The LLM reads the memory, realizes it needs to save the file, and calls the `save_text_to_file` tool.
6. **Final Output**: The LLM formats the final summarized answer to match the strict `Pydantic` schema, which is then parsed and printed beautifully using the `Rich` console.

---

## 🛠️ Setup & Installation

### 1. Prerequisites
* Python `3.10` or higher installed.

### 2. Setup Project & Virtual Environment
```bash
# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate   # Windows
# source venv/bin/activate # macOS / Linux
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the root project directory and add your Hugging Face API Token:
```env
HUGGINGFACEHUB_API_TOKEN=hf_your_secret_api_token_here
```
> **Note**: You can get your free API token from [Hugging Face Settings](https://huggingface.co/settings/tokens).

---

## 🚀 Usage

Run the agent via the command line:
```bash
python main.py
```

### Example Prompt & Execution Loop

**User:**
> What can I help you research? Tell me about quantum computing and save it to a file.

**Output:**
```text
╭──────────────────────── Research Complete ────────────────────────╮
│ Topic: Quantum Computing Overview                                 │
│                                                                   │
│ Summary:                                                          │
│ Quantum computing leverages quantum mechanics principles like     │
│ superposition and entanglement to perform complex calculations... │
│                                                                   │
│ Sources: https://en.wikipedia.org/wiki/Quantum_computing          │
│                                                                   │
│ Tools Used: wiki_tool, save_text_to_file                          │
╰───────────────────────────────────────────────────────────────────╯
```