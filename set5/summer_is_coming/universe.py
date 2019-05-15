from __future__ import annotations

from copy import deepcopy
from typing import Iterable

from sortedcontainers import SortedKeyList

from summer_is_coming import utils
from summer_is_coming.kingdom import Kingdom


class Universe:
    def __init__(self, name):
        self.name = name.capitalize()
        self._kingdoms = SortedKeyList(key=lambda x: x.name)
        self._ruler = ''

    @property
    def kingdoms(self) -> SortedKeyList[Kingdom]:
        # deepcopy prevents client code from modifying internal state of universe
        return deepcopy(self._kingdoms)

    @property
    def ruler(self) -> str:
        return self._ruler

    @ruler.setter
    def ruler(self, new_ruler: str):
        new_ruler = new_ruler.capitalize()
        self._get_kingdom(new_ruler)
        self._ruler = new_ruler

    def add_kingdoms(self, kingdoms: Iterable[Kingdom]):
        for kingdom in kingdoms:
            if kingdom not in self._kingdoms:
                self._kingdoms.add(kingdom)

    def _get_kingdom(self, kingdom_name: str) -> Kingdom:
        kingdom_name = kingdom_name.capitalize()
        try:
            kingdom = utils.sorted_list_get_with_key(self._kingdoms, kingdom_name)
        except ValueError:
            raise ValueError(
                "Kingdom '{}' is not part of the '{}' universe".format(
                    kingdom_name, self.name
                )
            )
        return kingdom

    def get_kingdom(self, kingdom_name: str) -> Kingdom:
        return deepcopy(self._get_kingdom(kingdom_name))

    def form_allegiance(self, sender: str, receiver: str, msg: str) -> bool:
        sender = self._get_kingdom(sender)
        receiver = self._get_kingdom(receiver)
        return sender.ask_allegiance(receiver, msg)
