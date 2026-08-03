import json
import os
import sys
import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import MagicMock, patch

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(PROJECT_ROOT))


def _patch_dotenv():
    patcher = patch.dict(os.environ, {}, clear=True)
    patcher.start()
    return patcher


def _make_mock_response(payload, status=200, headers=None):
    mock = MagicMock()
    mock.status = status
    mock.headers = headers or {}
    mock.read.return_value = json.dumps(payload).encode("utf-8")
    mock.__enter__ = MagicMock(return_value=mock)
    mock.__exit__ = MagicMock(return_value=False)
    return mock


def _make_mock_request(url, data=None, headers=None, timeout=None, **kwargs):
    return MagicMock()
