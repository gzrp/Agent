import re
from typing import List, Optional

from agent_graph.state_schema import ObjectBox, AgentState
from langchain_core.tools import tool

def compare_relative_longitude(a: ObjectBox, b: ObjectBox, sunset: ObjectBox) -> str:
    """判断 a 相对 b 是在 sunset 的西侧还是东侧"""
    def cx(box: ObjectBox) -> float:
        return (box['bbox'][0] + box['bbox'][2]) / 2.0
    sunset_cx = cx(sunset)
    a_cx = cx(a)
    b_cx = cx(b)
    return "WEST" if abs(a_cx - sunset_cx) < abs(b_cx - sunset_cx) else "EAST"

def generate_spatial_sql(a: ObjectBox, b: ObjectBox, sunset: Optional[ObjectBox]) -> str:
    direction_condition = ""
    if sunset:
        direction = compare_relative_longitude(a, b, sunset)
        if direction == "WEST":
            direction_condition = " AND ST_X(a.location) <= ST_X(b.location) "
        else:
            direction_condition = " AND ST_X(b.location) <= ST_X(a.location) "

    sql = f"""
        WITH geo_a AS (
            SELECT * FROM geo_table WHERE name LIKE '%{a['label']}%'
        ), geo_b AS (
            SELECT * FROM geo_table WHERE name LIKE '%{b['label']}%'
        )
        SELECT
            a.name AS a_name,
            a.address AS a_address,
            b.name AS b_name,
            b.address AS b_address,
            ROUND((st_distance(a.location, b.location) / 0.0111) * 1000) AS distance
        FROM geo_a AS a
        JOIN geo_b AS b ON 1=1
        WHERE 1=1 AND distance > 1 AND distance < 100
        {direction_condition}
        ORDER BY distance
        LIMIT 3;
    """
    return re.sub(r'\s+', ' ', sql.strip())
    # return sql.strip()

@tool
def generate_sql_queries(objects: List[ObjectBox]) -> List[str]:
    """
    根据检测到物体变迁生成 SQL 查询语句
    :param objects: 检测的物体
    :return: SQLs
    """
    sql_list = []
    sunset_obj = next((obj for obj in objects if obj["label"] == "夕阳"), None)
    # 枚举所有可能的组合 a != b
    for i in range(len(objects)):
        for j in range(i + 1, len(objects)):
            obj_a = objects[i]
            obj_b = objects[j]

            if obj_a["label"] == "夕阳" or obj_b["label"] == "夕阳" or obj_a["label"] == obj_b["label"]:
                continue  # 落日仅作参考不参与查询, 相同的 label 也跳过
            sql = generate_spatial_sql(obj_a, obj_b, sunset_obj)
            sql_list.append(sql)
    return sql_list

# LangGraph 节点函数
def generate_sql_node(state: AgentState) -> AgentState:
    print("\n================================[Brain Message]=================================\n")
    print("根据识别的实体，生成如下可能的 SQL：")
    sqls = generate_sql_queries.invoke({"objects": state["objects"] or []})
    sql_statements = (state["sql_statements"] or []) + sqls
    for i, sql in enumerate(sql_statements, 1):
        print(f"[{i}] {sql}")
    new_state = state.copy()
    new_state["sql_statements"] = sql_statements
    return new_state


if __name__ == "__main__":
    test_objects = [
        ObjectBox(label="银行", confidence=0.95, bbox=[30, 150, 130, 210]),
        ObjectBox(label="落日", confidence=0.90, bbox=[100, 120, 150, 170]),
    ]
    res = generate_sql_queries.invoke({"objects": test_objects})
    for i, sql in enumerate(res, 1):
        print(f"[{i}] {sql}")