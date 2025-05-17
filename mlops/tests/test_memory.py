import sys
import os

# Add the parent directory to sys.path so chatbot module can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../chatbot")))

from memory import get_memory

def test_memory_behavior():
    memory = get_memory()
    assert memory is not None