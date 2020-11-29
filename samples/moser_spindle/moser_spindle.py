from grafive.algorithms.welsh_powell import welsh_powell
from grafive.utils import graph_from_csv

moser_spindle = graph_from_csv("samples/moser_spindle/moser_spindle.csv")

welsh_powell(moser_spindle)
