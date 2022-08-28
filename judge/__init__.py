import tempfile
from .timedDS import TimedDict
from problem import Problem
import uuid
import multiprocessing
import time
import shutil

class Judge:
    def __init__(self):
        self.jobs = TimedDict()

    @staticmethod
    def mkdir():
        return tempfile.mkdtemp()

    @staticmethod
    def rmdir(workDir: str):
        shutil.rmtree(workDir, ignore_errors=True)

    def run(self, problem: Problem, workDir: str):
        jid = uuid.uuid4().hex

        multiprocessing.Process(target=self.worker, args=(jid, problem, workDir), daemon=True).start()

        return jid

    def worker(self, jid: str, problem: Problem, workDir: str):
        time.sleep(5)
        self.rmdir(workDir)

