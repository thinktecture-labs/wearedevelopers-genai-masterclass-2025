import os
import datetime
import uuid
from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver
from tools import get_employee_id, book_slot

def main():
    """Main entry point for the application."""
    try:
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        model_name = os.getenv("OPENAI_MODEL", "gpt-4o")
        
        if not api_key:
            print("Error: OPENAI_API_KEY environment variable is not set.")
            print("Please set it in the .env file or as an environment variable.")
            return
        
        agent = create_agent(api_key, model_name)
        run_chat_loop(agent)
    
    except Exception as ex:
        print(f"An error occurred: {ex}")

def create_agent(api_key, model_name):
    """Create and configure the LangGraph agent."""
    os.environ["OPENAI_API_KEY"] = api_key
    model = init_chat_model(model_name, temperature=0)
    checkpointer = InMemorySaver()
    
    agent = create_react_agent(
        model=model,
        tools=[get_employee_id, book_slot],
        prompt="You're a friendly, helpful chat assistant. "
               "Only answer questions that relate to your tools, functions, and plugins — no other questions! "
               "Only list and use the tools you are explicitly provided with as functions in the request. "
               f"Today is {datetime.datetime.now().strftime('%A, %B %d, %Y')}.",
        checkpointer=checkpointer
    )
    
    return agent

def run_chat_loop(agent):
    """Run the interactive chat loop."""
    print("Welcome to our Helpful Agent.")
    print("You can ask questions now.")
    print("Type 'exit' to quit.")
    print()
    
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    while True:
        user_input = input("Your input: ")
        
        if not user_input or user_input.lower() == "exit":
            break
        
        try:
            response = agent.invoke(
                {"messages": [{"role": "user", "content": user_input}]},
                config
            )
            
            try:
                last_message = response["messages"][-1]
                agent_message = last_message.content if hasattr(last_message, "content") else str(last_message)
                print(f"Agent output: {agent_message}")
            except Exception as ex:
                print(f"Error: {ex}")
            
        except Exception as ex:
            print(f"Error: {ex}")
    
    print("Goodbye!")

if __name__ == "__main__":
    main()
