from agent_graph.state_schema import AgentState


def sql_router_node(state: AgentState) -> AgentState:
    executed = set(state.get("executed_sqls") or [])
    sql_list = state.get("sql_statements") or []
    remaining = [sql for sql in sql_list if sql not in executed]

    if not remaining:
        return state

    current_sql = remaining[0]
    # executed_sqls = list(executed | {current_sql})

    new_state = state.copy()
    new_state["current_sql"] = current_sql
    new_state["current_index"] = len(executed) + 1
    # new_state["executed_sqls"] = executed_sqls
    return new_state


def route_sql_condition(state: AgentState):
    remaining = set(state.get("sql_statements") or []) - set(state.get("executed_sqls") or [])
    # print("continue" if remaining else "done")
    return "continue" if remaining else "done"