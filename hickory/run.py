import subprocess


def run(command, output=True, silent=False):
    if silent:
        command += " --quiet"
    if output:
        s = subprocess.run(command, capture_output=True, shell=True)
        o = s.stdout.decode("utf-8").strip()
        return o
    subprocess.run(command, shell=True)
