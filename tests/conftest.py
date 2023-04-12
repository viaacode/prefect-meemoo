import os
import subprocess

def pytest_sessionstart():
    path = os.path.join(os.getcwd(), "tests/etl")
    subprocess.run(['yarn', 'cache', 'clean'], cwd=path, check = True)
    subprocess.run(['yarn', 'install'], cwd=path, check = True)
    subprocess.run(['yarn', 'tsc'], cwd=path, check = True)
