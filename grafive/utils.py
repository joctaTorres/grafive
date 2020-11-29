from grafive.model.graph import Node, Graph


def graph_from_description(description):
    nodes = {}

    def __get_node(node_id):
        node = nodes.get(node_id)

        if not node:
            node = Node(id=int(node_id))
            nodes[node_id] = node
        
        return node


    for node_id, connection_ids in description:
        node = __get_node(node_id)
        
        for connection_id in connection_ids.split(";"):
            connected_node = __get_node(connection_id)

            node.connect(connected_node)


    return Graph(*set(nodes.values()))



