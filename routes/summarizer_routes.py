import uuid
import os
from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import StreamingResponse 
from typing import AsyncGenerator
import json

from controllers.GraphState import SummaryGenState
from controllers.SummarizerGenGraphController import stream_summarizer_graph as summarizer_graph
from langgraph.types import Command

router = APIRouter()

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_BASE_PATH = os.path.join(PROJECT_ROOT, "assets")

@router.post("/start_session_streaming")
async def start_summarization_session_streaming(asset_id: str = Body(..., embed=True)) -> StreamingResponse:
    """
    Starts a new summarization session for a given asset_id and streams graph events.
    This endpoint will stream JSON objects representing events from the graph execution.
    """
    thread_id = str(uuid.uuid4())
    context_file_path = os.path.join(ASSETS_BASE_PATH, asset_id, "extracted_text.txt")

    if not os.path.exists(context_file_path):
        raise HTTPException(status_code=404, detail=f"Asset text file not found for id: {asset_id}")

    try:
        with open(context_file_path, "r", encoding="utf-8") as f:
            context = f.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read context file: {str(e)}")

    initial_state = SummaryGenState(
        context=context,
        summary="",
        old_summary="",
        feedback="",
        Main_Points=""
    )

    config = {"configurable": {"thread_id": thread_id}}

    async def event_stream() -> AsyncGenerator[str, None]:

        global_events = ["main_point_summarizer", "summarizer_writer", "summarizer_rewriter"]
        initial_payload = {"thread_id": str(thread_id), "status": "starting_session"} 
        yield f'data: {json.dumps(initial_payload)}\n\n'
        try:
            # NOTE: switched from astream_events(..., version="v2") to plain astream(..., stream_mode="messages")
            # astream_events() combined with interrupt() raises:
            #   RuntimeError: Called get_config outside of a runnable context
            # (a known LangGraph bug: https://github.com/langchain-ai/langgraph/issues/2942)
            # astream(stream_mode="messages") still gives token-level streaming and doesn't hit this bug.
            async for msg, metadata in summarizer_graph.astream(initial_state, config=config, stream_mode="messages"):
                node_name = metadata.get("langgraph_node", "") if isinstance(metadata, dict) else ""

                if node_name in global_events and hasattr(msg, "content") and msg.content:
                    payload_to_yield = {
                        "event": "token",
                        "name": node_name,
                        "thread_id": thread_id,
                        "token": msg.content,
                        "status_update": node_name,
                    }
                    yield f'data: {json.dumps(payload_to_yield)}\n\n'
                # elif event_type == "on_chain_end":
                #     payload_to_yield["status_update"] = f"Finished: {event_name}"
                #     payload_to_yield["data"] = event_data.get("output")
            
                #     if event_name == "main_point_summarizer" and event_data.get("output") and "Main_Points" in event_data["output"] :
                #         payload_to_yield["main_points"] = event_data["output"]["Main_Points"]                  
                #         print(f"Main Points: {payload_to_yield['main_points']}\n") # Debugging output
                #         yield f'data: {json.dumps(payload_to_yield)}\n\n'
                #     elif event_name == "summarizer_writer" and event_data.get("output") and "summary" in event_data["output"]:
                #         payload_to_yield["summary"] = event_data["output"]["summary"]
                #         print(f"Summary: {payload_to_yield['summary']}\n") # Debugging output
                #         yield f'data: {json.dumps(payload_to_yield)}\n\n'
                #     elif event_name == "summarizer_rewriter" and event_data.get("output") and "summary" in event_data["output"]:
                #         payload_to_yield["summary"] = event_data["output"]["summary"]
                #         payload_to_yield["old_summary"] = event_data["output"].get("old_summary", "")
                #         print(f"Rewritten Summary: {payload_to_yield['summary']}\n") # Debugging output
                #         yield f'data: {json.dumps(payload_to_yield)}\n\n'
                 
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            error_message = f"Error in summarization stream: {str(e)}"
            print(f"Error details: {error_details}")
            yield f'data: {json.dumps({"event": "error", "thread_id": thread_id, "detail": error_message, "error_type": e.__class__.__name__})}\n\n'
        
        finally:
            payload = {"event": "stream_end", "thread_id": str(thread_id), "status_update": "Stream ended"}
            yield f'data: {json.dumps(payload)}\n\n'

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@router.post("/provide_feedback_streaming")
async def provide_feedback_to_summarization_streaming(
    thread_id: str = Body(..., embed=True),
    feedback: str = Body(..., embed=True)
) -> StreamingResponse:
    config = {"configurable": {"thread_id": thread_id}}

    # print(f"Received feedback: {feedback} for thread: {thread_id}")

    async def event_stream() -> AsyncGenerator[str, None]:
        global_events = ["summarizer_rewriter"]
        initial_payload = {"thread_id": thread_id, "status": "resuming_with_feedback"} 
        yield f'data: {json.dumps(initial_payload)}\n\n'
        try:
            # NOTE: switched from astream_events(..., version="v2") to plain astream(..., stream_mode="messages")
            # for the same reason as start_session_streaming above (avoids the interrupt()+astream_events bug).
            resume_command = Command(resume=feedback)
            async for msg, metadata in summarizer_graph.astream(resume_command, config=config, stream_mode="messages"):
                node_name = metadata.get("langgraph_node", "") if isinstance(metadata, dict) else ""

                if node_name in global_events and hasattr(msg, "content") and msg.content:
                    payload_to_yield = {
                        "event": "token",
                        "name": node_name,
                        "thread_id": thread_id,
                        "token": msg.content,
                        "status_update": node_name,
                    }
                    yield f'data: {json.dumps(payload_to_yield)}\n\n'
        
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            error_message = f"Error in feedback stream: {str(e)}"

            print(f"Error details: {error_details}")
            yield f'data: {json.dumps({"event": "error", "thread_id": thread_id, "detail": error_message,"error_type": e.__class__.__name__})}\n\n'
        
        finally:
            payload = {"event": "stream_end", "thread_id": thread_id, "status_update": "Stream ended"}
            yield f'data: {json.dumps(payload)}\n\n'

    return StreamingResponse(event_stream(), media_type="text/event-stream")
