import os
import subprocess

"""
Pytest configuration file
"""

def pytest_sessionstart():
    """
    Prepare tests
    """
    path = os.path.join(os.getcwd(), "tests/etl")
    # check if triplydb token is set
    assert os.environ.get('TRIPLYDB_GITLAB_TOKEN') is not None
    # Install yarn
    # subprocess.run(['yarn', '-v'], cwd=path, check = True)
    # subprocess.run(['yarn', 'cache', 'clean'], cwd=path, check = True)
    # subprocess.run(['yarn', 'install'], cwd=path, check = True)
    # subprocess.run(['yarn', 'tsc'], cwd=path, check = True)
    subprocess.run(['npm', 'i'], cwd=path, check = True)
    subprocess.run(['npm', 'run', 'build'], cwd=path, check = True)
