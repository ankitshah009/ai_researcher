#!/usr/bin/env python3
"""Script to test the AI Research Agent with a sample topic."""
import os
import sys
import argparse
import time
from dotenv import load_dotenv
from vertexai.preview.reasoning_engines import AdkApp
from agents.coordinator import coordinator_agent
from callbacks.logging_callback import ResearchAgentCallbackHandler
from config import load_config_from_file

# Load environment variables
load_dotenv()

# Check for API key
if not os.getenv("GOOGLE_API_KEY"):
    print("Error: GOOGLE_API_KEY environment variable not set.")
    print("Please set it in a .env file or export it in your shell.")
    sys.exit(1)

# Load configuration
config = load_config_from_file()

def test_agent(topic="Graph Neural Networks for Protein Folding", output_file="test_paper.pdf", verbose=True):
    """Test the agent with a sample topic."""
    # Initialize callback handler
    callbacks = [ResearchAgentCallbackHandler()]
    
    # Create the runnable app
    app = AdkApp(agent=coordinator_agent, callbacks=callbacks)
    
    print(f"🔍 Testing research agent with topic: '{topic}'")
    print(f"📄 Output will be saved as: {output_file}")
    print("⏳ This process may take several minutes. Progress updates will be shown below:")
    print("-" * 80)
    
    start_time = time.time()
    
    # Stream interaction
    try:
        for event in app.stream_query(
            user_id="TEST_USER", 
            message=f"{topic} Output filename: {output_file}"
        ):
            if event.content and event.content.parts:
                first_part = event.content.parts[0]
                if isinstance(first_part, dict) and "text" in first_part:
                    timestamp = time.strftime("%H:%M:%S", time.localtime())
                    print(f"[{timestamp}] {first_part['text']}")
                elif hasattr(first_part, 'text'):
                    timestamp = time.strftime("%H:%M:%S", time.localtime())
                    print(f"[{timestamp}] {first_part.text}")
        
        elapsed_time = time.time() - start_time
        print("-" * 80)
        print(f"✅ Test completed in {elapsed_time:.2f} seconds")
        print(f"📄 Output saved as: {output_file}")
        
        return True
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        if verbose:
            import traceback
            traceback.print_exc()
        return False

def main():
    """Main entry point for the test script."""
    parser = argparse.ArgumentParser(description="Test the AI Research Agent")
    parser.add_argument("--topic", type=str, 
                       default="Graph Neural Networks for Protein Folding",
                       help="Research topic to test with")
    parser.add_argument("--output", type=str, 
                       default="test_paper.pdf",
                       help="Output PDF filename")
    parser.add_argument("--verbose", "-v", action="store_true", 
                       help="Show verbose output")
    
    args = parser.parse_args()
    
    success = test_agent(args.topic, args.output, args.verbose)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 