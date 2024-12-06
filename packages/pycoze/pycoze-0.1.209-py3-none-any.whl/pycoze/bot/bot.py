from langchain_core.messages import HumanMessage, AIMessage
import threading
import queue
import json
from .agent import INPUT_MESSAGE, output, CHAT_DATA, clear_chat_data
from .agent_chat import agent_chat
import asyncio

class PeekableQueue(queue.Queue):
    def peek(self):
        try:
            return self._get()
        except queue.Empty:
            return None


def chat(bot_setting_file: str):
    history = []
    while True:
        input_text = input()
        if not input_text.startswith(INPUT_MESSAGE):
            raise ValueError("Invalid message")
        message = json.loads(input_text[len(INPUT_MESSAGE) :])
        history.append(HumanMessage(message["content"]))
        should_exit = threading.Event()
        asyncio.run(agent_chat(bot_setting_file, history, should_exit))
        history.append(AIMessage(CHAT_DATA["output"]))




def get_chat_response(bot_setting_file: str, input_text: str):
    history = [HumanMessage(input_text)]
    clear_chat_data()
    should_exit = threading.Event()
    asyncio.run(agent_chat(bot_setting_file, history, should_exit))
    return CHAT_DATA["output"]
