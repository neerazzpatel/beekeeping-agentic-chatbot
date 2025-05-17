# suggest.py

from langchain_core.messages import BaseMessage
from langchain.chat_models import init_chat_model
import os
import json

# Load model config
with open(r"..\configs\suggest_llm_model_configs.json") as f:
    model_config = json.load(f)


def load_prompt_template():
    # base_dir = os.path.dirname(__file__)
    prompt_path = os.path.join("..", "configs", "prompts", "suggest_llm_prompt.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()


# Initialize the LLM
llm = init_chat_model(
    model_config["model_name"],
    model_provider=model_config["provider"],
    temperature=model_config.get("temperature", 0.7),
)


def suggest_questions(history: list[BaseMessage]) -> list[str]:
    """
    Generates 3 follow-up question suggestions based on the recent conversation history.
    """
    last_turns = "\n".join(
        [f"{msg.type.capitalize()}: {msg.content}" for msg in history[-6:]]
    )  # last 3 exchanges

    # Load and format prompt
    prompt_template = load_prompt_template()
    prompt = prompt_template.format(history=last_turns)

    response = llm.invoke(prompt).content
    suggestions = []
    for line in response.strip().split("\n"):
        if line.strip().startswith(("1.", "2.", "3.")):
            question = line.split(".", 1)[1].strip()
            suggestions.append(question)
    return suggestions
