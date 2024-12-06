import pytest
from curly_comparer.algorithms.levenshtein import distace, weighted_distance


def test_distance_different_strings():
    str1 = "hello world!"
    str2 = "this is another string"
    assert distace(str1, str2) == 18


def test_distance_different_strings2():
    str1 = "Hell"
    str2 = "Hello"
    assert distace(str1, str2) == 1


def test_weighted_distance_different_strings():
    str1 = "Hello World"
    str2 = "Goodbye"
    assert int(weighted_distance(str1,
                                 str2,
                                 lambda x: 1,
                                 lambda x: 1,
                                 lambda x, y: 1)) == 10


def test_weighted_distance_with_0_cost_subs():
    str1 = "Hello World"
    str2 = "Goodbye"
    assert int(weighted_distance(str1,
                                 str2,
                                 lambda x: 1,
                                 lambda x: 1,
                                 lambda x, y: 0)) == 4


def test_weighted_distance_with_0_cost_insertion():
    str1 = "Hello World"
    str2 = "Goodbye"
    assert int(weighted_distance(str1,
                                 str2,
                                 lambda x: 0,
                                 lambda x: 1,
                                 lambda x, y: 1)) == 8


def test_weighted_distance_with_0_cost_deletion():
    str1 = "Hello World"
    str2 = "Goodbye"
    assert int(weighted_distance(str1,
                                 str2,
                                 lambda x: 1,
                                 lambda x: 0,
                                 lambda x, y: 1)) == 4


def test_weighted_distance_with_0_cost_deletion_and_insertion():
    str1 = "Hello World"
    str2 = "Goodbye"
    assert int(weighted_distance(str1,
                                 str2,
                                 lambda x: 0,
                                 lambda x: 0,
                                 lambda x, y: 1)) == 0
