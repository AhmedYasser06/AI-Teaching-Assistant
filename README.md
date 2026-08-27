# Teaching Assistance — Team Task Breakdown

**Dependency order:** Person 3 (ingestion) and Person 4 (prompts/LLM config) can start immediately — no dependencies. You (graphs) depend on their output shapes but can build against mocked text/prompts first. Person 2 (API) depends on your graphs existing, so they start by studying + stubbing routes, then wire up once your graphs compile.

---

## 🧑‍💼 (Team Lead)

**The hardest part of the project. This is the actual "agentic AI" — everyone else's code plugs into what you build.**

### Files you own

```
controllers/GraphState.py
controllers/QuestionGenGraphController.py
controllers/SummarizerGenGraphController.py
controllers/QuestionAnswerGraphController.py
```

### What's actually hard here

1. **LangGraph state machines** — `StateGraph`, `add_conditional_edges`, `START`/`END`. You're not writing one function, you're wiring a directed graph where the _router functions_ (`Router`, `on_topic_router`) decide the next node at runtime based on state.
2. **Human-in-the-loop interrupts** — `interrupt()` pauses graph execution mid-run and returns control to the caller; `Command(resume=feedback)` resumes it later from a _different HTTP request_. This only works because of `MemorySaver` checkpointing state against a `thread_id`. Understanding why a Python generator can "pause" across two separate API calls is the single hardest concept in this repo.
3. **RAG retrieval** (inside `QuestionAnswerGraphController.py`) — chunking context with `text_splitter`, embedding it, building an ephemeral `Chroma` vectorstore per request, retrieving with MMR search, then grading relevance with a structured-output LLM call (`GradeQuestion`) before deciding to answer or reject as off-topic.
4. **Sync vs. streaming duals** — every graph has two versions: a plain `.invoke()` graph and an `astream_events()` graph (`qa_graph` vs `stream_qa_graph`). You need to understand _why_ streaming needs `async def` generator nodes (`generate_answer_streaming`) while the non-streaming ones don't.

### Concepts to study (in order)

1. Finite state machines / directed graphs — conceptual warm-up, 30 min.
2. LangGraph basics: `StateGraph`, nodes, edges, conditional edges → [LangGraph docs](https://langchain-ai.github.io/langgraph/)
3. LangGraph `interrupt()` + `Command(resume=...)` + checkpointers (this is the core trick — read the "human-in-the-loop" LangGraph guide specifically)
4. Embeddings & semantic search — what a vector is, cosine similarity, why MMR (Maximal Marginal Relevance) reduces redundant retrieved chunks
5. Python `async`/`await` and `async generator` (`yield` inside `async def`) — needed to read `generate_answer_streaming`
6. `TypedDict` for typed state passed between nodes

### What you'll build/verify

- [ ] Trace all 3 graphs by hand on paper before touching code — draw the node/edge diagram from `README.md` and confirm it matches the `add_edge`/`add_conditional_edges` calls
- [ ] Get `qg_graph` running standalone with a hardcoded `context` string and print the interrupt payload
- [ ] Get `stream_qa_graph` running and manually print each event from `astream_events` to see the event stream shape Person 2 will need to parse
- [ ] Own integration: once Person 3 and Person 4's pieces exist, wire them into your graphs and confirm the full pipeline runs end-to-end locally before Person 2 builds routes on top

---

## 🧑‍💻 Person 2 — Backend API, Streaming & UI

**Medium difficulty. No LangGraph internals needed — you call the graphs as black boxes and expose them over HTTP.**

### Files you own

```
main.py
routes/question_gen_routes.py
routes/summarizer_routes.py
routes/qa_routes.py
gradio_ui.py                     (mostly repetitive UI boilerplate)
```

### What you're actually doing

- Each route reads an `asset_id`, loads its extracted text file, builds the graph's `initial_state`, calls `.invoke()` or `.astream_events()`, and formats the result as JSON or as a `text/event-stream`.
- `gradio_ui.py` is a **pure REST client** — it only talks to your own routes over `httpx`, never touches LangGraph directly. You can build this from the API contract in `README.md` alone.

### Concepts to study

1. FastAPI basics: path/query/body params, `APIRouter`, dependency wiring in `main.py`
2. What Server-Sent Events (SSE) are and why `StreamingResponse` + `text/event-stream` is used instead of a normal JSON response — read the "Streaming Response Events" examples in `README.md`
3. `thread_id` / session pattern — how a stateless HTTP API can resume a paused LangGraph session (you don't need to understand _how_ the graph pauses, just that `thread_id` is your session key)
4. Gradio `Blocks`, `Tab`, `Row`/`Column` layout basics
5. Basic `httpx` client usage (sync + the timeout patterns already used in the file)

### What you'll build/verify

- [ ] Test every endpoint in `README.md`'s API docs with `curl` or the FastAPI `/docs` Swagger UI before wiring the Gradio UI to it
- [ ] Confirm the SSE responses actually stream token-by-token (not buffered) — you'll see this live in the terminal
- [ ] Build/verify all 4 Gradio tabs: Upload → Question Generation → Summarization → Q&A chat
- [ ] Handle the "resume with feedback" pattern in the UI (send `'save'` to finish, anything else to refine)

---

## 🧑‍🔧 Person 3 — Content Ingestion Pipeline

**Simple, fully isolated. Nobody else's code needs to change if you get this working correctly.**

### Files you own

```
tools/pdf_extractor_tool.py
tools/transcript_tool.py
helper/text_splitter.py
routes/file_processing_routes.py
```

### What you're actually doing

- Turning an uploaded PDF/audio/video file into a plain `.txt` file that everyone else's code reads as `context`.
- PDF → `PyMuPDFLoader` extracts text per page.
- Audio/video → OpenAI **Whisper** (`tiny` model) transcribes it to text. This needs FFmpeg installed on the system (Whisper uses it under the hood to decode audio).
- Long text later gets split into overlapping chunks (`text_splitter.py`) for the RAG step in Person 1's Q&A graph — you don't need to call this yourself, just know it consumes your output.

### Concepts to study

1. What a PDF text extraction library does (no need to learn the internals — just the input/output contract: file path in, `Document` list out)
2. What Whisper is at a high level (speech-to-text model) and why FFmpeg is a prerequisite dependency, not a Python package
3. Why text gets "chunked" for LLMs — context window limits + retrieval granularity (a light read, not deep RAG theory — that's the Lead's job)
4. FastAPI file uploads: `UploadFile`, `multipart/form-data`

### What you'll build/verify

- [ ] Upload a real PDF and confirm `extracted_text.txt` looks clean (no garbled encoding, no missing pages)
- [ ] Upload a short `.mp3`/`.mp4` and confirm Whisper transcription is reasonably accurate — note the `tiny` model is fast but not the most accurate; flag to the team if quality is too low and a bigger model is worth the tradeoff
- [ ] Confirm all listed formats work: PDF, MP3, WAV, MP4, AVI, MOV, MKV, FLV
- [ ] Add basic error handling notes for corrupted/unsupported files (there's already a cleanup-on-failure pattern in the route — study why `shutil.rmtree` runs in the `except` block)

---

## ✍️ Person 4 — Prompt Engineering & LLM Configuration

**Simple, self-contained, and arguably the most fun — you're not writing complex logic, you're writing and tuning the actual "AI" instructions.**

### Files you own

```
chains/QuestionGenChain.py
chains/QuestionRefinerChain.py
chains/QuestionRewriterChain.py
chains/SummarizerMainPointChain.py
chains/SummarizerGenChain.py
chains/SummarizerRewriterChain.py
chains/GradeQuestionChain.py
chains/schemes/QuestionSchem.py
llm/LLMProviderFactory.py
llm/EmbeddingProviderFactory.py
llm/Enums.py
helper/Config.py
```

### What you're actually doing

- Each "chain" is a **prompt template + few-shot examples** piped into an LLM call (`prompt | llm`). You're writing the system instructions and example Q&A pairs that shape how good the generated questions/summaries are — this is pure prompt engineering, no algorithmic complexity.
- `QuestionSchem.py` defines **structured output schemas** (Pydantic models) so the LLM's response comes back as clean typed fields (`question`, `options`, `answer`) instead of raw text you'd have to parse yourself.
- `LLMProviderFactory` / `EmbeddingProviderFactory` are simple **factory pattern** switches — given a provider name string (`"OLLAMA"`, `"GROQ"`, `"GOOGLE_GENAI"`), return the right LangChain client object.
- `Config.py` loads all model names/providers/temperatures from a `.env` file — you'll set this up once for the whole team.

### Concepts to study

1. Prompt engineering basics: system prompts, few-shot examples, output format instructions
2. Pydantic models + LangChain's `with_structured_output()` — how a schema forces the LLM into valid, parseable output
3. The factory design pattern (just enough to read 15-line files, not a deep OOP dive)
4. `.env` files and why secrets/config are kept out of code (`pydantic_settings.BaseSettings`)
5. Temperature — what it does to LLM output (skim, not deep math)

### What you'll build/verify

- [ ] Set up the shared `.env` file from `.env.example` and get `ollama pull qwen3:4b` running locally so the whole team has a working default LLM without needing paid API keys
- [ ] Read each chain's system prompt and few-shot examples critically — try a few sample transcripts and see if generated questions/summaries are actually good; tune wording if not
- [ ] Confirm `GradeQuestionChain.py`'s relevance grading (used in the Lead's Q&A graph) reliably says "yes"/"no" for on-topic vs. off-topic test questions
- [ ] Document which provider (Ollama/Groq/Google) each agent role is configured to use, and why (cost/speed/quality tradeoffs) — a short note for the mentor review

---

## Suggested week-1 milestone

| Owner    | Deliverable                                                                                    |
| -------- | ---------------------------------------------------------------------------------------------- |
| Person 3 | Upload endpoint returns clean extracted text for all 8 file formats                            |
| Person 4 | `.env` configured, all chains callable standalone with a sample transcript                     |
| (Lead)   | All 3 graphs run standalone via `.invoke()` with hardcoded state, interrupts confirmed working |
| Person 2 | Swagger `/docs` shows all routes; Gradio shell renders all 4 tabs (not yet wired)              |

Once those land, wire top-to-bottom: Upload → Graph → Route → UI.
