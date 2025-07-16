import dashscope
from typing import List

class QwenWrapper:
    def __init__(self):
        self.api_key = "sk-bcabe4992cb94e8f896126cef8ee8dea"
        self.base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1/"
        self.model = "qwen2.5-72b-instruct"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def chat(self, messages: List, temperature: float = 0.7) -> str:
        """
        调用 Qwen 接口生成回复。

        messages: List of dicts, e.g. [{"role": "user", "content": "你是谁？"}]
        """
        try:
            resp = dashscope.Generation.call(
                api_key=self.api_key,
                model=self.model,
                messages=messages,
                result_format="message",
                temperature=temperature,
                top_p = 0.8
            )
            if (
                    hasattr(resp, "output")
                    and "choices" in resp.output
                    and resp.output["choices"]
            ):
                return resp.output["choices"][0]["message"]["content"]
            else:
                return "【无有效回复】"
        except Exception as e:
            return f"【调用异常】{str(e)}"


if __name__ == '__main__':
    qwen = QwenWrapper()
    messages = [
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': '你是谁？'}
    ]
    response = qwen.chat(messages)
    print(response)