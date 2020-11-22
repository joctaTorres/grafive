from grafive.model.graph import Node, Graph

def test_node_hash():
    foo = Node()
    bar =  Node()

    assert foo != bar


def test_graph_creation():
    graph = Graph()
    assert graph

    foo = Node()
    bar =  Node()

    graph = Graph(foo)
    assert graph.nodes == {foo}

    graph = Graph(foo, bar)
    assert graph.nodes == {foo, bar}