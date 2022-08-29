from dataclasses import dataclass
import traceback

class Result:
    def __init__(self):
        self.ready = False
        self.subtasks = []
        self.score = 0
        self.weight = 0

    def judgeError(self):
        self.subtasks = [Subtask('JUDGE ERROR', 'JE', 0, 0)]
        self.ready = True

    def write(self, content):
        try:
            for name, verdict, score, weight in content:
                self.score += score
                self.weight += weight
                self.subtasks.append(Subtask(name, verdict, score, weight))
            self.ready = True
        except:
            self.judgeError()
            print(traceback.format_exc())

    def __repr__(self):
        return repr(self.ready)

@dataclass
class Subtask:
    name: str
    verdict: str
    score: int
    weight: int