from grafive.model.graph import Node, Graph
from grafive.algorithms.welsh_powell import welsh_powell

def test_welsh():
    graph = Graph()
    assert graph
    assert graph.nodes == set()

    one = Node(content={"name":"one"})
    two =  Node(content={"name":"two"})
    three = Node(
        connections= {
            one, two
        },
        content={"name":"three"}
    )
    four = Node(
        connections={
            three
        },
        content={"name":"two"}
    )

    five = Node(
        connections={
            four
        },
        content={"name":"five"}
    )
    graph = Graph(one, two, three, four, five)

    welsh_powell(graph)

    assert one.color == two.color == four.color
    assert three.color == five.color
    assert one.color != three.color
