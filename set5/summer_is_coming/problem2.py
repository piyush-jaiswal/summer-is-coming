from summer_is_coming.ballot_system import Ballot
from summer_is_coming import universe_factory
from summer_is_coming.breaker_of_chains import HighPriest


if __name__ == "__main__":
    HighPriest(
        Ballot(universe_factory.get("Southeros"), no_of_messages=3)
    ).choose_ruler()
