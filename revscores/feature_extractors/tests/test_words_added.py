from collections import namedtuple

from nose.tools import eq_

from ..words_added import words_added


def test_words_added():
    eq_(words_added(["This is four words.", "And two."]), 6)
