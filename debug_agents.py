#!/usr/bin/env python3
"""Debug script to test individual agents and print their outputs."""
import os
import json
import sys
import traceback
from pathlib import Path

# Import agents
from agents.coordinator import coordinator_agent
from agents.outline_agent import outline_agent
from agents.literature_agent import literature_agent
from agents.drafting_agent import drafting_agent
from agents.citation_agent import citation_agent
from agents.formatting_agent import formatting_agent

# Import ADK
from google.adk.runtime.app import AdkApp
from google.adk.agents import Agent

# Set up output directory
debug_dir = Path("debug_outputs")
debug_dir.mkdir(exist_ok=True)

def update_agent_model(agent, model_name="gemini-2.5-flash-preview-04-17"):
    """Update agent model recursively."""
    agent.model = model_name
    print(f"Updated agent '{agent.name}' to use model: {model_name}")
    
    if hasattr(agent, 'sub_agents') and agent.sub_agents:
        for sub_agent in agent.sub_agents:
            update_agent_model(sub_agent, model_name)

def test_agent(agent, input_message, save_path):
    """Test a single agent with the given input and save the output."""
    print(f"\n\n{'='*80}")
    print(f"TESTING AGENT: {agent.name}")
    print(f"{'='*80}")
    
    try:
        # Create a copy with updated model
        update_agent_model(agent)
        
        # Create AdkApp for the agent
        app = AdkApp(agent=agent)
        
        # Create lists to store events and outputs
        events = []
        agent_output = ""
        
        # Run the agent
        print(f"Running {agent.name} with input: {input_message[:100]}...")
        for event in app.stream_query(user_id="debug_user", message=input_message):
            events.append(event)
            if event.content and event.content.parts:
                first_part = event.content.parts[0]
                message = ""
                if isinstance(first_part, dict) and "text" in first_part:
                    message = first_part["text"]
                elif hasattr(first_part, 'text'):
                    message = first_part.text
                
                if message:
                    agent_output += message + "\n"
                    print(f"Output from {agent.name}: {message[:200]}...")
        
        # Save the output
        with open(save_path, 'w') as f:
            f.write(f"Agent: {agent.name}\n")
            f.write(f"Input: {input_message}\n\n")
            f.write(f"Output:\n{agent_output}\n")
            
            # Save event details
            f.write("\nEvents:\n")
            for i, event in enumerate(events):
                f.write(f"Event {i}:\n")
                f.write(f"  Author: {event.author}\n")
                f.write(f"  Final: {event.is_final_response()}\n")
                if event.content:
                    for part in event.content.parts:
                        if hasattr(part, 'text'):
                            f.write(f"  Content: {part.text[:200]}...\n")
                f.write("\n")
        
        print(f"Output saved to {save_path}")
        return agent_output
    
    except Exception as e:
        error_message = f"Error testing {agent.name}: {str(e)}\n{traceback.format_exc()}"
        print(error_message)
        with open(save_path, 'w') as f:
            f.write(error_message)
        return error_message

def main():
    """Run tests on all agents."""
    # Sample research topic
    topic = "Machine learning applications in climate science"
    
    # Test outline agent
    outline_output = test_agent(
        outline_agent,
        topic,
        debug_dir / "outline_output.txt"
    )
    
    # Test literature agent with outline
    literature_output = test_agent(
        literature_agent,
        f"Topic: {topic}\nOutline:\n{outline_output}",
        debug_dir / "literature_output.txt"
    )
    
    # Test drafting agent with section and literature
    section_name = "Introduction"
    drafting_output = test_agent(
        drafting_agent,
        f"Section: {section_name}\nTopic: {topic}\nOutline Section: {outline_output}\nLiterature: {literature_output[:1000]}...",
        debug_dir / "drafting_output.txt"
    )
    
    # Test citation agent with draft and literature
    citation_output = test_agent(
        citation_agent,
        f"Draft: {drafting_output}\nLiterature: {literature_output[:1000]}...",
        debug_dir / "citation_output.txt"
    )
    
    # Test formatting agent with structured content
    paper_structure = {
        "title": f"Research on {topic}",
        "abstract": "This is a test abstract.",
        "introduction": drafting_output,
        "related_work": "This is the related work section.",
        "methodology": "This is the methodology section.",
        "experiments": "This is the experiments section.",
        "results": "This is the results section.",
        "discussion": "This is the discussion section.",
        "conclusion": "This is the conclusion.",
        "references": citation_output
    }
    
    formatting_input = json.dumps(paper_structure, indent=2)
    formatting_output = test_agent(
        formatting_agent,
        f"Please generate a PDF using the following paper structure:\n{formatting_input}",
        debug_dir / "formatting_output.txt"
    )
    
    # Print summary
    print("\n\nAGENT TESTING SUMMARY")
    print("-" * 40)
    for agent_name in ["outline", "literature", "drafting", "citation", "formatting"]:
        path = debug_dir / f"{agent_name}_output.txt"
        status = "✅ SUCCESS" if os.path.exists(path) and os.path.getsize(path) > 0 else "❌ FAILED"
        print(f"{agent_name.upper():15s}: {status}")
    
    print("\nCheck the debug_outputs directory for detailed agent outputs.")
    print(f"Full agent debugging complete. Results saved in {debug_dir}")

if __name__ == "__main__":
    main() 