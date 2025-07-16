from typing import List, Dict, Any
from langchain_core.tools import tool

from agent_graph.state_schema import AgentState

@tool
def filter_results(sql_statements: List[str], query_results: List[List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    """
    过滤掉查询结果为空的 SQL，将有结果的 SQL 和数据组合输出。
    :param sql_statements: SQL语句列表
    :param query_results: 每条SQL语句的查询结果
    :return: 包含有实际结果的 SQL + Result 对
    """
    valid_results = []
    for sql, result in zip(sql_statements, query_results):
        if isinstance(result, list) and len(result) > 0:
            valid_results.append({
                "sql": sql,
                "result": result
            })
    return valid_results

def filter_result_node(state: AgentState) -> AgentState:
    """
    过滤掉查询结果为空的 SQL，将有结果的 SQL 和数据组合输出。
    """
    print("\n================================[Brain Message]=================================\n")
    print("根据执行的SQL和查询结果，汇总有效结果：")
    results = filter_results.invoke({
        "sql_statements": state["sql_statements"],
        "query_results": state["query_results"]
    })

    for i, res in enumerate(results, 1):
        print(f"\n有效SQL: {res.get('sql')}")
        print(f"执行结果：")
        result = res.get("result")
        print("[")
        for row in result:
            print(f"\t {row}")
        print("]")
    new_state = state.copy()
    new_state["filter_results"] = results

    print("\n根据置信度，这张图片最有可能拍摄于一下地点之一：")
    for i, res in enumerate(results, 1):
        result = res.get("result")
        # print("[")
        k = 0
        for idx, row in enumerate(result, 1):
            print(f"[{idx}]: {row}")
        # print("]")
        if i>0:
            break

    return new_state