from langchain_core.messages import HumanMessage, AIMessage
from .agent import INPUT_MESSAGE, INTERRUPT_MESSAGE, output, CHAT_DATA, clear_chat_data
from .agent_chat import agent_chat
import json
import threading
import queue
import time
import asyncio
import multiprocessing
from multiprocessing import Queue, Event


class PeekableQueue(queue.Queue):
    def peek(self):
        try:
            return self._get()
        except queue.Empty:
            return None
        
async def handle_input_queue(input_queue, should_exit, history):
    while not should_exit.is_set():
        if not input_queue.empty():
            next_input_text = input_queue.get_nowait()
            if next_input_text == INTERRUPT_MESSAGE:
                history.append(AIMessage(content=CHAT_DATA["info"]))
                should_exit.set()  # 设置退出标志
                break
        await asyncio.sleep(0.1)  # 非阻塞地等待一段时间

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
                    
                    # 创建一个异步事件循环
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)

                    # 创建一个 Event 对象用于中断
                    should_exit = asyncio.Event()

                    # 并发运行 agent_chat 和 handle_input_queue
                    agent_chat_task = loop.create_task(agent_chat(bot_setting_file, history, should_exit))
                    input_handler_task = loop.create_task(handle_input_queue(input_queue, should_exit, history))

                    # 运行所有任务
                    loop.run_until_complete(asyncio.gather(agent_chat_task, input_handler_task))

                    # 如果没有中断，则添加 AI 的响应到历史记录
                    if not should_exit.is_set():
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
    should_exit = threading.Event()
    asyncio.run(agent_chat(bot_setting_file, history, should_exit))
    return CHAT_DATA["output"]