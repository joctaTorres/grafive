from __future__ import annotations

from typing import Callable, Set, Hashable
from itertools import combinations
from collections import defaultdict

from contextlib import suppress
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Set
from uuid import uuid4

from grafive.model.color import Color


@dataclass
class Node:
    id: int = field(default_factory=lambda: hash(uuid4()))
    color: Optional[Color] = None
    connections: Set[Node] = field(default_factory=set)
    content: Dict[Any, Any] = field(default_factory=dict)
    update_connection_hook = None

    def __hash__(self):
        return self.id

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __repr__(self):
        return f"Node(id={self.id}, color={self.color}, content={self.content})"

    @property
    def degree(self):
        return len(self.connections)

    def connect(self, node: Node):
        self.connections.add(node)
        node.connections.add(self)

        if self.update_connection_hook:
            self.update_connection_hook(self)

    def connect_all(self, nodes: Set[Node]):
        for node in nodes:
            self.connect(node)

    def disconnect(self, node: Node):
        self.connections.discard(node)
        node.connections.discard(self)

        if self.update_connection_hook:
            self.update_connection_hook(self)


class Graph:
    def __init__(self, *nodes, connection_factory: Callable[[Node], Hashable] = None):
        self.nodes = set(nodes)
        self.connection_factory = connection_factory

        self.connections = {}
        for node in self.nodes:
            self.connections.update({node.id: node.connections})
            node.update_connection_hook = self.update_connection_hook

        if connection_factory:
            self._create_connections()

    def _create_connections(self):
        connection_groups = defaultdict(set)

        for node in self.nodes:
            key = self.connection_factory(node)
            connection_groups[key].add(node)
        
        for group in connection_groups.values():
            for node in group:
                node_connections = group - {node}
                node.connections.update(node_connections)
                self.connections[node.id].update(node_connections)


    def update_connection_hook(self, node):
        self.connections.update({node.id: node.connections})

    def __repr__(self):
        def get_connection_ids(start_node):
            return "-".join([str(node.id) for node in start_node.connections])

        return "\n".join(
            [
                f"[{node.id}][{node.color}] :: {get_connection_ids(node)}"
                for node in self.nodes
            ]
        )

    @property
    def colors(self):
        return {node.color for node in self.nodes if node.color}

    @property
    def chromatic_number(self):
        return len(self.colors)

    def nodes_not_connected_to(self, node):
        not_connected = self.nodes - {node, *node.connections}

        return {
            graph_node
            for graph_node in not_connected
            if node not in graph_node.connections
        }
