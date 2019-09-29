from summer_is_coming.kingdom import Kingdom
from summer_is_coming.universe import Universe


def get(universe_name: str):
    universe_name = universe_name.capitalize()
    if universe_name == "Southeros":
        universe = Universe("Southeros")
        universe.add_kingdoms(
            [
                Kingdom(name="Space", emblem="Gorilla"),
                Kingdom(name="Land", emblem="Panda"),
                Kingdom(name="Water", emblem="Octopus"),
                Kingdom(name="Fire", emblem="Dragon"),
                Kingdom(name="Air", emblem="Owl"),
                Kingdom(name="Ice", emblem="Mammoth"),
            ]
        )
        return universe
    else:
        raise ValueError(f"Factory for {universe_name} not present")
