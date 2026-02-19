# 🤖 AGENT-AI — Learning Agentic AI Basics

> A hands-on, day-by-day journey into building AI agents with the **Google Gemini API**.  
> Each file is a self-contained experiment that adds one new concept on top of the last.

---

## 📖 What Is This?

This repo is a **progressive learning log** for understanding how AI agents work from the ground up.  
Instead of jumping straight into frameworks, every concept is built from scratch in plain Python so you can see exactly what's happening under the hood.

The goal is simple: start with a raw LLM call, and gradually build up toward an agent that can reason, choose tools, and take actions.

---

## 🗂️ Project Structure

```
AGENT-AI/
├── get_client.py           # Shared Google Gemini client (used by all day files)
├── check_models.py         # Utility — lists all available Gemini models
│
├── day1_llm_test.py        # Day 1 — First LLM call
├── day2_chatbot.py         # Day 2 — Multi-turn chatbot with memory
├── day3_tool_agent.py      # Day 3 — Agent with a regex-based tool router
├── day4_model_tool_agent.py# Day 4 — Model-driven tool routing via JSON + system prompt
│
├── .env.example            # Template for your API key
├── .env                    # Your actual API key (git-ignored)
└── .gitignore
```

---

## 📅 Day-by-Day Breakdown

### Day 1 — `day1_llm_test.py`: First LLM Call
The simplest possible Gemini API call. Sends a single prompt and prints the response.

**Concept learned:** How to connect to the Gemini API and get a text response.

---

### Day 2 — `day2_chatbot.py`: Multi-turn Chatbot
Adds a `chat_history` list that grows with every exchange, giving the model memory of the conversation.

**Concept learned:** How LLMs maintain context — not magic, just a growing list of messages sent each time.

---

### Day 3 — `day3_tool_agent.py`: Rule-based Tool Agent
Introduces a **calculator tool**. A regex check decides whether to call the calculator or the LLM. The agent routes the request — it just uses a hard-coded rule to do it.

**Concept learned:** The tool-use loop: detect intent → call tool → return result.

---

### Day 4 — `day4_model_tool_agent.py`: Model-driven Tool Routing
The model itself decides whether to use the calculator. A **system prompt** instructs it to respond in JSON (`{ "action": "calculator", "input": "..." }` or `{ "action": "none", ... }`). The code then reads that JSON and acts accordingly.

**Concept learned:** Using the LLM as a router/planner — the foundation of real agentic systems.

---

### Helpers

| File | Purpose |
|---|---|
| `get_client.py` | Creates a shared `genai.Client` from your `.env` API key. Imported by all day files. |
| `check_models.py` | Quick utility to list every model available on your API key. Handy when picking a model name. |

---

## ⚙️ Setup

### 1. Clone the repo

```bash
git clone https://github.com/abinesh-t/AGENT-AI.git
cd AGENT-AI
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your API key

```bash
cp .env.example .env
```

Open `.env` and replace `YOUR_API_KEY` with your actual [Google AI Studio API key](https://aistudio.google.com/app/apikey):

```
API_KEY=your_real_api_key_here
```

### 5. (Optional) Check which models you can access

```bash
python check_models.py
```

---

## 🚀 Run Each Day

```bash
python day1_llm_test.py        # Single prompt → response
python day2_chatbot.py         # Interactive chat (type 'quit' to exit)
python day3_tool_agent.py      # Tool agent (type 'exit' to quit)
python day4_model_tool_agent.py# Model-driven agent (type 'exit' to quit)
```

---

## 🧭 How to Adapt This for Your Own Learning

This repo is designed to be **forked and extended**. Here's how to make it yours:

### Follow the same day-by-day pattern
Each day introduces **one new concept only**. Keep your files small and focused. If a day file is getting long, you've probably packed too much in — split it.


### Tips
- **Keep the `get_client.py` pattern** — one shared client file avoids repeating boilerplate.
- **Commit after each day** — your git history becomes a learning log you can revisit.
- **Read the raw responses** — print `response.text` before parsing it. Understanding what the model actually outputs makes debugging much easier.
- **Intentionally break things** — remove the system prompt in Day 4, see what happens. Experimentation is the fastest way to learn.

---

## 🛠️ Requirements

- Python 3.9+
- A [Google AI Studio](https://aistudio.google.com/app/apikey) API key (free tier available)
- `google-genai` SDK
- `python-dotenv`

---

## 📄 License

MIT — use this however you like, learn from it, improve on it.

---

*Learning in public. One agent concept at a time.*
