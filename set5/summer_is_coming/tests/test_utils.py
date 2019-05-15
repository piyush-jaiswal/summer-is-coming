import io
from unittest.mock import patch

import pytest
from sortedcontainers import SortedKeyList

from summer_is_coming import utils


def test_sorted_list_get_with_key():
    sorted_list = SortedKeyList([(1, 3), (2, 2), (3, 1)], key=lambda x: x[1])
    assert utils.sorted_list_get_with_key(sorted_list, 1) == (3, 1)
    assert utils.sorted_list_get_with_key(sorted_list, 2) == (2, 2)
    with pytest.raises(ValueError):
        utils.sorted_list_get_with_key(sorted_list, 10)


def test_clear_stringio():
    stringio = io.StringIO()

    stringio.write("Hello World")
    assert stringio.getvalue() == "Hello World"

    utils.clear_stringio(stringio)
    assert stringio.getvalue() == ""


@patch("sys.stdout", new_callable=io.StringIO)
def test_show_universe_state(stdout):
    universe_name = "southeros"
    king = "Shan"
    allies = "Ice, Land"
    utils.show_universe_state(universe_name=universe_name, king=king, allies=allies)
    assert (
        stdout.getvalue()
        == "\n"
        + f"Who is the ruler of {universe_name}?\n"
        + f"Output: {king}\n"
        + "Allies of Ruler?\n"
        + f"Output: {allies}\n"
        + "\n"
    )
