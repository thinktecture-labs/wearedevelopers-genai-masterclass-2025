# Simple Function Calling Agent with LangGraph

This project demonstrates how to build a conversational agent with function calling capabilities using LangGraph and LangChain. It's a Python implementation of the same functionality found in the Semantic Kernel C# version (`simple-function-calling-agent-sk`).

## Features

- Implements a chat agent that can call functions based on user input
- Uses LangGraph's ReAct agent pattern for reasoning and action
- Supports two functions:
  - Getting an employee ID by name
  - Booking a meeting slot for an employee
- Maintains conversation history across multiple turns

## Prerequisites

- Python 3.9+
- OpenAI API key

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   OPENAI_MODEL=gpt-4o  # Optional, defaults to gpt-4o
   ```

## Running the Agent

We've provided several versions of the agent implementation to accommodate different use cases and potential compatibility issues:

### Interactive Chat (main.py)

The standard implementation with an interactive chat loop:

```bash
python main.py
```

### Alternative Implementations

If you encounter issues with the main implementation, try one of these alternatives:

1. **Revised Chat Loop (main_new.py)**:
   ```bash
   python main_new.py
   ```

2. **Simple Demo (main_simple.py)**:
   A simplified version with memory management:
   ```bash
   python main_simple.py
   ```

3. **Basic Demo (main_basic.py)**:
   The most basic implementation following the LangGraph documentation closely:
   ```bash
   python main_basic.py
   ```

## Example Conversation

```
Welcome to our Helpful Agent.
You can ask questions now.
Type 'exit' to quit.

Your input: What's the employee ID for John Smith?
Agent output: I'll help you find the employee ID for John Smith.

I need to use the get_employee_id function to look up this information.

The employee ID for John Smith is 42.

Your input: Can you book a meeting with them tomorrow at 2pm for 30 minutes?
Agent output: I'll book a meeting slot for employee 42 (John Smith) tomorrow at 2:00 PM for 30 minutes.

I'll use the book_slot function to schedule this meeting.

I've booked a 'Meeting' slot for employee 42 on 2023-06-13T14:00:00+02:00 for 30 minutes.

Your input: exit
Goodbye!
```

## How It Works

1. The agent uses LangGraph's `create_react_agent` to create a ReAct agent that can reason about user requests and take appropriate actions.
2. When a user asks a question, the agent determines if it needs to call a function to fulfill the request.
3. If needed, it calls one of the registered functions (`get_employee_id` or `book_slot`).
4. The agent incorporates the function results into its response to the user.
5. The conversation history is maintained across turns using LangGraph's memory system.

## Comparison with Semantic Kernel Version

This implementation provides the same functionality as the Semantic Kernel C# version but uses LangGraph and LangChain in Python. The key differences are:

- Uses Python instead of C#
- Uses LangGraph's ReAct agent pattern instead of Semantic Kernel's function calling
- Implements the same functions with similar signatures and behavior

## License

[MIT License](LICENSE)
