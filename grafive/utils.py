from collections import defaultdict

from grafive.model.graph import Graph, Node


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


def graph_from_csv(path):
    def csv_line_generator(path):
        with open(path, "r") as csv_file:
            for line in csv_file:
                line = line.strip()
                yield line.split(",")

    return graph_from_description(csv_line_generator(path))


def graph_from_edge(path):
    def edge_line_generator(path):
        with open(path, "r") as edge_file:
            for line in edge_file:
                line = line.strip()
                yield line.split(" ")

    edge_generator = edge_line_generator(path)

    # ignore header
    next(edge_generator)

    node_connections = defaultdict(list)
    for _, node, connection in edge_generator:
        node_connections[node].append(connection)

    def description_generator(node_connections):
        for key, values in node_connections.items():
            values = ";".join(values) or ""
            yield (key, values)

    return graph_from_description(description_generator(node_connections))
