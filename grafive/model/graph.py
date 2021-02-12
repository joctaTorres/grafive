from __future__ import annotations

from typing import Callable, Set
from itertools import combinations

from contextlib import suppress
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Set
from uuid import uuid4

from grafive.model.color import Color


@dataclass
class Node:
    id: int = field(default_factory= lambda: hash(uuid4()))
    color: Optional[Color] = None
    connections: Set[Node] = field(default_factory=set)
    content: Dict[Any, Any] = field(default_factory=dict)

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

    def disconnect(self, node: Node):
        with suppress(KeyError):
            self.connections.remove(node)



class Graph:
    def __init__(
        self,
        *nodes,
        connection_factory: Callable[[Node, Node], bool]=None
    ):
        self.nodes = set(nodes)
        self.connection_factory = connection_factory

        if connection_factory:
            self._create_connections()

    def _create_connections(self):
        for node, other_node in combinations(self.nodes, 2):
            should_connect = self.connection_factory(node, other_node)
            if should_connect:
                node.connect(other_node)
            
    def __repr__(self):
        def get_connection_ids(start_node):
            return "-".join([str(node.id) for node in start_node.connections])

        return "\n".join([f"[{node.id}][{node.color}] :: {get_connection_ids(node)}" for node in self.nodes])

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

