import csv
from datetime import datetime
from pathlib import Path

LOG_FILE = Path(__file__).parent.parent / "mlops" / "logs" / "chat_log.csv"

# Ensure header row is written only once
def init_log():
    print(1)
    if not LOG_FILE.exists():
        with open(LOG_FILE, mode="w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp","thread_id", "user_query", "bot_response", "used_memory", "used_weather_api"])
            print(2)

def log_chat(thread_id, user_query, bot_response, used_memory=False, used_weather_api=False):
    with open(LOG_FILE, mode="a", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().isoformat(),
            thread_id,
            user_query,
            bot_response,
            str(used_memory),
            str(used_weather_api)
        ])
