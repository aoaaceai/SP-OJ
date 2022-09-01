from dataclasses import dataclass
from datetime import datetime
import config.problem as config
import json
import os
import traceback
# Problems should be stored in the following structure:
# - config.json
#   - visibility
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
    quota: int
    description: str

    @property
    def available(self):
        return datetime.now() <= self.deadline

problems = {}

def loadProblems():
    problems.clear()
    for entry in os.scandir(config.problemsPath):
        try:
            with open(entry.path + '/config.json') as f:
                info = json.load(f)
            with open(entry.path + '/description.md') as f:
                description = f.read()
            if not info['visible']:
                continue
            pid = int(entry.name)
            deadline = datetime.strptime(info['deadline'], '%Y-%m-%d %H:%M')
            problems[pid] = Problem(pid, info['name'], deadline, info['imageName'], info['quota'], description)
        except:
            print(traceback.format_exc())
            print(f'skipping {entry.name} due to errors')
            continue

def getProblem(pid):
    if not problems:
        loadProblems()

    if pid not in problems:
        return None

    return problems[pid]

def getProblems():
    if not problems:
        loadProblems()
    return list(problems.values())