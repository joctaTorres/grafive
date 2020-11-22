from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Set

from uuid import uuid4 , UUID

from grafive.model.color import Color


@dataclass
class Node:
    id: int = field(default_factory= lambda: hash(uuid4()))
    color: Color = Color.BLACK
    connections: Set[Node] = field(default_factory=set)

    def __hash__(self):
        return self.id
    
    @property
    def degree(self):
        return len(self.connections)


class Graph:
    def __init__(self, *nodes):
        self.nodes = set(nodes)
