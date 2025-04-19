"""Custom callback handler for logging agent activity."""
import logging
from typing import Any, Dict, Optional
from google.adk.utils.callbacks import CallbackHandler, CallbackEvent

# Configure logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("ai_research_agent.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("ai_research_agent")

class ResearchAgentCallbackHandler(CallbackHandler):
    """CallbackHandler for monitoring and logging agent execution."""
    
    def on_event(self, event_type: CallbackEvent, event_data: Optional[Dict[str, Any]] = None) -> None:
        """Process callback events from the ADK framework."""
        if event_type == CallbackEvent.AGENT_STARTED:
            agent_name = event_data.get("agent_name", "unknown")
            logger.info(f"Agent started: {agent_name}")
            
        elif event_type == CallbackEvent.AGENT_FINISHED:
            agent_name = event_data.get("agent_name", "unknown")
            logger.info(f"Agent finished: {agent_name}")
            
        elif event_type == CallbackEvent.TOOL_STARTED:
            tool_name = event_data.get("tool_name", "unknown")
            logger.info(f"Tool started: {tool_name}")
            
        elif event_type == CallbackEvent.TOOL_FINISHED:
            tool_name = event_data.get("tool_name", "unknown")
            logger.info(f"Tool finished: {tool_name}")
            
        elif event_type == CallbackEvent.ERROR:
            error_msg = event_data.get("error", "Unknown error")
            logger.error(f"Error: {error_msg}")

# Usage in main.py:
# from callbacks.logging_callback import ResearchAgentCallbackHandler
# app = AdkApp(agent=coordinator_agent, callbacks=[ResearchAgentCallbackHandler()]) 