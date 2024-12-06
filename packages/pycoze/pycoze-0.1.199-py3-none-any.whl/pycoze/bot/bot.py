from langchain_core.messages import HumanMessage, AIMessage
from .agent import INPUT_MESSAGE, INTERRUPT_MESSAGE, output, CHAT_DATA, clear_chat_data
from .agent_chat import agent_chat
import json
import threading
import queue
import time
import asyncio
import multiprocessing


class PeekableQueue(queue.Queue):
    def peek(self):
        try:
            return self._get()
        except queue.Empty:
            return None


def run_agent_chat(bot_setting_file, history, should_exit):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(agent_chat(bot_setting_file, history, should_exit))
    loop.close()


def chat(bot_setting_file: str):
    history = []
    input_queue = PeekableQueue()

    def input_thread(input_queue: PeekableQueue):
        while True:
            input_text = input()
            if input_text == INTERRUPT_MESSAGE or input_text.startswith(INPUT_MESSAGE):
                input_queue.put(input_text)
            else:
                raise ValueError("Invalid message")
            

    input_thread_instance = threading.Thread(target=input_thread, args=(input_queue,))
    input_thread_instance.start()

    try:
        while True:
            if not input_queue.empty():
                input_text = input_queue.get()
                if input_text == INTERRUPT_MESSAGE:
                    continue
                try:
                    message = json.loads(input_text[len(INPUT_MESSAGE):])
                    history.append(HumanMessage(message["content"]))
                    clear_chat_data()
                    
                    # 创建进程退出标志
                    should_exit = multiprocessing.Event()
                    agent_chat_process = multiprocessing.Process(target=run_agent_chat, args=(bot_setting_file, history, should_exit)) # 需要是独立进程，不然无法创建新进程
                    agent_chat_process.start()
                    
                    next_input_text = ""
                    while agent_chat_process.is_alive():
                        if not input_queue.empty():
                            next_input_text = input_queue.peek()
                            if next_input_text == INTERRUPT_MESSAGE:
                                history.append(AIMessage(content=CHAT_DATA["info"]))
                                should_exit.set()  # 设置退出标志
                                break
                        time.sleep(0.1)  # 每隔 0.1 秒检查一次
                    if next_input_text != INTERRUPT_MESSAGE:
                        history.append(AIMessage(content=CHAT_DATA["output"]))
                except json.JSONDecodeError:
                    print("Invalid JSON format in input message.")
                except KeyError:
                    print("Missing 'content' key in input message.")
                except Exception as e:
                    print(f"An error occurred: {e}")
    finally:
        input_thread_instance.join()



def get_chat_response(bot_setting_file: str, input_text: str):
    history = [HumanMessage(input_text)]
    clear_chat_data()
    should_exit = multiprocessing.Event()
    asyncio.run(agent_chat(bot_setting_file, history, should_exit))
    return CHAT_DATA["output"]