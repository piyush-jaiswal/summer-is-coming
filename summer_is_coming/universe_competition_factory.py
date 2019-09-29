from abc import abstractmethod, ABC

from summer_is_coming import universe_factory
from summer_is_coming.ballot import Ballot
from summer_is_coming.universe_competition import UniverseCompetition


class UniverseCompetitionFactory(ABC):
    @staticmethod
    @abstractmethod
    def get(*args, **kwargs) -> UniverseCompetition:
        pass


class BallotFactory(UniverseCompetitionFactory):
    @staticmethod
    def get(universe_name: str) -> UniverseCompetition:
        universe_name = universe_name.capitalize()

        if universe_name == "Southeros":
            return Ballot(universe_factory.get("Southeros"), no_of_messages=6)
        else:
            raise ValueError(f"No Ballot competition available for universe '{universe_name}'")
