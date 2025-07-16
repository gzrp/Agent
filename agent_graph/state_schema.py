from typing import List, Optional, Dict, Any

from typing_extensions import TypedDict


class ObjectBox(TypedDict):
    label: str
    confidence: float
    bbox: List[float]  # x1, y1, x2, y2


class AgentState(TypedDict):
    """Agent 在图中流动的状态结构"""
    user_text: Optional[str]                        # 用户输入
    image_path: Optional[str]                       # 图像存储路径

    intent: Optional[str]                           # 意图 chat or reasoning

    objects: Optional[List[ObjectBox]]              # 感知阶段感知到的实体

    sql_statements: Optional[List[str]]             # 所有生成的 SQL
    current_sql: Optional[str]                      # 当前处理的 SQL
    current_index: Optional[int]                    # 当前处理的 SQL index
    executed_sqls: Optional[List[str]]              # 已经执行过的 SQL

    query_results: Optional[List[str]]              # 全不查询结果
    filter_results: Optional[List[Dict[str, Any]]]  # 过滤掉空结果
    summary: Optional[str]                          # 大模型总结

    chat_response: Optional[str]                    # 聊天结果


def get_init_agent_state(user_text: str, image_path: str) -> AgentState:
    state: AgentState = {
        "user_text": user_text,
        "image_path": image_path,

        "intent": "",

        "objects": [],

        "sql_statements": [],
        "current_sql": "",
        "current_index": -1,
        "executed_sqls": [],

        "query_results": [],
        "filter_results": [],
        "summary": "",

        "chat_response": "",
    }
    return state
