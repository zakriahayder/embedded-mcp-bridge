import subprocess

import pytest


@pytest.fixture
def successful_proc():
    return subprocess.CompletedProcess(
        args=["pio", "run"], returncode=0, stdout="Build successful", stderr=""
    )