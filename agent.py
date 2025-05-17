# agent.py

from langchain.chat_models import init_chat_model
from langchain.agents import Tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import create_react_agent
from memory import get_memory
from weather import get_weather_info
import os

if not os.environ.get("GROQ_API_KEY"):
  os.environ["GROQ_API_KEY"] = "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"

def create_agent():
    llm = init_chat_model("llama3-8b-8192", model_provider="groq")

    tools = [
        Tool(
            name="Weather",
            func=get_weather_info,
            description=(
                "Use this tool to fetch weather information for a specific location and date. "
                "It's particularly useful for beekeeping decisions like hive inspections, feeding, or pest control. "
                "Only use this tool when weather information is essential." 
                "For the date parameter, use the format YYYY-MM-DD. "
                "If no date is provided, you should first see the user input and then decide about the date else take today as default. "
            )
        )
    ]

    system_prompt = SystemMessage(
        content="""
    You are a helpful assistant for beekeepers. Only use tools if absolutely necessary. 
    Do not call any tool unless the user's question cannot be answered without it.
    Here tools are used to fetch weather information. Whenever you find a question that requires weather information, then use the tool.
    There can be direct and indirect questions about weather.
    Indirect questions will be like "What is the best time to inspect my hive?" or "When should I feed my bees?"
    Example: If a user just says "hi" or "how can you help me", respond conversationally. 
    Also, whenever you are using weather tool you have to explain its reasoning (e.g., “Checked weather before advising hive inspection”).
    """
    )

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
