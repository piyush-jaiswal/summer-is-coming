from summer_is_coming.breaker_of_chains import HighPriest
from summer_is_coming.universe_competition_factory import BallotFactory


if __name__ == "__main__":
    HighPriest(BallotFactory.get("Southeros")).choose_ruler()
