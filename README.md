# GemAgent

GemAgent is a **Multi-Agent System** built upon the `google-adk` framework. This project is designed to understand a wide range of user requests, intelligently delegate tasks to specialized agents, and ensure efficient and accurate execution.

## Key Features

*   **Date & Time:** Provides current date and time information.
*   **Web Search:** Leverages Google Search to find the latest information and answer your questions.
*   **File System Operations:** Manages local files and directories, including listing files, reading file content, and more.
*   **Fetch Web Content:** Retrieves the content of web pages from specified URLs and converts it into Markdown format.
*   **YouTube Script Extraction:** Extracts the full text transcript from YouTube videos.

## Architecture

GemAgent features a robust, modular architecture composed of a central orchestrator, the `RootAgent`, and a suite of specialized agents, each expertly handling a distinct set of tasks.

*   **RootAgent:**
    *   **Primary Entry Point:** Serves as the initial recipient for all user requests.
    *   **Intent Analysis:** Accurately determines the user's core intent to identify the required task.
    *   **Agent Selection:** Dynamically selects the most suitable specialized agent to address the request.
    *   **Task Routing:** Seamlessly directs the task to the chosen agent, ensuring efficient workflow.

*   **Specialized Agents:** Each agent is designed to excel in its specific domain, contributing to overall system precision and performance.

    *   **`DateTimeAgent`**: Manages all date and time-related inquiries.
        *   **Tooling**: Leverages Function Tools based on simple Python functions.
    *   **`SearchAgent`**: Conducts web searches efficiently using Google.
        *   **Tooling**: Utilizes ADK Built-in Tools for robust search capabilities.
    *   **`FileSystemAgent`**: Facilitates various operations on the local file system.
        *   **Tooling**: Operates as an ADK agent and MCP client, integrating external tools from MCP servers distributed as Node.js packages (executed via `npx`).
    *   **`FetchAgent`**: Retrieves and processes content from web pages.
        *   **Tooling**: Functions as an ADK agent and MCP client, leveraging external tools from MCP servers distributed as Python packages (executed via `uvx`).
    *   **`YouTubeAgent`**: Extracts transcripts from YouTube videos.
        *   **Tooling**: Employs Function Tools based on Python functions, enhanced with additional modules for comprehensive functionality.

This highly modular design empowers each agent to dedicate its focus to a specific domain, resulting in superior accuracy, enhanced operational efficiency, and simplified system maintenance.

## Prerequisites

1.  **Google Gemini API Key:** A Google Gemini API Key is essential for accessing the services.
2.  **Python Installation:** Python must be installed.
    *   `uvx` is required. `uvx` is provided by the uv package. `uv` is a modern, high-performance Python package installer and resolver, developed in Rust. You can install `uv` using `pip` as shown below:
        ```bash
        # pip install uvx
        ```
3.  **Node.js Installation:** Node.js must be installed.
    *   `npx` is required. `npx` is automatically included when you install Node.js (along with `npm`).

## Installation

1.  **Clone the Repository (or download the code):**
    ```bash
    git clone https://github.com/Homin0321/gemagent.git
    ```

2.  **Install Dependencies:**
    Navigate to the project's root directory and install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

To run the project, you need to configure essential environment variables.

- **Create your `.env` file:**
    Within the `allinone` folder (or your project's root if that's where `adk-web` expects it), create a new file named `.env`.
- **Refer to the `.env.example` file for guidance** on the required variables and format. 
- Copy the content from `.env.example` into your `.env` file and **replace the placeholder values with your actual credentials and paths**:
    *   `GOOGLE_API_KEY`: Your API key obtained from Google AI Studio.
    *   `FILESYSTEM_TARGET_FOLDER_PATH`: The absolute path to a local directory that the `FileSystemAgent` will have access to.

## Running the Agent

The agent can be run in three different modes: web interface, CLI, or API server.

### 1. Web Interface
```bash
adk web
```
This will start the web server at http://localhost:8000. You can interact with the agent through a chat-based interface.

### 2. Command Line Interface (CLI)
```bash
adk run allinone
```
This starts an interactive CLI session where you can directly communicate with the agent. Type 'exit' to quit.

### 3. API Server
```bash
adk api_server&
```
This launches the API server at http://localhost:3000, allowing you to integrate the agent with other applications.

### Frontend Application
After starting the ADK API server, you can run the Streamlit frontend:
```bash
streamlit run app.py
```

The frontend interface provides:
- API Server URL configuration (default: http://localhost:8000)
- Agent name selection (default: allinone)
- Session management controls
- Chat interface with message history
- Full response viewer

### Note
Make sure to start the appropriate backend (web, CLI, or API server) before launching the frontend application. The API server must be running at the configured URL for the frontend to function properly.

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.
