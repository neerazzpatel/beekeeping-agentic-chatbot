from agent import create_agent
from langchain_core.messages import HumanMessage, AIMessage
from suggest import suggest_questions
from dotenv import load_dotenv
load_dotenv()
import os
def main():
    chat_history = []
    agent, memory = create_agent()
    print("🐝 Welcome, Beekeepers! Ask me anything related to beekeeping.")
    thread_id = input("🧵 Enter your name or session ID: ").strip()
    config = {"configurable": {"thread_id": thread_id}}
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        try:
            user_msg = HumanMessage(content=user_input)
            chat_history.append(user_msg)
            # Streaming the response
            for chunk in agent.stream({"messages": [HumanMessage(content=user_input)]}, config=config):
                response = chunk.get("agent", {}).get("messages", [])
                if response:
                    ai_msg = response[0]
                    chat_history.append(ai_msg)
                    print("Bot:", response[0].content)
            
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

