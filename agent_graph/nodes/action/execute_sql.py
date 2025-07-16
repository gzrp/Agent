from pathlib import Path
from typing import List
import duckdb
from langchain_core.tools import tool

from agent_graph.state_schema import AgentState
from common.config_loader import load_config

def get_duckdb_conn():
    config = load_config()
    project_root = Path(__file__).resolve().parents[3]
    db_path = (project_root / config['duckdb']['path']).resolve()
    _duckdb_conn = duckdb.connect(db_path)
    _duckdb_conn.execute("INSTALL spatial;")
    _duckdb_conn.execute("LOAD spatial;")
    return _duckdb_conn

@tool
def execute_sql_query(sql: str) -> List[dict]:
    """
    执行单条 SQL 查询，并返回结果列表（字典形式）。
    :param sql: SQL 语句
    :return: 查询结果
    """
    try:
        conn = get_duckdb_conn()
        result = conn.execute(sql).fetchall()
        columns = [desc[0] for desc in conn.description]
        conn.close()
        # 转为 list[dict]
        return [dict(zip(columns, row)) for row in result]
    except Exception as e:
        return [{"error": str(e)}]

# LangGraph 节点函数
def execute_sql_node(state: AgentState) -> AgentState:
    executed = set(state.get("executed_sqls") or [])
    sql = state.get("current_sql")
    index = str(state.get("current_index"))
    if not sql:
        print("没有可以执行的SQL")
        return state
    print("\n================================[Action Message]================================\n")
    print(f"执行 SQL[{index}]: {sql}")
    result = execute_sql_query.invoke(sql)
    if len(result) == 0:
        print(f"执行结果: []\n")
    else:
        print(f"执行结果: \n")
        print("[")
        for row in result:
            print(f"\t{row}")
        print("]")
    new_state = state.copy()
    executed_sqls = list(executed | {sql})
    new_state["executed_sqls"] = executed_sqls
    query_results = (state.get("query_results") or []) + [result]
    new_state["query_results"] = query_results
    return new_state


if __name__ == '__main__':
    sql_statements =  "SELECT * FROM bank WHERE name LIKE '%落日%';"
    ans = execute_sql_query.invoke(sql_statements)
    print(ans)