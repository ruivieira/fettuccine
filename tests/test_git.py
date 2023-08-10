import pytest
from linguine.git import Git

def test_git():
    g = Git(".")
    assert g is not None

