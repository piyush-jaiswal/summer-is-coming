import pytest

from summer_is_coming import utils
from summer_is_coming.kingdom import Kingdom


def test_kingdoms_getter(westeros):
    kingdoms = westeros.kingdoms
    for kingdom in kingdoms:
        original_kingdom = utils.sorted_list_get_with_key(westeros._kingdoms, kingdom.name)
        assert kingdom is not original_kingdom


def test_ruler_setter(westeros):
    westeros.ruler = "stark"

    assert westeros.ruler == "Stark"
    with pytest.raises(ValueError):
        westeros.ruler = "tully"


def test_add_kingdoms(westeros):
    tully = Kingdom(name="Tully", emblem="Horse")
    prev_len = len(westeros.kingdoms)
    westeros.add_kingdoms([tully])

    assert westeros.get_kingdom("Tully") == tully
    assert len(westeros.kingdoms) == prev_len + 1

    arryn = Kingdom(name="Arryn", emblem="Eagle")
    arryn._allies_received.add(tully)
    with pytest.raises(RuntimeError):
        westeros.add_kingdoms([arryn])


def test__get_kingdom(westeros):
    assert westeros.get_kingdom("Stark") == utils.sorted_list_get_with_key(westeros._kingdoms, "Stark")
    with pytest.raises(ValueError):
        assert westeros.get_kingdom("Tully")


def test_get_kingdom(westeros):
    assert westeros.get_kingdom("Stark") is not westeros._get_kingdom("Stark")


def test_form_allegiance(westeros):
    assert (
        westeros.form_allegiance(
            sender="Lannister", receiver="Stark", msg="Hand of King"
        )
        is False
    )
    assert westeros.form_allegiance(
        sender="Lannister", receiver="Stark", msg="Kill that direwolf!"
    )

    with pytest.raises(ValueError):
        assert westeros.form_allegiance(
            sender="Tully", receiver="Stark", msg="abcd"
        )
        assert westeros.form_allegiance(
            sender="Stark", receiver="Tully", msg="abcd"
        )
