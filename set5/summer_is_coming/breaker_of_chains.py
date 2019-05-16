from summer_is_coming import utils
from summer_is_coming.universe_competition import UniverseCompetition, UniverseCompetitor


class HighPriest:
    _no_ruler = "None"
    _no_allies = "None"

    def __init__(self, universe_competition: UniverseCompetition):
        self._universe_competition = universe_competition

    def _crown_king(self, winner: UniverseCompetitor):
        kingdoms = [
            competitor.kingdom for competitor in self._universe_competition.competitors
        ]
        universe = self._universe_competition.universe

        # setting the allies of the universe in the end prevents the universe state being modified during the competition
        allegiances_formed = [
            universe.form_allegiance(
                sender=kingdom.name, receiver=ally.name, msg=ally.emblem
            )
            for kingdom in kingdoms
            for ally in kingdom.allies_received
        ]
        assert all(allegiances_formed)
        universe.ruler = winner.kingdom.name

    def _show_universe_state(self):
        universe = self._universe_competition.universe
        ruler = universe.ruler if universe.ruler else self._no_ruler
        allies = (
            ", ".join(
                [ally.name for ally in universe.get_kingdom(ruler).allies_received]
            )
            if ruler != self._no_ruler
            else self._no_allies
        )
        utils.show_universe_state(universe.name, ruler, allies)

    def choose_ruler(self):
        self._show_universe_state()
        self._universe_competition.register_competitors()

        self._universe_competition.commence()
        self._universe_competition.evaluate_competitors()
        self._universe_competition.show_status()
        self._crown_king(self._universe_competition.winner)

        self._show_universe_state()


# abstract factory?