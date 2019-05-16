from typing import Tuple, List, Iterable

from summer_is_coming import universe_factory
from summer_is_coming import utils
from summer_is_coming.universe import Universe


class GoldenCrown:
    _no_ruler = 'None'
    _no_allies = 'None'

    def __init__(self, king: str, kingdom_name: str, universe: Universe, allies_needed: int):
        self.king = king.capitalize()
        self.kingdom_name = kingdom_name.capitalize()
        self.universe = universe
        self.allies_needed = allies_needed
        self._validate_kingdom()

    def _validate_kingdom(self):
        self.universe.get_kingdom(self.kingdom_name.capitalize())

    def _process_input(self, user_input: str) -> (str, str):
        kingdom_name, msg = user_input.split(",")
        kingdom_name = kingdom_name.strip()
        if kingdom_name == self.kingdom_name:
            raise RuntimeError("Kingdom {} cannot form allegiance with itself".format(self.kingdom_name))

        msg = msg.strip()
        msg = msg.strip('"')

        return kingdom_name, msg

    def _get_input_messages(self) -> List[Tuple[str, str]]:
        n = int(input("No of messages: "))
        print(f"Input Messages to kingdoms from King {self.king}:")
        inputs = [self._process_input(input("Input: ")) for _ in range(n)]
        print()
        return inputs

    def _send_message(self, receiver: str, msg: str) -> bool:
        return self.universe.form_allegiance(sender=self.kingdom_name, receiver=receiver, msg=msg)

    def _get_support(self) -> List[bool]:
        replies = [self._send_message(kingdom_name, msg) for kingdom_name, msg in self._get_input_messages()]
        return replies

    def _is_strong(self, replies: Iterable[bool]) -> bool:
        return sum(1 for reply in replies if reply is True) >= self.allies_needed

    def show_state(self):
        king = self.king if self.universe.ruler == self.kingdom_name else self._no_ruler
        if king == self.king:
            ruling_kingdom = self.universe.get_kingdom(self.universe.ruler)
            allies = ", ".join([ally.name for ally in ruling_kingdom.allies_received])
        else:
            allies = self._no_allies
        utils.show_universe_state(self.universe.name, king, allies)

    def _claim_crown(self):
        self.universe.ruler = self.kingdom_name

    def conquer(self):
        self.show_state()
        replies = self._get_support()
        if self._is_strong(replies):
            self._claim_crown()
        self.show_state()


class GoldenCrownFactory:
    @staticmethod
    def get(king: str) -> GoldenCrown:
        king = king.capitalize()

        if king == "Shan":
            return GoldenCrown(
                king="Shan",
                kingdom_name="Space",
                universe=universe_factory.get("Southeros"),
                allies_needed=3,
            )
        else:
            raise ValueError("King {} cannot obtain a golden crown!".format(king))
