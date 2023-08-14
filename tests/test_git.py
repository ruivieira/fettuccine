import pytest
from fettuccine.git import Git

def test_git():
    g = Git(".")
    assert g is not None

def test_has_changes():
    g = Git(".")
    assert not g.has_changes()
