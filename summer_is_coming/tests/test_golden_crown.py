import io
from unittest.mock import patch

import pytest

from summer_is_coming import utils
from summer_is_coming.golden_crown import GoldenCrownFactory


@pytest.fixture
def shan_golden_crown():
    return GoldenCrownFactory.get("Shan")


@pytest.fixture
def input_mock():
    with patch(
        "builtins.input",
        side_effect=[
            "3",
            'Air, "oaaawaala"',
            'Land, "a1d22n333a4444p"',
            'Ice, "zmzmzmzaztzozh"',
        ],
    ) as input_mock:
        yield input_mock


def test__validate_kingdom(shan_golden_crown):
    shan_golden_crown.kingdom_name = "Dummy"
    with pytest.raises(ValueError):
        shan_golden_crown._validate_kingdom()


def test__process_input(shan_golden_crown):
    assert shan_golden_crown._process_input('Air, "oaaawaala"') == ("Air", "oaaawaala")
    assert shan_golden_crown._process_input('Land, "a1d22n333a4444p"') == (
        "Land",
        "a1d22n333a4444p",
    )
    with pytest.raises(RuntimeError):
        shan_golden_crown._process_input('Space, "Gorilla"')


def test__get_input_messages(shan_golden_crown, input_mock):
    assert shan_golden_crown._get_input_messages() == [
        ("Air", "oaaawaala"),
        ("Land", "a1d22n333a4444p"),
        ("Ice", "zmzmzmzaztzozh"),
    ]


def test__send_message(shan_golden_crown):
    assert shan_golden_crown._send_message(receiver="Land", msg="Panda") is True
    assert shan_golden_crown._send_message(receiver="Water", msg="Panda") is False


def test__get_support(shan_golden_crown, input_mock):
    assert shan_golden_crown._get_support() == [True, True, True]


def test__is_strong(shan_golden_crown):
    assert shan_golden_crown._is_strong([True, True]) is False
    assert shan_golden_crown._is_strong([True, True, True]) is True
    assert shan_golden_crown._is_strong([True, True, True, True]) is True
    assert shan_golden_crown._is_strong([True, True, False, True]) is True
    assert shan_golden_crown._is_strong([False]) is False


@patch("sys.stdout", new_callable=io.StringIO)
def test_show_state(stdout_patch, shan_golden_crown):
    universe = shan_golden_crown.universe
    shan_golden_crown.show_state()
    assert (
        stdout_patch.getvalue()
        == "\nWho is the ruler of Southeros?\nOutput: None\nAllies of Ruler?\nOutput: None\n\n"
    )

    utils.clear_stringio(stdout_patch)
    universe.ruler = "Space"
    kingdom = universe._get_kingdom("Space")
    kingdom._allies_received.add(universe._get_kingdom("Water"))
    kingdom._allies_received.add(universe._get_kingdom("Air"))

    shan_golden_crown.show_state()
    assert (
        stdout_patch.getvalue()
        == "\nWho is the ruler of Southeros?\nOutput: Shan\nAllies of Ruler?\nOutput: Air, Water\n\n"
    )


def test__claim_crown(shan_golden_crown):
    shan_golden_crown._claim_crown()
    assert shan_golden_crown.universe.ruler == shan_golden_crown.kingdom_name


@patch("sys.stdout", new_callable=io.StringIO)
def test_conquer(stdout_patch, shan_golden_crown, input_mock):
    shan_golden_crown.conquer()
    assert shan_golden_crown.universe.ruler == "Space"
    assert (
        stdout_patch.getvalue()
        == "\nWho is the ruler of Southeros?\nOutput: None\nAllies of Ruler?\nOutput: None\n\n"
        + "Input Messages to kingdoms from King Shan:\n\n"
        + "\nWho is the ruler of Southeros?\nOutput: Shan\nAllies of Ruler?\nOutput: Air, Ice, Land\n\n"
    )
