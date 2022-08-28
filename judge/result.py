from dataclasses import dataclass
from enum import Enum

class Verdict(Enum):
    AC = 0
    JE = 1
    RE = 2
    WA = 3
    TLE = 4

class Result:
    def __init__(self):
        self.ready = False
        self.subtasks = []
        self.score = 0

@dataclass
class Subtask:
    name: str
    verdict: Verdict
    score: int
    weight: int


