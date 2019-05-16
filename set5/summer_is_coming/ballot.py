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
        if len(set(kingdom_names)) != len(kingdom_names):
            raise ValueError("Kingdoms should not be repeated!")

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
            f"Results after round {num2words(self._round_count)} ballot count"
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
