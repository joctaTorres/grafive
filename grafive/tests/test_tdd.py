from grafive.model.graph import Node, Graph
from grafive.model.color import Color

def test_node_hash():
    foo = Node()
    bar =  Node()

    assert foo != bar

def test_node():
    foo = Node()
    assert foo
    assert foo.connections == set()

    foo = Node(color=Color.RED)
    assert foo.color == Color.RED

    bar = Node(connections={foo})
    assert bar.connections == {foo}
    assert bar.degree == 1

    whatever = Node(connections={foo, bar})
    assert whatever.degree == 2


def test_graph():
    graph = Graph()
    assert graph
    assert graph.nodes == set()

    foo = Node()
    bar =  Node()

    graph = Graph(foo)
    assert graph.nodes == {foo}

    graph = Graph(foo, bar)
    assert graph.nodes == {foo, bar}