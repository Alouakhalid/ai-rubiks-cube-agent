from abc import ABC, abstractmethod
from typing import List


class BaseSolver(ABC):
    @abstractmethod
    def solve(self, state: str) -> List[str]:
        pass
