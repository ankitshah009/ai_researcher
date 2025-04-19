"""CLI entry-point: `python main.py --topic "Self-supervised audio event detection"`"""
import argparse
import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv

# Updated import for AdkApp
from google.cloud.aiplatform.preview.reasoning_engines import AdkApp
# Alternative import if needed: 
# import vertexai
# from vertexai.preview.reasoning_engines import AdkApp

from agents.coordinator import coordinator_agent
from callbacks.logging_callback import ResearchAgentCallbackHandler

# Load environment variables from .env file
load_dotenv()

# Check for API key
if not os.getenv("GOOGLE_API_KEY"):
    print("Error: GOOGLE_API_KEY environment variable not set.")
    print("Please set it in a .env file or export it in your shell.")
    sys.exit(1)

def display_progress(event):
    """Display progress updates to the console with timestamp."""
    if event.content and event.content.parts:
        first_part = event.content.parts[0]
        if isinstance(first_part, dict) and "text" in first_part:
            timestamp = time.strftime("%H:%M:%S", time.localtime())
            print(f"[{timestamp}] {first_part['text']}")
        elif hasattr(first_part, 'text'):
            # Handle string-like objects with text attribute
            timestamp = time.strftime("%H:%M:%S", time.localtime())
            print(f"[{timestamp}] {first_part.text}")

def main():
    """Main entry point for the research agent."""
    parser = argparse.ArgumentParser(description="AI Research Agent - Generate research papers from topics")
    parser.add_argument("--topic", type=str, help="Research topic to generate a paper about")
    parser.add_argument("--package", action="store_true", help="Package the codebase for sharing")
    parser.add_argument("--output", type=str, default="research_paper.pdf", help="Output PDF filename")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
    parser.add_argument("--model", choices=["gemini-2.0-flash", "gemini-2.5-pro"], 
                      help="Override the model used by coordinator (advanced)")
    
    args = parser.parse_args()
    
    # Handle packaging option
    if args.package:
        package_codebase()
        return
    
    # Ensure topic is provided
    if not args.topic:
        parser.print_help()
        print("\nError: --topic argument is required unless --package is specified")
        sys.exit(1)
    
    # Initialize callback handler
    callbacks = [ResearchAgentCallbackHandler()]
    
    # Create the runnable app with callbacks
    app = AdkApp(agent=coordinator_agent, callbacks=callbacks)
    
    print(f"🔍 Starting research on topic: '{args.topic}'")
    print(f"📄 Output will be saved as: {args.output}")
    print("⏳ This process may take several minutes. Progress updates will be shown below:")
    print("-" * 80)
    
    try:
        # Stream interaction
        for event in app.stream_query(
            user_id="LOCAL_USER", 
            message=f"{args.topic} Output filename: {args.output}"
        ):
            display_progress(event)
            
        print("-" * 80)
        print(f"✅ Research paper generation complete! Check {args.output} for the result.")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

def package_codebase():
    """Package the codebase for sharing."""
    import shutil
    
    zip_path = Path("ai_research_agent.zip")
    try:
        # Create the zip archive
        shutil.make_archive(zip_path.stem, "zip", ".")
        
        # Get file size in MB
        size_mb = zip_path.stat().st_size / (1024 * 1024)
        
        print(f"✅ Packaged codebase: {zip_path.absolute()} ({size_mb:.2f} MB)")
    except Exception as e:
        print(f"❌ Error creating package: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 