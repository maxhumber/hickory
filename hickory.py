import functools
import subprocess
import uuid

def run(command, output=False, silent=False):
    '''Run shell commands
    - command (str): a bash command
    - output (bool, False): capture and return the STDOUT
    - silent (bool, False): force commands to run silently
    Example:
    `run('git --git-dir=.mummify status')`
    '''
    if silent:
        command += ' --quiet'
    if output:
        s = subprocess.run(command, capture_output=True, shell=True)
        output = s.stdout.decode('utf-8').strip()
        return output
    subprocess.run(command, shell=True)



def task(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("stuff")
        func(*args, **kwargs)
        return "hi"
    return wrapper

def print_hello():
    print("Hello")

print_hello.__name__
