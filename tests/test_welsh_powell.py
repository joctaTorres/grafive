from grafive.algorithms.welsh_powell import welsh_powell
from grafive.utils import graph_from_description


def test_welsh():
    moser_spindle = graph_from_description(
        [
            ("1", "2;4;6"),
            ("2", "1;3;4;5"),
            ("3", "2;5;7"),
            ("4", "1;2;6"),
            ("5", "2;3;7"),
            ("6", "1;4;7"),
            ("7", "3;5;6"),
        ]
    )

    welsh_powell(moser_spindle)
    assert moser_spindle.chromatic_number == 4
