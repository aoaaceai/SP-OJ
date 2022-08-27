import tempfile
from problem import Problem
import uuid
import multiprocessing
import time
import shutil
from . import reaper

reaper.start()

def mkdir():
    return tempfile.mkdtemp()

def run(problem: Problem, workDir: str):
    jid = uuid.uuid4().hex

    child = multiprocessing.Process(target=worker, args=(jid, problem, workDir))
    child.start()

    return jid

def worker(jid: str, problem: Problem, workDir: str):
    time.sleep(5)
    shutil.rmtree(workDir, ignore_errors=True)
