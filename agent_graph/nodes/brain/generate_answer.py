from agent_graph.state_schema import AgentState
from llm.qwen_wrapper import QwenWrapper

def generate_answer_node(state: AgentState) -> AgentState:
    user_question = state.get("user_text")
    qwen = QwenWrapper()
    prompt = f"""用户提问如下：
            “{user_question}”

            以下是系统生成的完整图像分析报告内容，请你根据其中的信息，包括物体识别、SQL生成与执行结果等，综合判断回答用户的问题，給出最多5个最有可能的拍摄位置，并给出具体的原因：
            
            识别到的物体：{state.get("objects")}

            生成的SQL：{state.get("sql_statements")}
            
            有效SQL的执行结果：{state.get("filter_results")}

            请只输出你的最终回答，不要复述报告内容。"""

    messages = [
        {"role": "system", "content": "你是一个图像与地理位置推理专家。"},
        {"role": "user", "content": prompt}
    ]
    print(prompt)
    chat_response = qwen.chat(messages)
    new_state = state.copy()
    new_state["summary"] = chat_response
    print("\n================================[Brain Message]=================================\n")
    print(chat_response)
    return new_state



