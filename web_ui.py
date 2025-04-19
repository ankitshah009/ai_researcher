"""Simple web UI for the AI Research Agent using Gradio."""
import os
import time
import argparse
import threading
import queue
from pathlib import Path
from typing import Iterator, Dict, Any, Optional, List

import gradio as gr
from dotenv import load_dotenv
from vertexai.preview.reasoning_engines import AdkApp

from agents.coordinator import coordinator_agent
from config import get_config, load_config_from_file

# Load environment variables
load_dotenv()

# Load configuration
config = load_config_from_file()

# Create outputs directory if it doesn't exist
output_dir = Path(config["output"]["output_dir"])
output_dir.mkdir(exist_ok=True, parents=True)

# Message queue for communication between threads
message_queue = queue.Queue()

def generate_research_paper(topic: str, 
                           output_filename: str = None, 
                           status_callback = None) -> Iterator[Dict[str, Any]]:
    """
    Generate a research paper on the given topic.
    
    Args:
        topic: Research topic
        output_filename: Name of the output file
        status_callback: Function to call with status updates
    
    Yields:
        Status update messages
    """
    if output_filename is None:
        output_filename = config["output"]["default_pdf_name"]
    
    # Full path to output file
    output_path = output_dir / output_filename
    
    # Initialize the app
    app = AdkApp(agent=coordinator_agent)
    
    # Update status
    if status_callback:
        status_callback(f"Starting research on: {topic}")
    
    # Stream output
    try:
        for event in app.stream_query(
            user_id="WEB_UI_USER", 
            message=f"{topic} Output filename: {output_filename}"
        ):
            if event.content and event.content.parts:
                first_part = event.content.parts[0]
                if isinstance(first_part, dict) and "text" in first_part:
                    text = first_part["text"]
                    if status_callback:
                        status_callback(text)
                    yield {"message": text, "complete": False}
                elif hasattr(first_part, 'text'):
                    text = first_part.text
                    if status_callback:
                        status_callback(text)
                    yield {"message": text, "complete": False}
    
        # Final status update
        final_message = f"Research paper generation complete! Check {output_path} for the result."
        if status_callback:
            status_callback(final_message)
        yield {"message": final_message, "complete": True, "file_path": str(output_path)}
    
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        if status_callback:
            status_callback(error_msg)
        yield {"message": error_msg, "complete": True, "error": True}

def worker_thread(topic: str, output_filename: str):
    """Background worker thread to process research paper generation."""
    for update in generate_research_paper(topic, output_filename):
        message_queue.put(update)
    
    # Signal completion
    message_queue.put(None)

def create_ui() -> gr.Blocks:
    """Create the Gradio web UI."""
    with gr.Blocks(title="AI Research Agent") as ui:
        gr.Markdown("# AI Research Agent")
        gr.Markdown("Generate academic research papers from a single topic using Google's Agent Development Kit (ADK)")
        
        with gr.Row():
            with gr.Column(scale=3):
                topic_input = gr.Textbox(
                    label="Research Topic",
                    placeholder="Enter a research topic (e.g., 'Graph Neural Networks for Protein Folding')",
                    lines=2
                )
            
            with gr.Column(scale=1):
                output_filename = gr.Textbox(
                    label="Output Filename",
                    placeholder="research_paper.pdf",
                    value="research_paper.pdf"
                )
        
        with gr.Row():
            submit_button = gr.Button("Generate Research Paper", variant="primary")
            cancel_button = gr.Button("Cancel", variant="secondary")
            cancel_button.visible = False
        
        # Output area
        output_area = gr.Markdown("Results will appear here")
        status_box = gr.Textbox(label="Status", lines=10, max_lines=15)
        file_output = gr.File(label="Generated PDF")
        
        # State variables
        is_generating = gr.State(False)
        thread_ref = gr.State(None)

        def start_generation(topic, filename, state):
            """Start the paper generation process."""
            if state:
                return {
                    output_area: "Generation already in progress. Please wait or cancel.",
                    status_box: "Generation already in progress.",
                    is_generating: True,
                    submit_button: gr.Button.update(interactive=False),
                    cancel_button: gr.Button.update(visible=True)
                }
            
            if not topic.strip():
                return {
                    output_area: "Please enter a research topic.",
                    status_box: "Error: Missing research topic.",
                    is_generating: False
                }
            
            # Clear previous output
            status_box.value = ""
            output_area.value = f"Generating research paper on: **{topic}**\n\nThis may take several minutes..."
            
            # Start worker thread
            thread = threading.Thread(
                target=worker_thread,
                args=(topic, filename),
                daemon=True
            )
            thread.start()
            
            return {
                is_generating: True,
                thread_ref: thread,
                submit_button: gr.Button.update(interactive=False),
                cancel_button: gr.Button.update(visible=True)
            }
        
        def check_progress(state, thread):
            """Check for progress updates from the worker thread."""
            if not state or thread is None:
                return {}
            
            updates = {}
            new_messages = []
            
            # Process all available messages
            try:
                while True:
                    msg = message_queue.get_nowait()
                    if msg is None:  # End signal
                        updates = {
                            is_generating: False,
                            thread_ref: None,
                            submit_button: gr.Button.update(interactive=True),
                            cancel_button: gr.Button.update(visible=False)
                        }
                        break
                    
                    new_messages.append(msg["message"])
                    
                    if msg.get("complete", False):
                        if not msg.get("error", False) and "file_path" in msg:
                            updates = {
                                file_output: msg["file_path"],
                                output_area: f"✅ **Generation Complete!**\n\n{msg['message']}",
                                is_generating: False,
                                thread_ref: None,
                                submit_button: gr.Button.update(interactive=True),
                                cancel_button: gr.Button.update(visible=False)
                            }
                        else:
                            updates = {
                                output_area: f"❌ **Error**\n\n{msg['message']}",
                                is_generating: False,
                                thread_ref: None,
                                submit_button: gr.Button.update(interactive=True),
                                cancel_button: gr.Button.update(visible=False)
                            }
            except queue.Empty:
                pass
            
            if new_messages:
                current_text = status_box.value
                if current_text:
                    status_box.value = current_text + "\n" + "\n".join(new_messages)
                else:
                    status_box.value = "\n".join(new_messages)
                updates["status_box"] = status_box.value
            
            return updates
        
        def cancel_generation(state, thread):
            """Cancel the paper generation process."""
            if state and thread is not None:
                # Cannot directly stop thread, but we can update the UI
                return {
                    output_area: "Generation cancelled by user.",
                    is_generating: False,
                    thread_ref: None,
                    submit_button: gr.Button.update(interactive=True),
                    cancel_button: gr.Button.update(visible=False)
                }
            return {}
        
        # Wire up events
        submit_button.click(
            fn=start_generation,
            inputs=[topic_input, output_filename, is_generating],
            outputs=[output_area, status_box, is_generating, thread_ref, submit_button, cancel_button]
        )
        
        cancel_button.click(
            fn=cancel_generation,
            inputs=[is_generating, thread_ref],
            outputs=[output_area, is_generating, thread_ref, submit_button, cancel_button]
        )
        
        # Check for updates every second
        ui.load(
            fn=lambda: None, 
            inputs=None, 
            outputs=None,
            every=1
        )
        
        check_progress_event = ui.every(
            fn=check_progress,
            inputs=[is_generating, thread_ref],
            outputs=[status_box, output_area, file_output, is_generating, thread_ref, submit_button, cancel_button],
            interval=1.0,
        )

    return ui

def launch_ui(host: str = "127.0.0.1", port: int = 7860):
    """Launch the web UI on the specified host and port."""
    # Check for API key
    if not os.getenv(config["api_key_env_var"]):
        print(f"Error: {config['api_key_env_var']} environment variable not set.")
        print("Please set it in a .env file or export it in your shell.")
        return False
    
    ui = create_ui()
    ui.queue()
    ui.launch(server_name=host, server_port=port)
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Research Agent Web UI")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host to run the web UI on")
    parser.add_argument("--port", type=int, default=7860, help="Port to run the web UI on")
    
    args = parser.parse_args()
    
    print(f"Starting AI Research Agent Web UI on {args.host}:{args.port}")
    launch_ui(args.host, args.port) 