from grafive.algorithms.welsh_powell import welsh_powell
from grafive.utils import graph_from_edge

homer = graph_from_edge("samples/homer/homer.edge")

welsh_powell(homer)
