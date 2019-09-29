from copy import deepcopy

import pytest


def test_equals_operator(kingdoms):
    kingdom, kingdom2, kingdom3 = kingdoms
    assert (kingdom == kingdom2) is False
    assert kingdom == kingdom3


def test__validate_ally(kingdoms):
    kingdom, kingdom2, _ = kingdoms
    assert kingdom._validate_ally(kingdom2) is None
    with pytest.raises(RuntimeError):
        kingdom._validate_ally(kingdom)
        kingdom._validate_ally(deepcopy(kingdom))


def test_give_allegiance(kingdoms):
    kingdom, kingdom2, _ = kingdoms

    allegiance_given = kingdom.give_allegiance(kingdom2, msg="Abc")
    assert allegiance_given is False
    assert kingdom2 not in kingdom.allies_given

    allegiance_given = kingdom.give_allegiance(kingdom2, msg=kingdom.emblem)
    assert allegiance_given is True
    assert kingdom2 in kingdom.allies_given


def test_ask_allegiance(kingdoms):
    kingdom, kingdom2, _ = kingdoms

    allegiance_received = kingdom.ask_allegiance(kingdom2, msg="Abc")
    assert allegiance_received is False
    assert kingdom2 not in kingdom.allies_received

    allegiance_received = kingdom.ask_allegiance(kingdom2, msg=kingdom2.emblem)
    assert allegiance_received is True
    assert kingdom2 in kingdom.allies_received


def test_clear_allegiances(kingdoms):
    kingdom, kingdom2, _ = kingdoms

    kingdom.ask_allegiance(kingdom2, msg=kingdom2.emblem)
    assert len(kingdom.allies_received) != 0

    kingdom.clear_allegiances()
    assert len(kingdom.allies_received) == 0
