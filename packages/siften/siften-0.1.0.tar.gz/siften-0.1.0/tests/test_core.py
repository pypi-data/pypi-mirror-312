"""
Tests for core functionality.
"""
from siften import hello_world

def test_hello_world_default():
    assert hello_world() == "Hello, World!"

def test_hello_world_custom():
    assert hello_world("Alice") == "Hello, Alice!"
