from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from summer_is_coming.kingdom import Kingdom
from summer_is_coming.universe import Universe


@dataclass
class UniverseCompetitor(ABC):
    kingdom: Kingdom
    is_competing: bool = False

    @abstractmethod
    def compete(self, *args, **kwargs):
        pass


class UniverseCompetition(ABC):
    def __init__(self, universe: Universe):
        self._universe = universe
        self._competitors = []
        self._winner = None

    @abstractmethod
    def register_competitors(self, *args, **kwargs):
        pass

    @property
    def universe(self) -> Universe:
        return self._universe

    @property
    def competitors(self) -> List[UniverseCompetitor]:
        return self._competitors

    @abstractmethod
    def show_status(self):
        pass

    @property
    @abstractmethod
    def winner(self) -> UniverseCompetitor:
        pass

    @abstractmethod
    def evaluate_competitors(self):
        pass

    @abstractmethod
    def commence(self):
        pass
