from operator import attrgetter

from grafive.model.color import iterate_colors
from grafive.model.graph import Graph


def welsh_powell(graph: Graph, color_generator=iterate_colors()):
    sorted_nodes = sorted(
        graph.nodes,
        key=attrgetter("degree"),
        reverse=True
    )

    for node in sorted_nodes:
        if node.color:
            continue

        color = next(color_generator)
        node.color = color

        non_adjacent_nodes = {
            node
            for node in
            graph.nodes_not_connected_to(node)
            if not node.color
        }

        non_adjacent_nodes_sorted = sorted(
            non_adjacent_nodes,
            key=attrgetter("degree"),
            reverse=True
        )

        nodes_not_to_color = set()
        for non_adjacent_node in non_adjacent_nodes_sorted:
            if non_adjacent_node in nodes_not_to_color:
                continue
            nodes_not_to_color.update(non_adjacent_node.connections)
    
        nodes_to_color = non_adjacent_nodes - nodes_not_to_color

        for node_to_color in nodes_to_color:
            node_to_color.color = color
