import csv
from pathlib import Path
from collections import Counter
import pandas as pd

LOG_FILE = Path(__file__).parent.parent / "logs" / "chat_log.csv"

def load_logs():
    return pd.read_csv(LOG_FILE)

def basic_summary(df):
    print(" Basic Summary")
    print("Total chat turns:", len(df))
    print("Memory used:", df['used_memory'].sum())
    print("Weather API used:", df['used_weather_api'].sum())

def analyze_tool_usage(df):
    print("\n🔍 Tool Usage Insights")

    print("Memory Usage per Thread ID:")
    print(df.groupby("thread_id")['used_memory'].sum())

    print("\nWeather API Usage per Thread ID:")
    print(df.groupby("thread_id")['used_weather_api'].sum())

def find_misfires(df):
    print("\n Potential Errors or Misfires")
    df["bot_response"] = df["bot_response"].fillna("").astype(str)
    wrong_weather = df[
        (df["used_weather_api"] == True) &
        (~df["bot_response"].str.lower().str.contains("weather"))
    ]

    if not wrong_weather.empty:
        print("Weather tool was triggered but not mentioned in response:")
        print(wrong_weather[["user_query", "bot_response"]])
    else:
        print("No weather tool misfires detected.")

def mark_for_manual_review(df):
    print("\n Flagged for Manual Review (ambiguous responses)")
    flags = df[df['bot_response'].str.len() < 25]  # Example: too short = suspicious
    print(flags[["user_query", "bot_response"]])

def main():
    df = load_logs()
    df["used_memory"] = df["used_memory"].astype(bool)
    df["used_weather_api"] = df["used_weather_api"].astype(bool)

    basic_summary(df)
    analyze_tool_usage(df)
    find_misfires(df)
    mark_for_manual_review(df)

if __name__ == "__main__":
    main()
