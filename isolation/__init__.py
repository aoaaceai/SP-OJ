import subprocess
import config.isolation as config

def execProgram(args, cwd: str='/', tmpfs: bool=False, mountRW: dict={}, mountRO: dict={}, env: dict=config.defaultEnv):
    command = ['nsjail', '-Q', '-c', config.chrootPath, '-D', cwd]
    if tmpfs:
        command += ['-T', '/tmp']
    for hostPath, guestPath in mountRW.items():
        command += ['-B', f'{hostPath}:{guestPath}']
    for hostPath, guestPath in mountRO.items():
        command += ['-R', f'{hostPath}:{guestPath}']
    for key, val in env.items():
        command += ['-E', f'{key}={val}']
    

    result = subprocess.run(command + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    return result

def make(args, workDir):
    return execProgram(['make', *args], workDir)