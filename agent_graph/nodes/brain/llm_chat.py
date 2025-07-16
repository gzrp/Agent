from agent_graph.state_schema import AgentState, get_init_agent_state
from llm.qwen_wrapper import QwenWrapper


def llm_chat_node(state: AgentState) -> AgentState:
    user_text = state.get("user_text", "")
    qwen = QwenWrapper()

    messages = [
        {"role": "system", "content": "你是一个乐于助人的中文助手。"},
        {"role": "user", "content": user_text}
    ]
    chat_response = qwen.chat(messages)
    new_state = state.copy()
    new_state["chat_response"] = chat_response
    print("\n================================[Brain Message]=================================\n")
    print(chat_response)
    return new_state


if __name__ == '__main__':
    test_cases = [
        "你好，今天天气怎么样？",
        "你是谁？",
        "能给我讲个笑话吗？",
        "帮我推荐几本好书。",
        "什么是量子纠缠？"
    ]

    for input_text in test_cases:
        case_state: AgentState = get_init_agent_state(input_text, "")
        updated_state = llm_chat_node(case_state)
        # 输出模型回复
        print(f"问题：{input_text}")
        print("💬 模型回复：")
        print(updated_state.get("chat_response", "无回复"))
