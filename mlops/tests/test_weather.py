import sys
import os

# Add the parent directory to sys.path so chatbot module can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../chatbot")))

from weather import get_weather_info

def test_weather_api_response():
    result = get_weather_info("Bangalore")
    assert isinstance(result, str)
