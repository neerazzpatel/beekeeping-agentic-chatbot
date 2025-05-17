# agent.py

from langchain.chat_models import init_chat_model
from langchain.agents import Tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import create_react_agent
from memory import get_memory
from weather import get_weather_info
import os
import json

if not os.environ.get("GROQ_API_KEY"):
    raise ValueError("GROQ_API_KEY not set. Please set it as an environment variable.")

def create_agent():
    # Load model config
    with open(r"..\configs\agent_llm_model_configs") as f:
        model_config = json.load(f)
    llm = init_chat_model(model_config["model_name"],
            model_provider=model_config["provider"],
            temperature=model_config.get("temperature", 0.7))
    
    
    with open(r"..\configs\prompts\weather_tool_prompt.txt", encoding="utf-8") as f:
        description = f.read()
    tools = [
        Tool(
            name="Weather",
            func=get_weather_info,
            description= description,
        )
    ]
    with open(r"..\configs\prompts\agent_llm_prompt.txt", encoding="utf-8") as f:
        system_prompt = SystemMessage(content=f.read())


    prompt = ChatPromptTemplate.from_messages([
        system_prompt,
        MessagesPlaceholder(variable_name="messages")
    ])

    memory = get_memory()

    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=prompt,  
        checkpointer=memory
    )

    return agent, memory
