from grafive.algorithms.welsh_powell import welsh_powell
from grafive.model.color import random_unique_color
from grafive.utils import graph_from_edge

heule = graph_from_edge("samples/heule_529/529.edge")

welsh_powell(heule, color_generator=random_unique_color())
