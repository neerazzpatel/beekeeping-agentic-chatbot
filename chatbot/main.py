from agent import create_agent
from langchain_core.messages import HumanMessage, AIMessage
from suggest import suggest_questions
from dotenv import load_dotenv
from logger import init_log, log_chat

load_dotenv()
import os


def main():
    def tool_used_in_steps(steps, tool_name="Weather"):
        """
        Checks if the agent called a tool with the given name in the current chunk.
        Works for LangGraph create_react_agent streamed outputs.
        """
        for step in steps:
            action = step.get("action", {})
            if isinstance(action, dict) and action.get("tool") == tool_name:
                return True
        return False

    chat_history = []
    agent, memory = create_agent()
    print("🐝 Welcome, Beekeepers! Ask me anything related to beekeeping.")
    thread_id = input("🧵 Enter your name or session ID: ").strip()
    config = {"configurable": {"thread_id": thread_id}}
    
    init_log()

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        try:
            user_msg = HumanMessage(content=user_input)
            chat_history.append(user_msg)
            all_steps = []
            ai_msg = None
           
            # Streaming the response
            for chunk in agent.stream({"messages": [HumanMessage(content=user_input)]}, config=config):
                if "agent" in chunk:
                    steps = chunk["agent"].get("steps", [])
                    all_steps.extend(steps)

                response = chunk.get("agent", {}).get("messages", [])
                if response:
                    ai_msg = response[0]
                    chat_history.append(ai_msg)
                    print("Bot:", response[0].content)
                    used_weather = False
                    used_weather = tool_used_in_steps(all_steps, tool_name="Weather")
                    log_chat(
                        thread_id=thread_id,
                        user_query=user_input,
                        bot_response=ai_msg.content,
                        used_memory=True,
                        used_weather_api=used_weather )


            chat_history = chat_history[-10:]

            # Suggest follow-up questions
            suggestions = suggest_questions(chat_history)

            if suggestions:
                print("\n🤔 Follow-up suggestions:")
                for i, q in enumerate(suggestions, 1):
                    print(f"  {i}. {q}")
                print()
                # memory.add(thread_id, AIMessage(content="\n".join(suggestions)))
        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    main()
