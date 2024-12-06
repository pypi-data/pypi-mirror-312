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

# 假设 PeekableQueue 类已经定义好了，如果没有，请自行实现或使用其他方式
class PeekableQueue:
    def __init__(self, maxsize=0):
        self.queue = Queue(maxsize=maxsize)
    
    def put(self, item):
        self.queue.put(item)
    
    def get(self):
        return self.queue.get()
    
    def peek(self):
        with self.queue.mutex:
            if self.queue.empty():
                return None
            return self.queue.queue[0]
    
    def empty(self):
        return self.queue.empty()

def input_process(input_queue: Queue, interrupt_event: Event):
    while not interrupt_event.is_set():
        input_text = input()
        if input_text == INTERRUPT_MESSAGE or input_text.startswith(INPUT_MESSAGE):
            input_queue.put(input_text)
        else:
            raise ValueError("Invalid message")

async def handle_input_queue(input_queue: Queue, should_exit: asyncio.Event, history):
    while not should_exit.is_set():
        try:
            next_input_text = input_queue.get_nowait()
            if next_input_text == INTERRUPT_MESSAGE:
                history.append(AIMessage(content=CHAT_DATA["info"]))
                should_exit.set()  # 设置退出标志
                break
        except queue.Empty:
            pass
        await asyncio.sleep(0.1)  # 非阻塞地等待一段时间

def chat(bot_setting_file: str):
    history = []
    input_queue = PeekableQueue()
    interrupt_event = Event()  # 用于中断输入进程的事件

    # 创建并启动输入进程
    input_process_instance = multiprocessing.Process(target=input_process, args=(input_queue, interrupt_event))
    input_process_instance.start()

    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        while True:
            if not input_queue.empty():
                input_text = input_queue.get()
                if input_text == INTERRUPT_MESSAGE:
                    continue
                try:
                    message = json.loads(input_text[len(INPUT_MESSAGE):])
                    history.append(HumanMessage(message["content"]))
                    clear_chat_data()

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
        # 设置中断事件以停止输入进程
        interrupt_event.set()
        input_process_instance.join()



def get_chat_response(bot_setting_file: str, input_text: str):
    history = [HumanMessage(input_text)]
    clear_chat_data()
    should_exit = threading.Event()
    asyncio.run(agent_chat(bot_setting_file, history, should_exit))
    return CHAT_DATA["output"]