import pytest
from messenger import User, Channel, LocalStorage

storage = LocalStorage()

def test_user_init():
    u = User(1, "Alice")
    assert u.id == 1
    assert u.name == "Alice"

def test_channel_init():
    c = Channel(1, 'Amis' , member_ids=None)
    assert c.id == 1
    assert c.name == "Amis"
    assert c.member_ids == []

def test_create_channel():
    storage = LocalStorage()
    storage.create_channel("test")
    channels = storage.get_channels()
    assert channels[-1].name == "test"

