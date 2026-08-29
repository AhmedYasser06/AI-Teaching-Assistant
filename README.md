# Project Name

AI-powered teaching assistant that transforms video lectures into quizzes and summaries helping course creators accelerate content creation and boost learner engagement.

## 🚀 Overview

This project is built with a modular architecture that separates concerns across routing, LLM logic, chain orchestration, and supporting utilities. It exposes both an API (via `main.py`) and a UI (via `gradio_ui.py`).

## 📁 Project Structure

```
.
├── chains/          # LLM chain definitions and orchestration logic
├── controllers/      # Business logic connecting routes to services
├── helper/           # Shared utility/helper functions
├── llm/               # LLM client setup, prompts, and configuration
├── routes/            # API route/endpoint definitions
├── tools/             # Custom tools used by chains/agents
├── .env.example       # Example environment variables
├── .gitignore
├── gradio_ui.py        # Gradio-based front-end UI
├── main.py             # Application entry point
├── requirements.txt
└── README.md
```

## ⚙️ Setup

```bash
# Clone the repo
git clone https://github.com/AhmedYasser06/AI-Teaching-Assistant.git
cd AI-Teaching-Assistant

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# then fill in your API keys / config values

# Run the app
python main.py

# Or run the Gradio UI
python gradio_ui.py
```

## 👥 Team Responsibilities

The project is divided into four ownership areas so each contributor has a clear, self-contained scope.

### 1️⃣ Controllers & Routes — *API Layer*
**Folders:** `controllers/`, `routes/`

Responsible for:
- Defining API endpoints and request/response schemas
- Routing incoming requests to the correct controller logic
- Input validation, error handling, and status codes
- Connecting the API layer to the LLM/chains layer (without owning their internals)

### 2️⃣ LLM — *Model Layer*
**Folder:** `llm/`

Responsible for:
- LLM client configuration (model selection, API keys, providers)
- Prompt templates and prompt engineering
- Token/context management and model-specific settings
- Abstracting the LLM provider so chains can call it consistently

### 3️⃣ Chains — *Orchestration Layer*
**Folder:** `chains/`

Responsible for:
- Building and composing chains (sequential, conditional, agent-based, etc.)
- Wiring together LLM calls, tools, and helpers into end-to-end workflows
- Managing chain-level state/memory
- Testing chain outputs for correctness and consistency

### 4️⃣ Helper, Tools & Gradio UI — *Support & Interface Layer*
**Folders:** `helper/`, `tools/`, `gradio_ui.py`

Responsible for:
- Shared/reusable utility functions used across the codebase
- Custom tools exposed to chains/agents (e.g., search, calculators, external API calls)
- Building and maintaining the Gradio UI for demoing/testing the app
- Ensuring the UI stays in sync with backend changes

## 🔗 How the Pieces Fit Together

```
User → Gradio UI / API Routes → Controllers → Chains → LLM
                                       ↑           ↑
                                    Helpers ←──── Tools
```

## 📋 Contributing

1. Create a feature branch from `main`
2. Work within your assigned folder(s) — keep changes to other areas as pull requests reviewed by their owner
3. Update `requirements.txt` if you add new dependencies
4. Open a PR with a clear description of your changes

## 📄 License

Add your license here.

