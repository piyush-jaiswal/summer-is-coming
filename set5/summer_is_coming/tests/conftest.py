import pytest

from summer_is_coming.kingdom import Kingdom
from summer_is_coming.universe import Universe


@pytest.fixture
def westeros():
    universe = Universe("Westeros")
    universe.add_kingdoms([
        Kingdom(name="Stark", emblem="Direwolf"),
        Kingdom(name="Lannister", emblem="Lion"),
        Kingdom(name="Targareyan", emblem="Dragon")
    ])

    return universe


@pytest.fixture
def kingdoms():
    return [
        Kingdom(name="Land", emblem="paNda"),
        Kingdom(name="Air", emblem="owl"),
        Kingdom(name="Land", emblem="elephant")
    ]
