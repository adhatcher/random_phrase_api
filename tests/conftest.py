import importlib
import os
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture(scope="session")
def api_module(tmp_path_factory):
    logs_dir = tmp_path_factory.mktemp("logs")
    os.environ["LOG_DIR"] = str(logs_dir)

    module = importlib.import_module("random_phrase_api")
    module.app.config.update(TESTING=True)
    module.phrases = ["alpha", "beta", "gamma"]
    return module


@pytest.fixture
def client(api_module):
    with api_module.app.test_client() as test_client:
        yield test_client
