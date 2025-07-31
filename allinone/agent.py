import os
import datetime
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools import agent_tool
from google.adk.tools import google_search
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from .youtube import get_youtube_transcript
from .instruction import root_instruction, datetime_instruction, search_instruction, filesystem_instruction, fetch_instruction, youtube_instruction 

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
# Defines the target directory for the FileSystemAgent.
# This path is loaded from the .env file.
TARGET_FOLDER_PATH = os.path.abspath(
    os.getenv("FILESYSTEM_TARGET_FOLDER_PATH", os.getcwd())
)

# --- Tool Functions ---
def get_current_datetime() -> str:
    """
    Tool function that returns the current date and time.
    Returns the current date and time as a string in 'YYYY-MM-DD HH:MM:SS' format.
    """
    now = datetime.datetime.now()

    return f"Current Date and Time: {now.strftime('%Y-%m-%d %H:%M:%S')}"

# --- Agent Definitions ---

# Agent for handling date and time related queries.
datetime_agent = Agent(
    model='gemini-2.0-flash',
    name='DateTimeAgent',
    instruction=datetime_instruction,
    tools=[get_current_datetime],
)

# Agent for performing web searches using Google Search.
search_agent = Agent(
    model='gemini-2.0-flash',
    name='SearchAgent',
    instruction=search_instruction,
    tools=[google_search],
)

# Agent for interacting with the local filesystem.
# It uses the Model-Context-Protocol (MCP) to securely manage file operations.
filesystem_agent = Agent(
    model='gemini-2.0-flash',
    name='FileSystemAgent',
    instruction=filesystem_instruction,
    tools=[
        MCPToolset(
            connection_params=StdioServerParameters(
                command='npx',
                args=[
                    "-y",
                    "@modelcontextprotocol/server-filesystem",
                    os.path.abspath(TARGET_FOLDER_PATH),
                ],
            ),
        )
    ],
)

# Agent for fetching and processing content from web pages.
# It uses an MCP server to handle the fetching process.
fetch_agent = Agent(
    model='gemini-2.0-flash',
    name='fetch',
    instruction=fetch_instruction,
    tools=[
        MCPToolset(
            connection_params=StdioServerParameters(
                command='uvx',
                args=[
                    "mcp-server-fetch"
                ],
            ),
        )
    ],
)

# Agent for extracting transcripts from YouTube videos.
youtube_agent = Agent(
    model='gemini-2.0-flash',
    name='YouTubeAgent',
    instruction=youtube_instruction,
    tools=[get_youtube_transcript],
)

# --- Root Agent ---
# The main agent that orchestrates the other agents.
# It analyzes the user's request and delegates the task to the most appropriate sub-agent.
root_agent = Agent(
    name="RootAgent",
    model="gemini-2.0-flash",
    instruction=root_instruction,
    description="Root Agent",
    tools=[
        agent_tool.AgentTool(agent=datetime_agent),
        agent_tool.AgentTool(agent=search_agent),
        agent_tool.AgentTool(agent=filesystem_agent),
        agent_tool.AgentTool(agent=fetch_agent),
        agent_tool.AgentTool(agent=youtube_agent),
    ],
)