from grafive.model.color import Color
from grafive.model.graph import Graph, Node


def test_node_hash_eq():
    foo = Node()
    bar = Node()

    assert foo != bar

    foo = Node(id=42)
    bar = Node(id=42)

    assert foo == bar


def test_node():
    foo = Node()
    assert foo
    assert foo.connections == set()
    assert foo.degree == 0

    foo = Node(color=Color.RED)
    assert foo.color == Color.RED

    bar = Node(connections={foo})
    assert bar.connections == {foo}
    assert bar.degree == 1

    whatever = Node(connections={foo, bar})
    assert whatever.degree == 2


def test_node_connect():
    foo = Node()
    bar = Node()

    foo.connect(bar)
    assert foo.degree == 1

    foo.disconnect(bar)
    assert foo.degree == 0

    # test supress
    foo.disconnect(bar)


def test_graph():
    graph = Graph()
    assert graph
    assert graph.nodes == set()

    foo = Node()
    bar = Node()

    graph = Graph(foo)
    assert graph.nodes == {foo}

    graph = Graph(foo, bar)
    assert graph.nodes == {foo, bar}


def test_graph_chromatic_number():
    foo = Node(color=Color.RED)
    bar = Node(color=Color.BLUE)
    bar_again = Node(color=Color.BLUE)

    graph = Graph(foo, bar, bar_again)
    assert graph.chromatic_number == 2
