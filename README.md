# Carbon

Carbon is a minimalist, local-first ReAct coding agent built in Python. It executes multi-turn tool-calling loops to inspect, modify, and run code within a sandboxed project directory (`./calculator`).

---

## Architecture

Carbon implements an iterative ReAct (Reasoning + Acting) loop using OpenAI-compatible function-calling specifications:

```
                  +-------------------+
                  |    User Prompt    |
                  +---------+---------+
                            |
                            v
               +------------+------------+
+------------> | LLM Chat Completions API | <------------+
|              +------------+------------+              |
|                           |                           |
|                    (Tool Calls?)                      |
|                           |                           |
|             +-------------+-------------+             |
|        Yes  |                           |  No         |
|             v                           v             |
|   +-------------------+       +-------------------+   |
|   | Dispatch Function |       | Print Final Answer|   |
|   +---------+---------+       +---------+---------+   |
|             |                           |             |
|             v                           v             |
|   +-------------------+             [ Terminate ]     |
|   | Execute Tool &    |                               |
|   | Append to History |                               |
|   +---------+---------+                               |
+-------------+                                         |
```

### Core Components

- **`main.py`**: CLI entry point and agent loop orchestrator. Manages conversation history, message sequence integrity, and iteration limits.
- **`call_functions.py`**: Tool router and OpenAI JSON schema registry. Dispatches tool requests and injects the working directory.
- **`prompt.py`**: System instructions establishing agent behavior, planning expectations, and relative path constraints.
- **`functions/`**:
  - [`get_files_info.py`](functions/get_files_info.py): Directory inspection with file sizes and directory metadata.
  - [`get_file_content.py`](functions/get_file_content.py): Safe file read operations.
  - [`write_file.py`](functions/write_file.py): Atomic-style file writes with directory auto-creation.
  - [`run_python_file.py`](functions/run_python_file.py): Isolated Python subprocess execution with timeouts and output capture.
- **`calculator/`**: Target workspace sandbox containing the codebase the agent operates on.

---

## Security & Path Sandboxing

All file operations enforce strict path traversal protection using `os.path.commonpath`:
```python
valid_path = os.path.commonpath([work_path, target_path]) == work_path
```
Requests attempting to escape `./calculator` (e.g. `../` or `/etc/passwd`) are rejected before touching the filesystem.

---

## Setup

### Prerequisites

- Python `>= 3.13`
- [`uv`](https://github.com/astral-sh/uv)

### Installation

```bash
# Clone the repository
git clone git@github.com:ahorts/carbon.git
cd carbon

# Sync virtualenv and dependencies
uv sync
```

### Configuration

Create a `.env` file in the project root:

```ini
# OpenRouter API Key (if using cloud inference)
OPENROUTER_API_KEY="sk-or-v1-..."
```

For local inference via Ollama, configure the client in `main.py` to point to `http://localhost:11434/v1` with any dummy key (e.g., `api_key="ollama"`).

---

## Usage

### Basic Execution

```bash
uv run main.py "Check the calculator tests and fix any failing test cases"
```

### Verbose Mode

Pass `--verbose` to inspect token usage, tool invocation arguments, and intermediate function outputs in real-time:

```bash
uv run main.py "Add a modulo operator to the calculator" --verbose
```

---

## Running Tests

Unit tests for each tool function live in the project root:

```bash
uv run test_get_files_info.py
uv run test_get_file_content.py
uv run test_write_file.py
uv run test_run_python_file.py
```
