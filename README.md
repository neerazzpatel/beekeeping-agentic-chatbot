🐝 Agentic Beekeeping Chatbot + MLOps

This repository contains an intelligent beekeeping assistant that uses conversational memory, tool-based reasoning, and weather awareness to guide beekeepers. Built with LangGraph and LangChain, the bot makes agentic decisions and suggests relevant follow-up questions, while also including MLOps features like testing, logging, and CI/CD.

🎯 Objective

Build a context-aware, tool-using chatbot that helps beekeepers make weather-sensitive decisions, with support from automated tests, versioning, and logging — all without Docker.

✅ Functional Features

1. 🧠 Conversational Memory

  Maintains the last 5 user-bot interactions using MemorySaver.
  
  Enables the bot to give contextual answers based on prior exchanges.

2. 🤖 Agentic Decision-Making
   
Uses LangGraph’s create_react_agent to determine:

Whether to recall memory.

Whether to invoke a weather API tool.

Agent calls the weather tool only for relevant queries (e.g. hive inspections, feeding).

Includes explanations like: "Checked weather before advising hive inspection."

3. 💬 Follow-up Suggestions
   
Generates 3 relevant follow-up questions after each user query.

Tailored to the conversation context (e.g. health of bees, best practices, inspections).

⚙️ MLOps Features (No Docker)

4. 🔖 Model & Prompt Versioning
   
Prompts and model settings are stored in the configs/ directory.

Git is used to track changes in prompt wording and model configuration over time.

5. 🔄 CI/CD Pipeline
   
Configured using GitHub Actions.

Automatically:

Installs dependencies.

Runs basic tests (pytest).

Checks code style using black and flake8.

6. 📊 Logging & Monitoring
   
Each chat turn logs:

The user query

Bot response

Whether memory and weather API were used

Logs saved to a CSV file at mlops/logs/chat_log.csv

7. 🧪 Evaluation Tools
   
A Python script under mlops/eval/ assesses:

Whether the weather API was used appropriately

Whether memory was referenced

Flags ambiguous or short responses for review


🚀 How to Run

Install requirements:

pip install -r requirements.txt
Set up your environment:

Copy .env.example → .env and set your GROQ_API_KEY and WEATHER_API_KEY.

Launch the chatbot:


cd chatbot
python main.py
🧪 Run Tests and Evaluation
Run tests:


pytest
Run code formatter check:


black --check .
Evaluate chat logs:


python mlops/eval/evaluate_chat_logs.py
📌 Notes
No Docker or cloud deployment used.

CI/CD is handled via GitHub Actions.

All prompts and models are version-controlled under configs/.

📬 Example Use Case
User: “Can I open the hive tomorrow in Bangalore?”
Bot: “Checked weather before advising hive inspection. Tomorrow in Bangalore is sunny with moderate temperatures — good conditions for opening the hive.”
