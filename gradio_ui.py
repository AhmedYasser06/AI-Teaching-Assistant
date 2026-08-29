import gradio as gr
import httpx
import json
from typing import List, Tuple

# API Configuration
API_BASE_URL = "http://127.0.0.1:8000"

# ============================================================
# THEME — light workspace, dark sidebar, teal accent
# ============================================================
professional_theme = gr.themes.Base(
    primary_hue=gr.themes.colors.teal,
    secondary_hue=gr.themes.colors.slate,
    neutral_hue=gr.themes.colors.slate,
    font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "system-ui", "sans-serif"],
    font_mono=[gr.themes.GoogleFont("JetBrains Mono"), "ui-monospace", "Consolas", "monospace"],
).set(
    body_background_fill="#f5f7fa",
    body_background_fill_dark="#f5f7fa",
    body_text_color="#1e293b",
    body_text_color_dark="#1e293b",
    background_fill_primary="#ffffff",
    background_fill_primary_dark="#ffffff",
    background_fill_secondary="#f1f5f9",
    background_fill_secondary_dark="#f1f5f9",

    block_background_fill="#ffffff",
    block_background_fill_dark="#ffffff",
    block_border_color="#e2e8f0",
    block_border_color_dark="#e2e8f0",
    block_label_background_fill="#ffffff",
    block_label_text_color="#475569",
    block_title_text_color="#0f172a",
    block_title_text_weight="600",
    block_shadow="0 1px 2px rgba(15, 23, 42, 0.05)",
    block_radius="10px",

    input_background_fill="#f8fafc",
    input_background_fill_dark="#f8fafc",
    input_border_color="#cbd5e1",
    input_border_color_focus="#0d9488",
    input_placeholder_color="#94a3b8",
    input_radius="8px",

    button_primary_background_fill="linear-gradient(90deg, #0d9488 0%, #0f766e 100%)",
    button_primary_background_fill_hover="linear-gradient(90deg, #0f766e 0%, #115e59 100%)",
    button_primary_text_color="#ffffff",
    button_primary_border_color="#0d9488",
    button_large_radius="8px",
    button_small_radius="8px",

    button_secondary_background_fill="#eef2f6",
    button_secondary_background_fill_hover="#e2e8f0",
    button_secondary_text_color="#334155",
    button_secondary_border_color="#e2e8f0",

    border_color_accent="#0d9488",
    color_accent_soft="#ccfbf1",
    shadow_drop="0 4px 12px rgba(15, 23, 42, 0.06)",
)

# ============================================================
# CSS — sidebar workspace layout
# ============================================================
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

.gradio-container {
    max-width: 1440px !important;
    margin: auto !important;
    background: #f5f7fa !important;
}

/* ---------- App shell ---------- */
.app-shell {
    gap: 0 !important;
}

/* ---------- Sidebar ---------- */
.sidebar {
    background: #f4f6f9 !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 14px !important;
    padding: 22px 16px !important;
    min-height: 760px !important;
    display: flex !important;
    flex-direction: column !important;
}

.brand-title h2 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: #0f172a !important;
    font-weight: 700 !important;
    letter-spacing: -0.01em !important;
    margin-bottom: 2px !important;
}
.brand-tagline p {
    color: #64748b !important;
    font-size: 12.5px !important;
    margin-top: 0 !important;
}

.sidebar-divider {
    border: none !important;
    border-top: 1px solid #e2e8f0 !important;
    margin: 16px 0 !important;
}

.sidebar-label p {
    color: #64748b !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    margin-bottom: 6px !important;
}

.asset-field textarea, .asset-field input {
    background: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    color: #0f172a !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 12.5px !important;
}
.asset-field textarea::placeholder, .asset-field input::placeholder {
    color: #94a3b8 !important;
}

.nav-btn {
    justify-content: flex-start !important;
    text-align: left !important;
    background: transparent !important;
    color: #475569 !important;
    border: none !important;
    box-shadow: none !important;
    font-weight: 500 !important;
    font-size: 14.5px !important;
    padding: 10px 12px !important;
    border-radius: 8px !important;
    margin-bottom: 4px !important;
}
.nav-btn:hover {
    background: #e2e8f0 !important;
    color: #0f172a !important;
}

.sidebar-footer p {
    color: #94a3b8 !important;
    font-size: 11.5px !important;
    line-height: 1.5 !important;
}

/* ---------- Main workspace ---------- */
.main-panel {
    padding: 4px 8px 4px 24px !important;
}

.panel-header h2 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: #0f172a !important;
    font-weight: 700 !important;
    letter-spacing: -0.01em !important;
    margin-bottom: 2px !important;
}
.panel-subtitle p {
    color: #64748b !important;
    font-size: 14px !important;
    margin-top: 0 !important;
}

.panel-card {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 12px !important;
    padding: 18px !important;
}

/* Upload dropzone */
.upload-area {
    border: 2px dashed #cbd5e1 !important;
    border-radius: 12px !important;
    background: #f8fafc !important;
    transition: all 0.2s ease !important;
}
.upload-area:hover {
    border-color: #0d9488 !important;
    background: #f0fdfa !important;
}

/* Status banners */
.status-success {
    background: #f0fdf4 !important;
    border: 1px solid #86efac !important;
    color: #166534 !important;
    padding: 10px 14px !important;
    border-radius: 8px !important;
    font-size: 13.5px !important;
}
.status-error {
    background: #fef2f2 !important;
    border: 1px solid #fca5a5 !important;
    color: #991b1b !important;
    padding: 10px 14px !important;
    border-radius: 8px !important;
    font-size: 13.5px !important;
}

/* Chat */
.chat-container {
    max-height: 480px !important;
    overflow-y: auto !important;
    border-radius: 12px !important;
    background: #ffffff !important;
}

/* Primary action buttons */
.button-primary {
    background: linear-gradient(90deg, #0d9488 0%, #0f766e 100%) !important;
    border: none !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 10px 22px !important;
    font-weight: 600 !important;
    letter-spacing: 0.01em !important;
    transition: all 0.2s ease !important;
}
.button-primary:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 16px rgba(13, 148, 136, 0.35) !important;
}

/* Extracted text panel */
.extracted-text {
    font-family: 'JetBrains Mono', 'Courier New', monospace !important;
    background: #f8fafc !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 10px !important;
    max-height: 600px !important;
    overflow-y: auto !important;
    color: #1e293b !important;
}

.section-label p {
    color: #0f172a !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    margin-bottom: 6px !important;
}

hr { border-color: #e2e8f0 !important; }
"""


class GradioUI:
    def __init__(self):
        self.question_session_state = {}
        self.summary_session_state = {}
        self.qa_session_state = {}    
        
    def upload_file(self, file) -> Tuple[str, str, str]:
        """Upload file and return asset ID, status message, and extracted text"""
        if file is None:
            return "", "❌ Please select a file to upload", ""
        
        try:
            # Set timeout for large file uploads (5 minutes)
            timeout = httpx.Timeout(300.0, connect=60.0)
            
            with httpx.Client(timeout=timeout) as client:
                with open(file.name, "rb") as f:
                    files = {"file": (file.name.split("/")[-1], f, "application/octet-stream")}
                    response = client.post(f"{API_BASE_URL}/upload_file/", files=files)
            
            if response.status_code == 200:
                result = response.json()
                asset_id = result["id"]
                
                # Fetch the extracted text
                extracted_text = self.get_extracted_text(asset_id)
                
                status_msg = f"✅ File uploaded successfully!\n📁 Asset ID: {asset_id}\n📄 File: {file.name.split('/')[-1]}"
                return asset_id, status_msg, extracted_text
            else:
                return "", f"❌ Upload failed: {response.text}", ""
                
        except httpx.TimeoutException:
            return "", "❌ Upload timed out. Please try with a smaller file or check your connection.", ""
        except httpx.ConnectError:
            return "", "❌ Cannot connect to the API server. Please ensure the server is running.", ""
        except Exception as e:
            return "", f"❌ Error uploading file: {str(e)}", ""

    def get_extracted_text(self, asset_id: str) -> str:
        """Retrieve extracted text for a given asset ID"""
        if not asset_id.strip():
            return ""
        
        try:
            timeout = httpx.Timeout(30.0, connect=10.0)
            with httpx.Client(timeout=timeout) as client:
                response = client.get(f"{API_BASE_URL}/get_extracted_text/{asset_id.strip()}")
            
            if response.status_code == 200:
                result = response.json()
                return result.get("extracted_text", "")
            else:
                return f"❌ Failed to retrieve extracted text: {response.text}"
                
        except httpx.TimeoutException:
            return "❌ Request timed out while retrieving extracted text."
        except httpx.ConnectError:
            return "❌ Cannot connect to the API server."
        except Exception as e:
            return f"❌ Error retrieving extracted text: {str(e)}"
        
    def start_question_session(self, asset_id: str, question_type: str) -> Tuple[str, str, str, str, str]:
        """Start a question generation session"""
        if not asset_id.strip():
            return "", "", "", "", "❌ Please enter an Asset ID"
        
        try:
            payload = {"asset_id": asset_id.strip(), "question_type": question_type}
            timeout = httpx.Timeout(60.0, connect=10.0)
            with httpx.Client(timeout=timeout) as client:
                response = client.post(f"{API_BASE_URL}/api/v1/graph/qg/start_session", json=payload)
         
            if response.status_code == 200:
                result = response.json()
                # print(f"Response from question generation: {result}")
                state = result
                self.question_session_state = {
                    "thread_id": state["thread_id"],
                    "asset_id": asset_id.strip(),
                    "question_type": question_type
                }
                
                question = state["data_for_feedback"].get("generated_question", "")
                options = state["data_for_feedback"].get("options", [])
                answer = state["data_for_feedback"].get("answer", "")
                explanation = state["data_for_feedback"].get("explanation", "")

                options_text = "\n".join([f"{opt}" for i, opt in enumerate(options)]) if options else ""
                status = f"✅ Question generated successfully!\n🎯 Type: {question_type}\n🔗 Session ID: {state['thread_id']}..."
                return question, options_text, answer, explanation, status
            else:
                return "", "", "", "", f"❌ Failed to generate question: {response.text}"
                
        except httpx.TimeoutException:
            return "", "", "", "", "❌ Request timed out. Please try again."
        except httpx.ConnectError:
            return "", "", "", "", "❌ Cannot connect to the API server. Please ensure the server is running."       
        except Exception as e:
            return "", "", "", "", f"❌ Error generating question: {str(e)}"
    
    def update_question(self, feedback: str) -> Tuple[str, str, str, str, str]:
        """Update question based on feedback"""
        if not self.question_session_state:
            return "", "", "", "", "❌ No active session. Please start a new session first."
        
        if not feedback.strip():
            return "", "", "", "", "❌ Please provide feedback for the question"
        
        try:
            payload = {
                "thread_id": self.question_session_state["thread_id"],
                "feedback": feedback.strip()
            }
            timeout = httpx.Timeout(60.0, connect=10.0)
            with httpx.Client(timeout=timeout) as client:
                response = client.post(f"{API_BASE_URL}/api/v1/graph/qg/provide_feedback", json=payload)

            if response.status_code == 200:
                result = response.json()
                # print(f"Response from question update: {result}")
                state = result

                question = state["data_for_feedback"].get("generated_question", "")
                options = state["data_for_feedback"].get("options", [])
                answer = state["data_for_feedback"].get("answer", "")
                explanation = state["data_for_feedback"].get("explanation", "")

                options_text = "\n".join([f"{opt}" for i, opt in enumerate(options)]) if options else ""
                status = "✅ Question updated based on your feedback!"
                return question, options_text, answer, explanation, status
            else:
                return "", "", "", "", f"❌ Failed to update question: {response.text}"
                
        except httpx.TimeoutException:
            return "", "", "", "", "❌ Request timed out. Please try again."
        except httpx.ConnectError:
            return "", "", "", "", "❌ Cannot connect to the API server. Please ensure the server is running."
        except Exception as e:
            return "", "", "", "", f"❌ Error updating question: {str(e)}"
    
    def start_summary_session(self, asset_id: str):
        """Start a summary generation session with streaming"""
        if not asset_id.strip():
            return "", "", "❌ Please enter an Asset ID"
        
        try:
            payload = {"asset_id": asset_id.strip()}

            # Use streaming endpoint
            with httpx.Client(timeout=httpx.Timeout(300.0)) as client:
                with client.stream("POST", f"{API_BASE_URL}/api/v1/graph/summarizer/start_session_streaming", json=payload) as response:
                    if response.status_code != 200:
                        return "", "", f"❌ Failed to start summary session: {response.text}"
                    
                    main_points = ""
                    summary = ""
                    thread_id = ""
                    
                    for chunk in response.iter_text():
                        if chunk.strip():
                            if chunk.startswith("data: "):
                                chunk = chunk[6:]  # Remove 'data: ' prefix
                            
                            try:
                                event = json.loads(chunk)

                                if event.get("thread_id"):
                                    thread_id = event["thread_id"]
                                    self.summary_session_state = {
                                        "thread_id": thread_id,
                                        "asset_id": asset_id.strip()
                                    }
                                
                                if event.get("event") == "token" and event.get("status_update") == "main_point_summarizer":
                                    main_points += event["token"]
                                    yield main_points, summary, "🔄 Generating main points..."
                                
                                elif event.get("event") == "token" and event.get("status_update") == "summarizer_writer":
                                    summary += event["token"]
                                    yield main_points, summary, "🔄 Generating detailed summary..."

                            except json.JSONDecodeError as e:
                                print(f"JSON decode error: {e}, chunk: {chunk}")
                                continue

                    status = f"✅ Summary generated successfully!\n🔗 Session ID: {thread_id[:8]}..."
                    yield main_points, summary, status
                
        except Exception as e:
            yield "", "", f"❌ Error generating summary: {str(e)}"

    def update_summary(self, feedback: str):
        """Update summary based on feedback"""
        if not self.summary_session_state:
            yield "", "❌ No active session. Please start a new session first."
            return
        
        if not feedback.strip():
            yield "", "❌ Please provide feedback for the summary"
            return
        
        try:
            payload = {
                "thread_id": self.summary_session_state["thread_id"],
                "feedback": feedback.strip()
            }
            with httpx.Client(timeout=httpx.Timeout(300.0)) as client:
                with client.stream("POST", f"{API_BASE_URL}/api/v1/graph/summarizer/provide_feedback_streaming", json=payload) as response:
                    if response.status_code != 200:
                        yield "", f"❌ Failed to update summary: {response.text}"
                        return
                    summary = ""
                    
                    for chunk in response.iter_text():
                        if chunk.strip():                            
                            if chunk.startswith("data: "):
                                chunk = chunk[6:]
                            try:
                                event = json.loads(chunk)
                                
                                if event.get("event") == "token" and event.get("status_update") == "summarizer_rewriter":
                                    summary += event["token"]
                                    yield summary, "🔄 Updating summary based on feedback..."

                            except json.JSONDecodeError:
                                continue
                    
                    status = "✅ Summary updated based on your feedback!"
                    yield summary, status

        except Exception as e:
            yield "", f"❌ Error updating summary: {str(e)}"

    def start_qa_session_streaming(self, asset_id: str, question: str):
        """Start a Q&A session with streaming response"""
        if not asset_id.strip():
            yield [], "❌ Please enter an Asset ID"
            return
        
        if not question.strip():
            yield [], "❌ Please enter a question"
            return
        
        try:
            payload = {"asset_id": asset_id.strip(), "initial_question": question.strip()}
            
            with httpx.Client(timeout=httpx.Timeout(300.0)) as client:
                with client.stream("POST", f"{API_BASE_URL}/api/v1/graph/qa/start_session_stream", json=payload) as response:
                    if response.status_code != 200:
                        yield [], f"❌ Failed to start Q&A session: {response.text}"
                        return
                    
                    thread_id = ""
                    ai_response = ""
                    for chunk in response.iter_text():
                        if chunk.strip():
                            if chunk.startswith("data: "):
                                chunk = chunk[6:]  # Remove 'data: ' prefix
                            
                            try:
                                event = json.loads(chunk)

                                if event.get("type") == "metadata":
                                    thread_id = event.get("thread_id", "")
                                    self.qa_session_state = {
                                        "thread_id": thread_id,
                                        "asset_id": asset_id.strip()
                                    }
                                    yield [], f"🔄 Starting Q&A session... ID: {thread_id[:8]}..."
                                
                                elif event.get("type") == "token":
                                    ai_response += event.get("content", "")
                                    chat_history = [(question.strip(), ai_response)]
                                    yield chat_history, f"🔄 Generating response..."
                                
                                elif event.get("type") == "complete":
                                    chat_history = [(question.strip(), ai_response)]
                                    yield chat_history, f"✅ Q&A session started! ID: {thread_id[:8]}..."
                                
                                elif event.get("type") == "error":
                                    yield [], f"❌ Error: {event.get('content', 'Unknown error')}"
                                    return
                                    
                            except json.JSONDecodeError:
                                continue

        except Exception as e:
            yield [], f"❌ Error starting Q&A session: {str(e)}"

    def continue_qa_chat_streaming(self, message: str, history: List[Tuple[str, str]]):
        """Continue the Q&A conversation with streaming"""
        if not self.qa_session_state:
            yield history, "❌ No active session. Please start a new session first."
            return
        
        if not message.strip():
            yield history, "❌ Please enter a message"
            return
        
        try:
            payload = {
                "thread_id": self.qa_session_state["thread_id"],
                "next_question": message.strip()
            }
            
            with httpx.Client(timeout=httpx.Timeout(300.0)) as client:
                with client.stream("POST", f"{API_BASE_URL}/api/v1/graph/qa/continue_conversation_stream", json=payload) as response:
                    if response.status_code != 200:
                        yield history, f"❌ Failed to get response: {response.text}"
                        return
                    
                    ai_response = ""
                    for chunk in response.iter_text():
                        if chunk.strip():
                            if chunk.startswith("data: "):
                                chunk = chunk[6:]  # Remove 'data: ' prefix

                            try:
                                event = json.loads(chunk)

                                if event.get("type") == "token":
                                    ai_response += event.get("content", "")
                                    new_history = history + [(message.strip(), ai_response)]
                                    yield new_history, "🔄 Generating response..."
                                
                                elif event.get("type") == "complete":
                                    new_history = history + [(message.strip(), ai_response)]
                                    yield new_history, "✅ Response complete"
                                
                                elif event.get("type") == "error":
                                    yield history, f"❌ Error: {event.get('content', 'Unknown error')}"
                                    return
                                    
                            except json.JSONDecodeError:
                                continue

        except Exception as e:
            yield history, f"❌ Error in conversation: {str(e)}"


# ============================================================
# UI helper — sidebar navigation switches which panel is shown
# ============================================================
NAV_KEYS = ["upload", "questions", "summary", "qa"]


def switch_panel(target: str):
    """Returns visibility updates for the 4 panels plus variant updates
    for the 4 nav buttons, so exactly one panel + one active nav item show."""
    visibility = [gr.update(visible=(target == key)) for key in NAV_KEYS]
    variants = [gr.update(variant=("primary" if target == key else "secondary")) for key in NAV_KEYS]
    return (*visibility, *variants)


def create_gradio_interface():
    ui = GradioUI()

    with gr.Blocks(css=custom_css, title="AI Teaching Assistant", theme=professional_theme) as app:

        with gr.Row(elem_classes="app-shell", equal_height=False):

            # ---------------- Sidebar ----------------
            with gr.Column(scale=1, min_width=260, elem_classes="sidebar"):
                gr.Markdown("## 🎓 AI Teaching Assistant", elem_classes="brand-title")
                gr.Markdown("AI Teaching Assistant", elem_classes="brand-tagline")

                gr.HTML("<hr class='sidebar-divider'>")

                gr.Markdown("Active Document", elem_classes="sidebar-label")
                asset_id_display = gr.Textbox(
                    show_label=False,
                    placeholder="No document loaded yet...",
                    interactive=True,
                    lines=1,
                    elem_classes="asset-field"
                )

                gr.HTML("<hr class='sidebar-divider'>")

                gr.Markdown("Workspace", elem_classes="sidebar-label")
                nav_upload_btn = gr.Button("📤  Upload & Extract", elem_classes="nav-btn", variant="primary")
                nav_questions_btn = gr.Button("❓  Generate Questions", elem_classes="nav-btn", variant="secondary")
                nav_summary_btn = gr.Button("📝  Summarize Content", elem_classes="nav-btn", variant="secondary")
                nav_qa_btn = gr.Button("💬  Ask Questions", elem_classes="nav-btn", variant="secondary")

                gr.HTML("<div style='flex:1'></div>")
                gr.Markdown(
                    "One document, four tools — upload once on the left, "
                    "then switch between question generation, summaries, and chat.",
                    elem_classes="sidebar-footer"
                )

            # ---------------- Main workspace ----------------
            with gr.Column(scale=4, elem_classes="main-panel"):

                # ===== Panel 1: Upload =====
                with gr.Group(visible=True) as group_upload:
                    gr.Markdown("## Upload & Extract", elem_classes="panel-header")
                    gr.Markdown(
                        "Add a PDF, audio, or video file — AI Teaching Assistant extracts the text and hands you an Asset ID for the tools on the left.",
                        elem_classes="panel-subtitle"
                    )

                    with gr.Row():
                        with gr.Column(scale=1):
                            with gr.Group(elem_classes="panel-card"):
                                file_input = gr.File(
                                    label="Select File",
                                    file_types=[".pdf", ".mp3", ".mp4", ".wav", ".avi", ".mov", ".mkv", ".flv"],
                                    elem_classes="upload-area"
                                )
                                upload_btn = gr.Button("🚀 Upload File", variant="primary", elem_classes="button-primary")
                                load_text_btn = gr.Button("📄 Reload Extracted Text", variant="secondary")
                                upload_status = gr.Markdown("📋 Ready to upload files")

                        with gr.Column(scale=2):
                            with gr.Group(elem_classes="panel-card"):
                                extracted_text_display = gr.Textbox(
                                    label="Extracted Text",
                                    placeholder="Extracted text will appear here after upload...",
                                    lines=17,
                                    max_lines=22,
                                    interactive=False,
                                    show_copy_button=True,
                                    elem_classes="extracted-text"
                                )

                # ===== Panel 2: Question Generation =====
                with gr.Group(visible=False) as group_questions:
                    gr.Markdown("## Generate Questions", elem_classes="panel-header")
                    gr.Markdown(
                        "Create MCQ or True/False questions from the active document, and refine them with feedback.",
                        elem_classes="panel-subtitle"
                    )

                    with gr.Row():
                        with gr.Column(scale=1):
                            with gr.Group(elem_classes="panel-card"):
                                question_type = gr.Radio(
                                    choices=["T/F", "MCQ"],
                                    label="Question Type",
                                    value="MCQ"
                                )
                                generate_q_btn = gr.Button("🎯 Generate Question", variant="primary", elem_classes="button-primary")
                                feedback_input = gr.Textbox(
                                    label="Feedback",
                                    placeholder="Provide feedback to improve the question...",
                                    lines=3
                                )
                                update_q_btn = gr.Button("🔄 Update Question", variant="secondary")
                                q_status = gr.Markdown("📋 Ready to generate questions")

                        with gr.Column(scale=2):
                            with gr.Group(elem_classes="panel-card"):
                                question_display = gr.Textbox(label="Generated Question", lines=3, interactive=False)
                                options_display = gr.Textbox(label="Answer Options", lines=4, interactive=False)
                                answer_display = gr.Textbox(label="Correct Answer", lines=1, interactive=False)
                                explanation_display = gr.Textbox(label="Explanation", lines=3, interactive=False)

                # ===== Panel 3: Summarization =====
                with gr.Group(visible=False) as group_summary:
                    gr.Markdown("## Summarize Content", elem_classes="panel-header")
                    gr.Markdown(
                        "Generate key points and a detailed summary of the active document, then refine with feedback.",
                        elem_classes="panel-subtitle"
                    )

                    with gr.Row():
                        with gr.Column(scale=1):
                            with gr.Group(elem_classes="panel-card"):
                                generate_s_btn = gr.Button("📊 Generate Summary", variant="primary", elem_classes="button-primary")
                                summary_feedback = gr.Textbox(
                                    label="Feedback",
                                    placeholder="Provide feedback to improve the summary...",
                                    lines=3
                                )
                                update_s_btn = gr.Button("🔄 Update Summary", variant="secondary")
                                s_status = gr.Markdown("📋 Ready to generate summaries")

                        with gr.Column(scale=2):
                            with gr.Group(elem_classes="panel-card"):
                                main_points_display = gr.Textbox(label="Main Points", lines=6, interactive=False)
                                summary_display = gr.Textbox(label="Detailed Summary", lines=9, interactive=False)

                # ===== Panel 4: Question Answering =====
                with gr.Group(visible=False) as group_qa:
                    gr.Markdown("## Ask Questions", elem_classes="panel-header")
                    gr.Markdown(
                        "Have a running conversation about the active document.",
                        elem_classes="panel-subtitle"
                    )

                    with gr.Group(elem_classes="panel-card"):
                        initial_question = gr.Textbox(
                            label="Ask a question about the active document",
                            placeholder="e.g. What are the main takeaways from chapter 2?",
                            lines=2
                        )
                        start_qa_btn = gr.Button("🚀 Start Q&A Session", variant="primary", elem_classes="button-primary")
                        qa_status = gr.Markdown("📋 Ready to start Q&A session")

                        chatbot = gr.Chatbot(label="Conversation", height=380, elem_classes="chat-container")

                        with gr.Row():
                            msg_input = gr.Textbox(
                                label="Your Message",
                                placeholder="Continue the conversation...",
                                lines=1,
                                scale=4
                            )
                            send_btn = gr.Button("📤 Send", variant="secondary", scale=1)

        # ================= Sidebar navigation wiring =================
        nav_outputs = [group_upload, group_questions, group_summary, group_qa,
                       nav_upload_btn, nav_questions_btn, nav_summary_btn, nav_qa_btn]

        nav_upload_btn.click(fn=lambda: switch_panel("upload"), outputs=nav_outputs)
        nav_questions_btn.click(fn=lambda: switch_panel("questions"), outputs=nav_outputs)
        nav_summary_btn.click(fn=lambda: switch_panel("summary"), outputs=nav_outputs)
        nav_qa_btn.click(fn=lambda: switch_panel("qa"), outputs=nav_outputs)

        # ================= Feature wiring (logic untouched) =================
        # Upload
        upload_btn.click(
            fn=ui.upload_file,
            inputs=[file_input],
            outputs=[asset_id_display, upload_status, extracted_text_display]
        )

        load_text_btn.click(
            fn=lambda asset_id: ("", ui.get_extracted_text(asset_id)) if asset_id.strip() else ("❌ Please enter an Asset ID", ""),
            inputs=[asset_id_display],
            outputs=[upload_status, extracted_text_display]
        )

        # Question generation — shares asset_id_display from the sidebar
        generate_q_btn.click(
            fn=ui.start_question_session,
            inputs=[asset_id_display, question_type],
            outputs=[question_display, options_display, answer_display, explanation_display, q_status]
        )

        update_q_btn.click(
            fn=ui.update_question,
            inputs=[feedback_input],
            outputs=[question_display, options_display, answer_display, explanation_display, q_status]
        )

        # Summarization — shares asset_id_display from the sidebar
        generate_s_btn.click(
            fn=ui.start_summary_session,
            inputs=[asset_id_display],
            outputs=[main_points_display, summary_display, s_status]
        )

        update_s_btn.click(
            fn=ui.update_summary,
            inputs=[summary_feedback],
            outputs=[summary_display, s_status]
        )

        # Q&A — shares asset_id_display from the sidebar
        start_qa_btn.click(
            fn=ui.start_qa_session_streaming,
            inputs=[asset_id_display, initial_question],
            outputs=[chatbot, qa_status]
        )

        send_btn.click(
            fn=ui.continue_qa_chat_streaming,
            inputs=[msg_input, chatbot],
            outputs=[chatbot, qa_status]
        ).then(
            lambda: "",
            outputs=[msg_input]
        )

        msg_input.submit(
            fn=ui.continue_qa_chat_streaming,
            inputs=[msg_input, chatbot],
            outputs=[chatbot, qa_status]
        ).then(
            lambda: "",
            outputs=[msg_input]
        )

    return app


if __name__ == "__main__":
    app = create_gradio_interface()
    app.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        show_error=True
    )
