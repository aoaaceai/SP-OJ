import tempfile
from .timedDS import TimedDict
from .result import Result
import config.judge as config
from problem import Problem
import uuid
import os
import docker
from docker.types import Mount
import json
import traceback
from .threadPool import ThreadPool

jobs = TimedDict(config.resultLifetime)
dockerClient = docker.from_env()
pool = ThreadPool(config.threadPoolSize)

def new():
    return uuid.uuid4().hex

def submissionFile(jid):
    return f'{tempfile.gettempdir()}/{jid}.zip'

def saveZip(jid, file):
    file.save(submissionFile(jid))

def rmZip(jid):
    os.remove(submissionFile(jid))

def run(jid: str, problem: Problem):
    jobs[jid] = Result()
    pool.addThread(worker, args=(jid, problem))

    return jid

def worker(jid: str, problem: Problem):
    try:
        result = dockerClient.containers.run(problem.imageName, remove=True, mounts=[Mount('/submission/submission.zip', submissionFile(jid), type='bind')]).decode()
        result = json.loads(result)
        jobs[jid].write(result)
    except Exception:
        jobs[jid].judgeError()
        print(traceback.format_exc())
    
    rmZip(jid)
