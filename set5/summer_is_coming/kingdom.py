from __future__ import annotations

from bisect import bisect_left, bisect_right
from copy import deepcopy
from dataclasses import dataclass, field
from functools import partial

from sortedcontainers import SortedKeyList


@dataclass(order=True)
class Kingdom:
    name: str
    emblem: str

    _allies_given: SortedKeyList[Kingdom] = field(
        default_factory=partial(SortedKeyList, key=lambda x: x.name), init=False
    )
    _allies_received: SortedKeyList[Kingdom] = field(
        default_factory=partial(SortedKeyList, key=lambda x: x.name), init=False
    )

    def __post_init__(self):
        self.name = self.name.capitalize()
        self.emblem = self.emblem.capitalize()

    # Custom '__eq__' method despite of dataclasses, for the reason that two kingdoms with the same name and different
    # emblems will be considered equal. Hence they can belong in the same universe, which should not be possible.
    def __eq__(self, other: Kingdom):
        return self.name == other.name

    @property
    def allies_given(self) -> SortedKeyList[Kingdom]:
        return deepcopy(self._allies_given)

    @property
    def allies_received(self) -> SortedKeyList[Kingdom]:
        return deepcopy(self._allies_received)

    def _validate_ally(self, ally: Kingdom):
        if self == ally:
            raise RuntimeError("Kingdom {} cannot form allegiance with itself".format(self.name))

    def give_allegiance(self, kingdom: Kingdom, msg: str) -> bool:
        self._validate_ally(kingdom)

        # Memory and time efficient way. Time Complexity: O(nlogn)
        i = 0
        j = 0
        emblem = sorted(self.emblem.lower())
        msg = sorted(msg.lower())
        is_worthy = True

        while i < len(emblem):
            alpha = emblem[i]
            emblem_start_pos = bisect_left(emblem, alpha, lo=i)
            emblem_end_pos = bisect_right(emblem, alpha, lo=i)

            msg_start_pos = bisect_left(msg, alpha, lo=j)
            msg_end_pos = bisect_right(msg, alpha, lo=j)

            if (msg_end_pos - msg_start_pos) < (emblem_end_pos - emblem_start_pos):
                is_worthy = False
                break

            i = emblem_end_pos
            j = msg_end_pos

        if is_worthy:
            self._allies_given.add(kingdom)

        return is_worthy

        # If memory and time is not an issue, we can use this. Time Complexity: O(n^2)
        #
        # is_worthy = all([msg.count(alpha) >= count for alpha, count in Counter(kingdom.emblem)])
        # return is_worthy

    def ask_allegiance(self, kingdom: Kingdom, msg: str) -> bool:
        self._validate_ally(kingdom)
        am_i_worthy = kingdom.give_allegiance(self, msg)
        if am_i_worthy:
            self._allies_received.add(kingdom)

        return am_i_worthy

    def clear_allegiances(self):
        self._allies_given = SortedKeyList(key=lambda x: x.name)
        self._allies_received = SortedKeyList(key=lambda x: x.name)
