import collections
import gnnenrich
import numpy
import pytest

def test_comp_corr():

    emb = collections.OrderedDict()

    scoring = gnnenrich.Scoring(emb)
    assert scoring.corr_threshold == 0.95
    a = numpy.array([[0, 1, 2, 3], [1, 0, -1, -2]])
    b = numpy.array([[1, 1, 2, 3], [1, 1, -4, -5]])
    assert scoring.comp_corr(a, b) == 0.0

    scoring = gnnenrich.Scoring(emb, corr_threshold=0.9)
    assert scoring.corr_threshold == 0.9
    a = numpy.array([[0, 1, 2, 3], [1, 0, -1, -2]])
    b = numpy.array([[1, 1, 2, 3], [1, 1, -4, -5]])
    assert scoring.comp_corr(a, b) == 1.0

    scoring = gnnenrich.Scoring(emb, corr_threshold=0.9,
                                corr_threshold_repl_value=0.0)
    assert scoring.corr_threshold == 0.9
    a = numpy.array([[0, 1, 2, 3], [1, 0, -1, -2]])
    b = numpy.array([[1, 1, 2, 3], [1, 1, -4, -5]])
    assert scoring.comp_corr(a, b) == 0.9356646608879388
    
def test_overlap_score():

    emb = collections.OrderedDict()

    scoring = gnnenrich.Scoring(emb)
    assert scoring.overlap_score == 3.0

    scoring = gnnenrich.Scoring(emb)
    a = numpy.array([[0, 1, 2, 3], [1, 0, -1, -2]])
    b = numpy.array([[0, 1, 2, 3], [1, 0, -1, -2]])
    assert scoring.comp_corr(a, b) == 3.0

    overlap = 4.0
    scoring = gnnenrich.Scoring(emb, overlap_score=overlap)
    a = numpy.array([[0, 1, 2, 3], [1, 0, -1, -2]])
    b = numpy.array([[0, 1, 2, 3], [1, 0, -1, -2]])
    assert scoring.comp_corr(a, b) == overlap
