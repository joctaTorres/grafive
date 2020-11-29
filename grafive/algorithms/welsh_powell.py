from grafive.model.graph import Node, Graph
from grafive.model.color import Color

from operator import attrgetter


def welsh_powell(graph: Graph):
    sorted_nodes = sorted(
        graph.nodes,
        key=attrgetter("degree"),
        reverse=True
    )

    for node in sorted_nodes:
        if node.color:
            continue

        color = get_new_color()
        node.color = color

        non_adjacent_nodes = sorted(
            graph.nodes_not_connected_to(node),
            key=attrgetter("degree"),
            reverse=True
        )

        nodes_not_to_color = set()
        for non_adjacent_node in non_adjacent_nodes:
            if non_adjacent_node in nodes_not_to_color:
                continue
            nodes_not_to_color.update(non_adjacent_node.connections)
    
        nodes_to_color = set(non_adjacent_nodes) - nodes_not_to_color

        for node_to_color in nodes_to_color:
            node_to_color.color = color


unused_colors = [
    Color.BLACK,
    Color.BLUE,
    Color.RED,
    Color.GREEN,
    Color.PINK,
]

def get_new_color() -> Color:
    return unused_colors.pop()