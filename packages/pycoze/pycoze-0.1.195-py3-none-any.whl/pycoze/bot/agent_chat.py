import json
from langchain_openai import ChatOpenAI
from .agent import run_agent, Runnable, output
import asyncio
from pycoze import utils
from pycoze.reference.bot import ref_bot
from pycoze.reference.tool import ref_tools
from langchain_core.utils.function_calling import convert_to_openai_tool

cfg = utils.read_json_file("llm.json")


def load_role_setting(bot_setting_file: str):
    with open(bot_setting_file, "r", encoding="utf-8") as f:
        return json.load(f)


def load_abilities(bot_setting_file: str):
    with open(bot_setting_file, "r", encoding="utf-8") as f:
        role_setting = json.load(f)

    abilities = []
    for bot_id in role_setting["bots"]:
        bot = ref_bot(bot_id, as_agent_tool=True)
        if bot:
            abilities.append(bot)
    for tool_id in role_setting["tools"]:
        abilities.extend(ref_tools(tool_id, as_agent_tool=True))
    
    for workflow_id in role_setting["workflows"]:
        workflow = ref_workflow(workflow_id, as_agent_tool=True)
        if workflow:
            abilities.append(workflow)
    return abilities


async def agent_chat(bot_setting_file, history, should_exit):
    role_setting = load_role_setting(bot_setting_file)
    abilities = load_abilities(bot_setting_file)

    chat = ChatOpenAI(
        api_key=cfg["apiKey"],
        base_url=cfg["baseURL"],
        model=cfg["model"],
        temperature=(
            role_setting["temperature"] * 2
            if cfg["model"].startswith("deepseek")
            else role_setting["temperature"]
        ),
        stop_sequences=[
            "tool▁calls▁end",
            "tool▁call▁end",
        ],  # 停用deepseek的工具调用标记，不然会虚构工具调用过程和结果
    )
    prompt = role_setting["prompt"]
    if (
        (cfg["model"].startswith("deepseek")
        or cfg["toolCompatibilityMode"])
        and len(abilities) > 0
    ):
        prompt += """
作为一个AI，你如果不确定结果，请务必使用工具查询。
你可以通过下面的方式使用工具，并耐心等待工具返回结果。
如果你需要调用工具，请使用以正确markdown中的json代码格式进行结尾（务必保证json格式正确，不要出现反斜杠未转义等问题）：
```json
{"name": 函数名, "parameters": 参数词典}
```
"""
        if cfg["model"].startswith("yi-"):
            prompt += "\nAvailable functions:\n"
            for t in abilities:
                prompt += f"\n```json\n{json.dumps(convert_to_openai_tool(t))}\n```"
    agent = Runnable(
        agent_execution_mode="FuncCall",
        tools=abilities,
        llm=chat,
        assistant_message=prompt,
        tool_compatibility_mode=cfg["toolCompatibilityMode"],
    )
    result = await run_agent(agent, history, cfg["toolCompatibilityMode"], should_exit)
    if not should_exit.is_set():
        output("assistant", result)