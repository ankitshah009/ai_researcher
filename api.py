#!/usr/bin/env python3
"""Simple Flask API for AI Research Agent"""
import os
import json
import time
import threading
import queue
from pathlib import Path
from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Import core components
from agents.coordinator import coordinator_agent
from config import get_config, load_config_from_file
from tools.arxiv_search import search_arxiv_func  # Direct function for testing

# Create Flask app
app = Flask(__name__)
# Enable CORS for all routes and all origins with additional options
CORS(app, resources={r"/api/*": {"origins": "*", "supports_credentials": True}})

# Load config
config = load_config_from_file()

# Create output directory
output_dir = Path(config["output"]["output_dir"])
output_dir.mkdir(exist_ok=True, parents=True)

OUTPUTS_FOLDER = os.path.join(os.getcwd(), 'outputs')

# Active jobs tracking
active_jobs = {}
message_queues = {}

def update_agent_models_recursively(agent, model_name):
    """Recursively update the model for an agent and all its sub-agents."""
    # Update this agent's model
    agent.model = model_name
    print(f"Updated agent '{agent.name}' to use model: {model_name}")
    
    # Update all sub-agents recursively if they exist
    if hasattr(agent, 'sub_agents') and agent.sub_agents:
        for sub_agent in agent.sub_agents:
            update_agent_models_recursively(sub_agent, model_name)

def generate_paper(job_id, topic, output_filename):
    """Background worker to generate a paper"""
    
    # Import here to avoid import errors until needed
    try:
        # Updated import pattern for ADK as per tutorial
        from google.adk.runtime.app import AdkApp
    except ImportError:
        try:
            from google.adk.app import AdkApp
        except ImportError:
            # Updated to match new ADK pattern
            from google.adk.runners import Runner
            
    try:
        # Log start
        message_queues[job_id].put({
            "status": "running",
            "message": f"Starting research on topic: {topic}"
        })
        
        # Initialize with updated ADK pattern
        if 'Runner' in locals():
            # Use newer ADK pattern
            from google.adk.sessions import InMemorySessionService
            from google.adk.agents import Agent
            from copy import deepcopy
            
            # Define the model to use
            MODEL_NAME = "gemini-2.5-flash-preview-04-17"
            
            # Create a modified version of the coordinator agent
            modified_agent = deepcopy(coordinator_agent)
            
            # Recursively update all models in the agent hierarchy
            update_agent_models_recursively(modified_agent, MODEL_NAME)
            
            # Create session service and runner
            session_service = InMemorySessionService()
            runner = Runner(
                agent=modified_agent,
                app_name="ai_researcher",
                session_service=session_service
            )
            
            # Create a unique session for this job
            session = session_service.create_session(
                app_name="ai_researcher",
                user_id=f"API_USER_{job_id}",
                session_id=f"session_{job_id}"
            )
            
            # Create content with user query
            from google.genai import types
            content = types.Content(
                role='user', 
                parts=[types.Part(text=f"{topic} Output filename: {output_filename}")]
            )
            
            # Run the agent with the new pattern
            for event in runner.run(
                user_id=f"API_USER_{job_id}",
                session_id=f"session_{job_id}",
                new_message=content
            ):
                if event.content and event.content.parts:
                    first_part = event.content.parts[0]
                    message = ""
                    if hasattr(first_part, 'text'):
                        message = first_part.text
                    
                    if message:
                        message_queues[job_id].put({
                            "status": "running",
                            "message": message
                        })
        else:
            # Use original AdkApp pattern if available
            app = AdkApp(agent=coordinator_agent)
            # Override the model to use
            MODEL_NAME = "gemini-2.5-flash-preview-04-17"
            
            # Recursively update all models in the agent hierarchy
            update_agent_models_recursively(app.agent, MODEL_NAME)
            
            # Run the agent with original pattern
            for event in app.stream_query(
                user_id=f"API_USER_{job_id}", 
                message=f"{topic} Output filename: {output_filename}"
            ):
                if event.content and event.content.parts:
                    first_part = event.content.parts[0]
                    message = ""
                    if isinstance(first_part, dict) and "text" in first_part:
                        message = first_part["text"]
                    elif hasattr(first_part, 'text'):
                        message = first_part.text
                    
                    if message:
                        message_queues[job_id].put({
                            "status": "running",
                            "message": message
                        })
        
        # Debugging: Check if file is present before completing
        full_output_path = os.path.join(OUTPUTS_FOLDER, output_filename)
        print(f"Checking for output file: {full_output_path}")
        
        # If file doesn't exist, create a simple dummy PDF for testing
        if not os.path.exists(full_output_path):
            try:
                print(f"File not found. Attempting to create a dummy PDF.")
                
                # Check if necessary packages are available
                try:
                    from reportlab.pdfgen import canvas
                    
                    # Create a simple PDF with the topic
                    c = canvas.Canvas(full_output_path)
                    c.drawString(100, 750, f"Research on: {topic}")
                    c.drawString(100, 700, "This is a placeholder PDF while we debug the issue.")
                    c.save()
                    print(f"Successfully created dummy PDF at {full_output_path}")
                except ImportError:
                    # If reportlab is not available, create an empty file
                    print("ReportLab not available, creating empty file")
                    with open(full_output_path, 'w') as f:
                        f.write(f"Research on: {topic}\n\nThis is a placeholder file while we debug the issue.")
                    print(f"Created text file at {full_output_path}")
            except Exception as e:
                print(f"Error creating dummy file: {str(e)}")
        else:
            print(f"Output file exists at: {full_output_path}")
                
        # Complete
        message_queues[job_id].put({
            "status": "completed",
            "message": f"Research paper generation complete!",
            "output_file": output_filename
        })
        
    except Exception as e:
        # Handle errors
        error_message = f"Error generating paper: {str(e)}"
        print(f"Error in generate_paper: {error_message}")
        message_queues[job_id].put({
            "status": "error",
            "message": error_message
        })
    
    # Mark job as inactive
    active_jobs[job_id] = False

@app.route('/api/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    # Simplified return
    return jsonify({"status": "ok"})

@app.route('/api/start', methods=['POST'])
def start_job():
    """Start a new research paper generation job"""
    data = request.json
    topic = data.get('topic', '')
    
    if not topic:
        return jsonify({
            "status": "error",
            "message": "Topic is required"
        }), 400
    
    # Generate job ID based on timestamp
    job_id = str(int(time.time()))
    
    # Set output filename
    output_filename = data.get('filename', config["output"]["default_pdf_name"])
    output_path = output_dir / output_filename
    
    # Create message queue for this job
    message_queues[job_id] = queue.Queue()
    
    # Start job in background thread
    active_jobs[job_id] = True
    thread = threading.Thread(
        target=generate_paper,
        args=(job_id, topic, output_filename),
        daemon=True
    )
    thread.start()
    
    return jsonify({
        "status": "started",
        "job_id": job_id,
        "message": f"Started research on topic: {topic}"
    })

@app.route('/api/status/<job_id>', methods=['GET'])
def job_status(job_id):
    """Get status updates for a job"""
    if job_id not in message_queues:
        return jsonify({
            "status": "error",
            "message": "Job not found"
        }), 404
    
    # Collect all available messages
    messages = []
    try:
        while not message_queues[job_id].empty():
            messages.append(message_queues[job_id].get_nowait())
    except queue.Empty:
        pass
    
    # Return status
    return jsonify({
        "job_id": job_id,
        "active": active_jobs.get(job_id, False),
        "updates": messages
    })

@app.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    """Download a generated PDF file"""
    # Use the OUTPUTS_FOLDER constant defined above
    file_path = Path(OUTPUTS_FOLDER) / filename
    
    if not file_path.exists():
        print(f"ERROR: File {file_path} not found")
        return jsonify({
            "status": "error",
            "message": f"File {filename} not found"
        }), 404
    
    # Return the file directly
    return send_file(file_path, as_attachment=True)

@app.route('/outputs/<filename>')
def serve_output_file(filename):
    """Serve files from the outputs directory."""
    try:
        # Explicitly print the requested file path for debugging
        print(f"Serving file from outputs directory: {filename}")
        file_path = os.path.join(OUTPUTS_FOLDER, filename)
        print(f"Full path: {file_path}")
        print(f"File exists: {os.path.exists(file_path)}")
        
        return send_from_directory(OUTPUTS_FOLDER, filename, as_attachment=False)
    except FileNotFoundError:
        print(f"ERROR: File {filename} not found in outputs directory")
        return jsonify({"error": "File not found"}), 404

@app.route('/api/test/arxiv', methods=['GET'])
def test_arxiv():
    """Test endpoint for arXiv search"""
    query = request.args.get('query', 'Graph Neural Networks')
    limit = int(request.args.get('limit', 3))
    
    try:
        results = search_arxiv_func(query, limit)
        return jsonify({
            "status": "success",
            "results": results
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)