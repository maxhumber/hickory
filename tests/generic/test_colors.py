import pytest

from hickory.colors import *


def test_color_str():
    assert str(Color(93)) == '\033[93m'
    assert str(Color(93, 94)) == '\033[93;94m'


def test_color_format():
    assert f'{Color(93)}' == '\033[93m'
    assert f'{Color(93)}bb' == '\033[93mbb'


def test_color_matmul():
    assert Color(93) @ 'allo' == '\033[93mallo\033[m'
    assert 'allo' @ Color(93) == '\033[93mallo\033[m'


def test_color_compose():
    assert Color(93) @ Color(102) @ 'allo' == '\033[93;102mallo\033[m'


def test_color_add():
    c = Color(93) + Color(94)
    print(repr(c))
    assert c == Color(93, 94)
