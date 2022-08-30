from dataclasses import dataclass
from datetime import datetime
# Problems should be stored in the following structure:
# - config.json
#   - name
#   - weight
#   - imageName
# - description.md

# Test cases, grading criteria, etc. are defined by the
# docker image, not the OJ.

# This Problem class only does the following jobs:
# - Provide data for the frontend to render

@dataclass
class Problem:
    id: int
    name: str
    deadline: datetime
    imageName: str
    description: str

defaultProblems = [
    Problem(0, 'aoeu', datetime.strptime('2022-09-30 00:00', '%Y-%m-%d %H:%M'), 'judger', 'aoeu\nhnts'),
    Problem(1, 'htns', datetime.strptime('2022-10-30 00:00', '%Y-%m-%d %H:%M'), 'judger', 'desc2')
]

def loadProblem(pid):
    if pid >= len(defaultProblems):
        return None

    return defaultProblems[pid]

def getProblems():
    return defaultProblems