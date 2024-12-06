import signal
import sys
import json
from .agent import INPUT_MESSAGE, output, CHAT_DATA, clear_chat_data
from .agent_chat import agent_chat
from multiprocessing import Process, Event
import asyncio
from langchain_core.messages import HumanMessage, AIMessage

# 用于标记中断请求
interrupt_flag = False

# 信号处理函数
def handle_interrupt(signum, frame):
    global interrupt_flag
    interrupt_flag = True
    print("Interrupt signal received. Waiting for the current operation to complete...")

# 设置信号处理器
signal.signal(signal.SIGINT, handle_interrupt)

def read_input():
    while True:
        try:
            input_text = input()
            if input_text.startswith(INPUT_MESSAGE):
                yield input_text
            else:
                raise ValueError("Invalid message")
        except EOFError:  # 如果输入流结束，则退出循环
            break

def chat(bot_setting_file: str):
    history = []
    for input_text in read_input():
        try:
            message = json.loads(input_text[len(INPUT_MESSAGE):])
            history.append(HumanMessage(message["content"]))
            clear_chat_data()

            # 创建一个事件来控制子进程的退出
            should_exit = Event()
            
            # 使用进程来运行 agent_chat
            agent_chat_process = Process(target=asyncio.run, args=(agent_chat(bot_setting_file, history, should_exit),))
            agent_chat_process.start()
            
            # 从管道中读取子进程的输出或错误
            if parent_conn.poll():
                result = parent_conn.recv()
                print(result)
            
            # 检查是否收到了中断信号
            while agent_chat_process.is_alive():
                if interrupt_flag:
                    should_exit.set()  # 设置退出标志
                    break
                time.sleep(0.1)  # 每隔 0.1 秒检查一次

            # 确保子进程已经退出
            agent_chat_process.join()

            # 如果没有收到中断信号，记录输出
            if not interrupt_flag:
                history.append(AIMessage(content=CHAT_DATA["output"]))
            
            # 重置中断标志
            interrupt_flag = False
        except json.JSONDecodeError:
            print("Invalid JSON format in input message.")
        except KeyError:
            print("Missing 'content' key in input message.")
        except Exception as e:
            print(f"An error occurred: {e}")


def get_chat_response(bot_setting_file: str, input_text: str):
    history = [HumanMessage(input_text)]
    clear_chat_data()
    should_exit = threading.Event()
    asyncio.run(agent_chat(bot_setting_file, history, should_exit))
    return CHAT_DATA["output"]