import os
import subprocess

import pytest

"""
Pytest configuration file
"""
def pytest_sessionstart():
    """
    Prepare tests
    """
    if os.environ.get('TRIPLYDB_GITLAB_TOKEN') is not None:
        path = os.path.join(os.getcwd(), "tests/etl")
        subprocess.run(['npm', 'i'], cwd=path, check = True)
        subprocess.run(['npm', 'run', 'build'], cwd=path, check = True)
