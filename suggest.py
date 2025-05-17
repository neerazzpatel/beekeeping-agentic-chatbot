# suggest.py

from langchain_core.messages import BaseMessage
from langchain.chat_models import init_chat_model

# Initialize the LLM 
llm = init_chat_model("llama3-8b-8192", model_provider="groq")

def suggest_questions(history: list[BaseMessage]) -> list[str]:
    """
    Generates 3 follow-up question suggestions based on the recent conversation history.
    """
    last_turns = "\n".join([f"{msg.type.capitalize()}: {msg.content}" for msg in history[-6:]])  # last 3 exchanges
    prompt = (
        f"Based on this conversation between a user and a beekeeping assistant:\n\n"
        f"{last_turns}\n\n"
        f"Suggest 3 helpful follow-up questions the user might ask next. "
        f"Keep them short, relevant, and specific to beekeeping or the current topic. "
        f"Format your response as a numbered list."
        f" Do not include any explanations or additional text. Just list the 3 questions numbered from 1 to 3.\n\n"
    )
    response = llm.invoke(prompt).content
    suggestions = []
    for line in response.strip().split("\n"):
        if line.strip().startswith(("1.", "2.", "3.")):
            question = line.split(".", 1)[1].strip()
            suggestions.append(question)
    return suggestions
