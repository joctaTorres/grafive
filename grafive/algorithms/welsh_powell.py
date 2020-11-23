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

        non_adjacent_nodes = graph.nodes_not_connected_to(node)
        for other_node in non_adjacent_nodes:
            other_node.color = color


unused_colors = [
    Color.BLACK,
    Color.BLUE,
    Color.RED,
    Color.GREEN,
    Color.PINK,
]

def get_new_color() -> Color:
    return unused_colors.pop()