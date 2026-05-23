from app.schemas.pipeline import EdgeSchema, NodeSchema


def check_is_dag(nodes: list[NodeSchema], edges: list[EdgeSchema]) -> bool:
    """Check whether the directed graph is acyclic using DFS cycle detection."""
    adj_list: dict[str, list[str]] = {node.id: [] for node in nodes}

    for edge in edges:
        if edge.source in adj_list and edge.target in adj_list:
            adj_list[edge.source].append(edge.target)

    visit_state: dict[str, int] = {node.id: 0 for node in nodes}

    def has_cycle(node_id: str) -> bool:
        visit_state[node_id] = 1

        for neighbor in adj_list.get(node_id, []):
            if visit_state[neighbor] == 1:
                return True

            if visit_state[neighbor] == 0 and has_cycle(neighbor):
                return True

        visit_state[node_id] = 2
        return False

    for node in nodes:
        if visit_state[node.id] == 0 and has_cycle(node.id):
            return False

    return True
