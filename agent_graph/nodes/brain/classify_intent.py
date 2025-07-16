
from agent_graph.state_schema import AgentState, get_init_agent_state
from llm.qwen_wrapper import QwenWrapper


def classify_intent_node(state: AgentState) -> AgentState:
    user_input = state.get("user_text", "")
    qwen = QwenWrapper()
    messages = [
        {
            "role": "system",
            "content": (
                "你是一个意图分类助手，只能在两个标签中选择一个：\n"
                "1. chat：表示用户只是想聊天或问问题\n"
                "2. reasoning：表示用户上传了图片并希望分析拍摄地点、识别位置或推理地理相关信息\n"
                "请你严格只回复一个标签：chat 或 reasoning，不要添加其他内容。"
            )
        },
        {
            "role": "user",
            "content": f"用户输入如下：\n{user_input}\n请判断用户的意图类型："
        }
    ]
    intent = qwen.chat(messages).strip().lower()
    if intent not in {"chat", "reasoning"}:
        intent = "chat"
    new_state = state.copy()
    new_state["intent"] = intent
    return new_state

def route_intent_condition(state: AgentState):
    return state.get("intent")


if __name__ == '__main__':
    test_cases = [
        # 🔵 聊天类输入
        "你好，你是谁？",
        "北京最近天气怎么样？",
        "你可以给我讲个笑话吗？",
        "帮我查一下AI的最新发展。",
        "你觉得马斯克怎么样？",

        # 🟢 图片分析类输入
        "请识别这张图的拍摄地点。",
        "我上传了一张照片，帮我看看是在哪里拍的？",
        "这张图好像是在海边，你能确认下具体位置吗？",
        "请分析这张图背后的地理信息。",
        "图中建筑像是法国的某个地方，你能帮我判断一下吗？"
    ]
    for input_text in test_cases:
        print(f"\n=== 测试输入 ===\n{input_text}\n")
        # 构造状态
        case_state: AgentState = get_init_agent_state(input_text, "xxx.png")

        # 调用分类节点
        updated_state = classify_intent_node(case_state)

        # 输出意图判断结果
        print(f"👉 识别意图：{updated_state.get('intent')}")