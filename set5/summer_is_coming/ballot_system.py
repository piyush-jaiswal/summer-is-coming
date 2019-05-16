from __future__ import annotations

import random
from copy import deepcopy
from dataclasses import dataclass
from os import path
from typing import List, Iterable, Callable

from num2words import num2words
from sortedcontainers import SortedKeyList

from summer_is_coming import utils
from summer_is_coming.kingdom import Kingdom
from summer_is_coming.universe import Universe
from summer_is_coming.universe_competition import (
    UniverseCompetitor,
    UniverseCompetition,
)


@dataclass
class BallotMessage:
    sender: BallotKingdom
    receiver: BallotKingdom
    msg: str


class BallotKingdom(UniverseCompetitor):
    _msg_file_path = path.join(path.dirname(__file__), "boc_messages.txt")
    _messages = []

    def __init__(self, kingdom: Kingdom):
        super().__init__(kingdom)
        self.kingdom.give_allegiance = self._check_availability(
            self.kingdom.give_allegiance
        )
        if not self._messages:
            self._read_messages()

    @classmethod
    def _read_messages(cls):
        with open(cls._msg_file_path, "r") as f:
            cls._messages = [msg.strip(",") for msg in f.read().splitlines()]

    def _check_availability(
        self, give_allegiance: Callable[[Kingdom, str], bool]
    ) -> Callable[[Kingdom, str], bool]:
        def boc_give_allegiance(kingdom: Kingdom, msg: str) -> bool:
            if self.is_competing or self.kingdom.allies_given:
                return False
            return give_allegiance(kingdom, msg)

        return boc_give_allegiance

    def compete(self, ballot_kingdoms: Iterable[BallotKingdom]) -> List[BallotMessage]:
        return [
            BallotMessage(
                sender=self, receiver=ballot_kingdom, msg=random.choice(self._messages)
            )
            for ballot_kingdom in ballot_kingdoms
        ]


class Ballot(UniverseCompetition):
    def __init__(self, universe: Universe, no_of_messages: int):
        super().__init__(universe)
        self._no_of_messages = no_of_messages
        self._ballot_kingdoms = SortedKeyList(
            [BallotKingdom(kingdom) for kingdom in self._universe.kingdoms],
            key=lambda x: x.kingdom.name,
        )
        self._ballot = []
        self._round_count = 0

    @staticmethod
    def _process_input(user_input):
        kingdom_names = [name.strip().capitalize() for name in user_input.split()]
        if not kingdom_names:
            raise ValueError("Please enter space separated kingdoms")
        return kingdom_names

    def _reset_state(self):
        for ballot_kingdom in self._ballot_kingdoms:
            ballot_kingdom.kingdom.clear_allegiances()
        self._ballot = []

    def _get_worthy_competitors(self) -> SortedKeyList:
        max_allies = max(
            [
                len(competitor.kingdom.allies_received)
                for competitor in self._competitors
            ]
        )
        return SortedKeyList([
            competitor
            for competitor in self._competitors
            if len(competitor.kingdom.allies_received) == max_allies
        ], key=lambda x: x.kingdom.name)

    def _update_competitors(self):
        worthy_competitors = self._get_worthy_competitors()
        for competitor in self._competitors:
            try:
                utils.sorted_list_get_with_key(worthy_competitors, competitor.kingdom.name)
            except ValueError:
                competitor.is_competing = False
        self._competitors = worthy_competitors

    def _settle_tie(self):
        while self._winner is None:
            self._update_competitors()
            self._reset_state()
            self._round_count += 1
            self.commence()
            self.evaluate_competitors()
            self.show_status()

    def register_competitors(self):
        if self._competitors:
            raise RuntimeError("Registration for the competition is now closed!")
        print("Enter the kingdoms competing to be the ruler:")
        self._competitors = [
            utils.sorted_list_get_with_key(self._ballot_kingdoms, competitor_name)
            for competitor_name in self._process_input(input("Input: "))
        ]
        for competitor in self._competitors:
            competitor.is_competing = True

    def show_status(self):
        print(
            "Results after round {} ballot count".format(num2words(self._round_count))
        )
        for competitor in self._competitors:
            print(
                "Output: Allies for {}: {}".format(
                    competitor.kingdom.name, len(competitor.kingdom.allies_received)
                )
            )

    @property
    def winner(self) -> BallotKingdom:
        if self._winner is None:
            self._settle_tie()
        return self._winner

    def evaluate_competitors(self):
        ballot_messages = random.sample(self._ballot, min(self._no_of_messages, len(self._ballot)))
        [
            msg.sender.kingdom.ask_allegiance(msg.receiver.kingdom, msg.msg)
            for msg in ballot_messages
        ]
        worthy_competitors = self._get_worthy_competitors()
        if len(worthy_competitors) == 1:
            self._winner = worthy_competitors[0]

    def commence(self):
        if not self._competitors:
            raise RuntimeError("No competitors. Please register competitors before competing!")

        for ballot_kingdom in self._competitors:
            ballot_kingdoms = deepcopy(self._ballot_kingdoms)
            ballot_kingdoms.remove(ballot_kingdom)
            self._ballot.extend(ballot_kingdom.compete(ballot_kingdoms))



























# def show_ruler_and_allies(universe: Universe):
#     ruler = universe.ruler if universe.ruler else "None"
#     allies = ", ".join(universe.allies) if universe.allies else "None"
#
#     print()
#     print("Who is the ruler of {}?".format(universe.name))
#     print("Output:", ruler)
#     print("Allies of Ruler?")
#     print("Output:", allies)
#     print()
#
#
# def set_ruler_and_allies(universe: Universe, ruler: str):
#     universe.ruler = ruler
#     for kingdom in universe.kingdoms:
#         if kingdom.ally and kingdom.ally.name == ruler:
#             universe.add_ally(kingdom.name)
#
#
# def show_ballot_result(kingdoms: Iterable[BOCKingdom], round_count: int):
#     print("Results after round {} ballot count".format(num2words(round_count)))
#     for boc_kingdom in kingdoms:
#         if boc_kingdom.is_competing:
#             print(
#                 "Output: Allies for {}: {}".format(
#                     boc_kingdom.kingdom.name, boc_kingdom.ally_count
#                 )
#             )
#
#
# def update_competing_kingdoms(kingdoms: Iterable[BOCKingdom]):
#     max_allies = max([kingdom.ally_count for kingdom in kingdoms])
#
#     # Assumption: Previously competing kingdom which won't be competing now can form allegiances
#     for kingdom in kingdoms:
#         if kingdom.ally_count != max_allies:
#             kingdom.is_competing = False
#
#
# def get_competing_kingdoms(kingdoms: SortedKeyList) -> SortedKeyList:
#     return SortedKeyList(
#         [kingdom for kingdom in kingdoms if kingdom.is_competing], key=kingdoms.key
#     )
#
#
# def get_ballot_messages(
#     kingdoms: SortedKeyList, messages: List[str], samples: int = 6
# ) -> List[BallotMessage]:
#     competing_kingdoms = get_competing_kingdoms(kingdoms)
#     ballot_messages = [
#         BallotMessage(receiver, sender, random.choice(messages))
#         for receiver, sender in itertools.product(kingdoms, competing_kingdoms)
#         if receiver is not sender
#     ]
#     return random.sample(ballot_messages, min(len(ballot_messages), samples))
#
#
# def read_messages(path: str) -> List[str]:
#     with open(path, "r") as f:
#         return [msg.strip(",") for msg in f.read().splitlines()]
#
#
# def get_boc_kingdoms(
#     universe: Universe, competing_kingdom_names: Iterable[str]
# ) -> SortedKeyList:
#     kingdoms = SortedKeyList(
#         [BOCKingdom(kingdom) for kingdom in universe.kingdoms],
#         key=lambda x: x.kingdom.name,
#     )
#
#     for kingdom_name in competing_kingdom_names:
#         kingdom = universe.sorted_list_get_with_key(kingdoms, key=kingdom_name)
#         kingdom.is_competing = True
#
#     return kingdoms
#
#
# def reset_allies(boc_kingdoms: Iterable[BOCKingdom]):
#     for boc_kingdom in boc_kingdoms:
#         boc_kingdom.ally_count = 0
#         boc_kingdom.kingdom.reset_ally()
#
#
# def conduct_ballot(universe: Universe, competing_kingdom_names: Iterable[str]) -> str:
#     messages = read_messages(MSG_FILE_PATH)
#     kingdoms = get_boc_kingdoms(universe, competing_kingdom_names)
#
#     round_count = 1
#     while len(get_competing_kingdoms(kingdoms)) > 1:
#         reset_allies(kingdoms)
#         ballot_messages = get_ballot_messages(kingdoms, messages)
#
#         for msg in ballot_messages:
#             if not msg.receiver.is_competing and msg.receiver.kingdom.ally is None:
#                 if universe.form_allegiance(
#                     msg.sender.kingdom.name, msg.receiver.kingdom.name, msg.msg
#                 ):
#                     msg.sender.ally_count += 1
#
#         show_ballot_result(kingdoms, round_count)
#         update_competing_kingdoms(kingdoms)
#         round_count += 1
#
#     return get_competing_kingdoms(kingdoms)[0].kingdom.name
#
#
# def process_input() -> List[str]:
#     print("Enter the kingdoms competing to be the ruler:")
#     inp = input("Input: ")
#     print()
#     kingdom_names = [name.strip().capitalize() for name in inp.split()]
#     if not kingdom_names:
#         raise ValueError("Please enter space separated kingdoms")
#
#     return kingdom_names
#
#
# def main():
#     southeros = SoutherosBuilder.build()
#     show_ruler_and_allies(southeros)
#     kingdom_names = process_input()
#     ruler = conduct_ballot(southeros, kingdom_names)
#     set_ruler_and_allies(universe=southeros, ruler=ruler)
#     show_ruler_and_allies(southeros)


# if __name__ == "__main__":
#     main()
