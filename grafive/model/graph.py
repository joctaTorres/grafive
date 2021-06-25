from __future__ import annotations

from collections import defaultdict
from typing import Any, Callable, Dict, Hashable, Optional, Set
from uuid import uuid4

from grafive.model.color import Color


class Node:
    def __init__(
        self,
        node_id: int = None,
        color: Optional[Color] = None,
        connections: Set[Node] = None,
        content: Dict[Any, Any] = None,
    ):
        self.id = node_id or hash(uuid4())
        self.color = color
        self._connections: Set[Node] = connections or set()
        self.content: Dict[Any, Any] = content or {}

        # hooks
        self.update_connection_hook = None
        self.use_connection_hook = None

        # connection factory helpers
        self.connection_key = None
        self.connections_found = False

    def __hash__(self):
        return self.id

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __repr__(self):
        return f"Node(id={self.id}, color={self.color}, content={self.content})"

    @property
    def connections(self):
        if self.use_connection_hook:
            return self.use_connection_hook(self)

        return self._connections

    @property
    def degree(self):
        return len(self.connections)

    def connect(self, node: Node):
        self._connections.add(node)
        node._connections.add(self)

        if self.update_connection_hook:
            self.update_connection_hook(self)

    def connect_all(self, nodes: Set[Node]):
        for node in nodes:
            self.connect(node)

    def disconnect(self, node: Node):
        self._connections.discard(node)
        node._connections.discard(self)

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
            node.use_connection_hook = self.use_connection_hook

        if connection_factory:
            self._create_connections()

    def _create_connections(self):
        # foo
        self.connection_groups = defaultdict(set)

        for node in self.nodes:
            connection_key = self.connection_factory(node)
            node.connection_key = connection_key
            try:
                keys = iter(connection_key)
                for key in keys:
                    self.connection_groups[key].add(node)
            except TypeError:
                self.connection_groups[connection_key].add(node)

    def update_connection_hook(self, node):
        self.connections.update({node.id: node.connections})

    def use_connection_hook(self, node):
        if not node.connection_key or node.connections_found:
            return self.connections[node.id]

        connection_key = node.connection_key
        try:
            keys = iter(connection_key)
            connected_nodes = set()
            for key in keys:
                connected_nodes.update(self.connection_groups[key])
        except TypeError:
            connected_nodes = self.connection_groups[connection_key]

        node_connections = self.connections[node.id] | (connected_nodes - {node})
        self.connections[node.id] = node_connections
        node.connections_found = True

        return node_connections

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
