import gnnenrich
import pytest
import random

def test_RandomListsGenerator():

    # Empty list
    gen = gnnenrich.RandomListsGenerator([], 0)
    assert gen.size == 0
    assert next(gen) == []
    with pytest.raises(ValueError):
        gen = gnnenrich.RandomListsGenerator([], 1)

    # One item, size 0
    gen = gnnenrich.RandomListsGenerator([1], 0)
    assert gen.size == 0
    assert next(gen) == []
    with pytest.raises(ValueError):
        gen = gnnenrich.RandomListsGenerator([1], 2)

    # One item, size 1
    gen = gnnenrich.RandomListsGenerator([1], 1)
    assert gen.size == 1
    assert gen.length == -1
    assert gen.offset == 0
    assert next(gen) == [1]
    assert next(gen) == [1]
    assert gen.count == 2

    # Two items, size 1
    random.seed(42)
    gen = gnnenrich.RandomListsGenerator([1, 2], 1)
    assert gen.size == 1
    assert gen.length == -1
    assert next(gen) == [1]
    assert next(gen) == [1]
    assert next(gen) == [2]
    assert gen.count == 3
    
def test_keep_generated_lists():

    random.seed(42)
    gen = gnnenrich.RandomListsGenerator([1, 2], 1)
    assert next(gen) == [1]
    assert gen.get_lists() == []

    random.seed(42)
    gen = gnnenrich.RandomListsGenerator([1, 2], 1, keep=True)
    assert next(gen) == [1]
    assert next(gen) == [1]
    assert next(gen) == [2]
    assert gen.get_lists() == [[1], [1], [2]]
    
def test_offset():
    random.seed(42)
    gen = gnnenrich.RandomListsGenerator([1, 2], 1, offset=1)
    assert gen.offset == 1
    assert next(gen) == [1]
    assert next(gen) == [2]

def test_length():
    random.seed(42)
    gen = gnnenrich.RandomListsGenerator([1, 2], 1, length=2)
    assert gen.length == 2
    assert next(gen) == [1]
    assert next(gen) == [1]
    assert gen.count == 2
    with pytest.raises(StopIteration):
        assert next(gen) == [2]
    assert gen.count == 2
    
def test_generate_random_lists():
    random.seed(42)
    assert gnnenrich.generate_random_lists(['a'], 1, 1) == [['a']]
    random.seed(42)
    assert gnnenrich.generate_random_lists(['a', 'b'], 1, 1) == \
        [['a']]
    random.seed(42)
    assert gnnenrich.generate_random_lists(['a', 'b'], 2, 1) == \
        [['a'], ['a']]
    random.seed(42)
    assert gnnenrich.generate_random_lists(['a', 'b'], 1, 2) == \
        [['a', 'b']]
    random.seed(42)
    assert gnnenrich.generate_random_lists(['a', 'b', 'c'], 1, 3) == \
        [['c', 'a', 'b']]
    random.seed(42)
    assert gnnenrich.generate_random_lists(['a', 'b', 'c'], 1, 2) == \
        [['c', 'a']]
    random.seed(42)
    assert gnnenrich.generate_random_lists(['a', 'b', 'c'], 2, 2) == \
        [['c', 'a'], ['a', 'b']]
