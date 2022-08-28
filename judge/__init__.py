import tempfile
from .timedDS import TimedDict
from .result import Result
import config.judge as config
from problem import Problem
import uuid
import multiprocessing
import time
import shutil

jobs = TimedDict(config.resultLifetime)

def mkdir():
    return tempfile.mkdtemp()

def rmdir(workDir: str):
    shutil.rmtree(workDir, ignore_errors=True)

def run(problem: Problem, workDir: str):
    jid = uuid.uuid4().hex

    jobs[jid] = Result()
    multiprocessing.Process(target=worker, args=(jid, problem, workDir), daemon=True).start()

    return jid

def worker(jid: str, problem: Problem, workDir: str):
    time.sleep(5)
    rmdir(workDir)