import io
from unittest.mock import patch

import pytest

from summer_is_coming import universe_factory, utils
from summer_is_coming.breaker_of_chains import HighPriest
from summer_is_coming.universe_competition import (
    UniverseCompetition,
    UniverseCompetitor,
)


@pytest.fixture
def high_priest_and_winner():
    with patch.multiple(UniverseCompetition, __abstractmethods__=set()):
        with patch.multiple(UniverseCompetitor, __abstractmethods__=set()):
            universe = universe_factory.get("Southeros")
            universe_competition = UniverseCompetition(universe)
            competitor = UniverseCompetitor(universe.get_kingdom("Space"))
            competitor.is_competing = True
            competitor2 = UniverseCompetitor(universe.get_kingdom("Land"))
            competitor2.is_competing = True

            water = universe.get_kingdom("Water")
            allegiance_formed = competitor.kingdom.ask_allegiance(
                water, msg=water.emblem
            )
            assert allegiance_formed
            universe_competition._competitors = [competitor, competitor2]

            yield HighPriest(universe_competition), competitor


def test__crown_king(high_priest_and_winner):
    high_priest, winner = high_priest_and_winner
    universe = high_priest._universe_competition.universe

    assert universe._ruler == ""
    for competitor in high_priest._universe_competition._competitors:
        assert not universe.get_kingdom(competitor.kingdom.name)._allies_received

    high_priest._crown_king(winner)

    assert universe._ruler == winner.kingdom.name
    for competitor in high_priest._universe_competition._competitors:
        assert (
            universe.get_kingdom(competitor.kingdom.name)._allies_received
            == competitor.kingdom._allies_received
        )


@patch("sys.stdout", new_callable=io.StringIO)
def test__show_universe_state(stdout_mock, high_priest_and_winner):
    high_priest, winner = high_priest_and_winner
    universe = high_priest._universe_competition.universe
    high_priest._show_universe_state()
    assert (
        stdout_mock.getvalue()
        == "\n"
        + f"Who is the ruler of {universe.name}?\n"
        + f"Output: None\n"
        + "Allies of Ruler?\n"
        + f"Output: None\n"
        + "\n"
    )

    utils.clear_stringio(stdout_mock)
    universe._ruler = winner.kingdom.name
    universe._get_kingdom(
        winner.kingdom.name
    )._allies_received = winner.kingdom._allies_received
    high_priest._show_universe_state()
    assert (
        stdout_mock.getvalue()
        == "\n"
        + f"Who is the ruler of {universe.name}?\n"
        + f"Output: {winner.kingdom.name}\n"
        + "Allies of Ruler?\n"
        + f"Output: {', '.join([ally.name for ally in winner.kingdom._allies_received])}\n"
        + "\n"
    )


def test__choose_ruler(high_priest_and_winner):
    high_priest, winner = high_priest_and_winner
    universe = high_priest._universe_competition.universe

    with patch(
        "summer_is_coming.universe_competition.UniverseCompetition",
        autospec=True,
        winner=winner,
        universe=universe,
    ) as uc_mock:
        high_priest = HighPriest(uc_mock)
        with patch.object(high_priest, "_show_universe_state") as state_mock:
            assert not universe._ruler

            high_priest.choose_ruler()

            uc_mock.register_competitors.assert_called_once()
            uc_mock.commence.assert_called_once()
            uc_mock.evaluate_competitors.assert_called_once()
            uc_mock.show_status.assert_called_once()
            assert state_mock.call_count == 2
            assert uc_mock.universe.ruler == winner.kingdom.name
