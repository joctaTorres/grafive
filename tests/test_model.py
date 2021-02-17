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
    assert bar.degree == 1
    assert foo.connections == {bar}
    assert bar.connections == {foo}

    foo.disconnect(bar)
    assert foo.degree == 0
    assert bar.degree == 0
    assert foo.connections == set()
    assert bar.connections == set()

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


def test_graph_connections():
    red_one = Node(color=Color.RED)
    red_two = Node(color=Color.RED)
    blue_one = Node(color=Color.BLUE)
    blue_two = Node(color=Color.BLUE)

    nodes = {red_one, red_two, blue_one, blue_two}

    def factory_method(node):
        return node.color

    graph = Graph(*nodes, connection_factory=factory_method)

    assert red_one.connections == {red_two}
    assert red_two.connections == {red_one}
    assert blue_one.connections == {blue_two}
    assert blue_two.connections == {blue_one}


def test_graph_multiple_connections():
    content_one = {"number": 1}
    content_two = {"number": 2}

    red_one = Node(color=Color.RED, content=content_one)
    red_two = Node(color=Color.RED, content=content_two)

    blue_one = Node(color=Color.BLUE, content=content_one)
    blue_two = Node(color=Color.BLUE, content=content_two)

    nodes = {red_one, red_two, blue_one, blue_two}

    def factory_method(node):
        return node.color, node.content["number"]

    graph = Graph(*nodes, connection_factory=factory_method)

    assert red_one.connections == {red_two, blue_one}
    assert red_two.connections == {red_one, blue_two}
    assert blue_one.connections == {blue_two, red_one}
    assert blue_two.connections == {blue_one, red_two}


def test_graph_node_connect_hook():
    foo = Node(1)
    bar = Node(2)

    graph = Graph(foo, bar)

    assert graph.connections == {
        1: set(),
        2: set(),
    }

    # connection to a node updates graph connection state
    foo.connect(bar)
    assert foo.connections == {bar}
    assert bar.connections == {foo}
    assert graph.connections == {
        1: {bar},
        2: {foo},
    }

    foo.disconnect(bar)
    assert foo.connections == set()
    assert bar.connections == set()
    assert graph.connections == {
        1: set(),
        2: set(),
    }
