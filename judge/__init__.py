import tempfile
from .timedDS import TimedDict
from .result import Result
import config.judge as config
from problem import Problem
import uuid
import threading
import shutil
import docker
from docker.types import Mount
import json
import traceback

jobs = TimedDict(config.resultLifetime)
dockerClient = docker.from_env()

def mkdir():
    return tempfile.mkdtemp()

def rmdir(workDir: str):
    shutil.rmtree(workDir, ignore_errors=True)

def run(problem: Problem, workDir: str):
    jid = uuid.uuid4().hex

    jobs[jid] = Result()
    threading.Thread(target=worker, args=(jid, problem, workDir), daemon=True).start()

    return jid

def worker(jid: str, problem: Problem, workDir: str):
    try:
        result = dockerClient.containers.run(problem.imageName, remove=True, mounts=[Mount('/submission', workDir, type='bind')]).decode()
        result = json.loads(result)
        jobs[jid].write(result)
    except Exception:
        jobs[jid].judgeError()
        print(traceback.format_exc())
    rmdir(workDir)