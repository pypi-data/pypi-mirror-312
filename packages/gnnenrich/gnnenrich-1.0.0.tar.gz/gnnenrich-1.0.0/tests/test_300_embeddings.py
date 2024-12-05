import collections
import gnnenrich
import numpy
import pytest

def test_get_items_embeddings():

    emb = collections.OrderedDict()
    emb['A'] = [1.0, 2.1]
    emb['B'] = [0.5, 3.4]

    scoring = gnnenrich.Scoring(emb)
    assert numpy.array_equal(scoring.get_items_embeddings(set(['A'])),
                             numpy.array([[1.0, 2.1]], dtype=numpy.float32))
    
def test_wrong_embeddings():

    emb = collections.OrderedDict()
    emb['A'] = [1.0, 2.1]
    emb['B'] = [0.5, 3.4, 7.8] # Embedding with different size

    with pytest.raises(ValueError):
        scoring = gnnenrich.Scoring(emb)
