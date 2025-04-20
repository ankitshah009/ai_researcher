#!/usr/bin/env python3
"""Simple Flask API for AI Research Agent"""
import os
import json
import time
import threading
import queue
from pathlib import Path
from flask import Flask, request, jsonify, send_file
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
# Enable CORS for all routes and all origins
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Load config
config = load_config_from_file()

# Create output directory
output_dir = Path(config["output"]["output_dir"])
output_dir.mkdir(exist_ok=True, parents=True)

# Active jobs tracking
active_jobs = {}
message_queues = {}

def generate_paper(job_id, topic, output_filename):
    """Background worker to generate a paper"""
    
    # Import here to avoid import errors until needed
    try:
        from google.adk.runtime.app import AdkApp
    except ImportError:
        try:
            from google.adk.app import AdkApp
        except ImportError:
            from google.adk import AdkApp
    
    try:
        # Log start
        message_queues[job_id].put({
            "status": "running",
            "message": f"Starting research on topic: {topic}"
        })
        
        # Initialize AdkApp
        app = AdkApp(agent=coordinator_agent)
        
        # Run the agent
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
        
        # Complete
        message_queues[job_id].put({
            "status": "completed",
            "message": f"Research paper generation complete!",
            "output_file": output_filename
        })
        
    except Exception as e:
        # Handle errors
        error_message = f"Error generating paper: {str(e)}"
        message_queues[job_id].put({
            "status": "error",
            "message": error_message
        })
    
    # Mark job as inactive
    active_jobs[job_id] = False

@app.route('/api/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({
        "status": "ok",
        "message": "AI Research Agent API is running"
    })

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
    file_path = output_dir / filename
    
    if not file_path.exists():
        return jsonify({
            "status": "error",
            "message": f"File {filename} not found"
        }), 404
    
    return send_file(file_path, as_attachment=True)

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