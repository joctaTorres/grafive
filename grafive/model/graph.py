from __future__ import annotations

from contextlib import suppress
from dataclasses import dataclass, field
from typing import Any, Set, Optional, Dict

from uuid import uuid4 , UUID

from grafive.model.color import Color


@dataclass
class Node:
    id: int = field(default_factory= lambda: hash(uuid4()))
    color: Optional[Color] = None
    connections: Set[Node] = field(default_factory=set)
    content: Dict[Any, Any] = field(default_factory=dict)

    def __hash__(self):
        return self.id
    
    def __repr__(self):
        return f"Node(id={self.id}, color={self.color}, content={self.content})"
    
    @property
    def degree(self):
        return len(self.connections)
    
    def connect(self, node: Node):
        self.connections.add(node)

    def disconnect(self, node: Node):
        with suppress(KeyError):
            self.connections.remove(node)



class Graph:
    def __init__(self, *nodes):
        self.nodes = set(nodes)

