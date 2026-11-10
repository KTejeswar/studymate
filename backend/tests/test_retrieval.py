"""
Tests for vector cosine similarity and ranking.
"""

import numpy as np
from app.services.retrieval import cosine_similarity


def test_cosine_similarity_identical_vectors():
    vec_a = np.array([1.0, 2.0, 3.0], dtype=np.float32)
    score = cosine_similarity(vec_a, vec_a)
    assert np.isclose(score, 1.0)


def test_cosine_similarity_orthogonal_vectors():
    vec_a = np.array([1.0, 0.0], dtype=np.float32)
    vec_b = np.array([0.0, 1.0], dtype=np.float32)
    score = cosine_similarity(vec_a, vec_b)
    assert np.isclose(score, 0.0)


def test_cosine_similarity_opposite_vectors():
    vec_a = np.array([1.0, 0.0], dtype=np.float32)
    vec_b = np.array([-1.0, 0.0], dtype=np.float32)
    score = cosine_similarity(vec_a, vec_b)
    assert np.isclose(score, -1.0)


def test_cosine_similarity_zero_vector():
    vec_a = np.array([0.0, 0.0], dtype=np.float32)
    vec_b = np.array([1.0, 1.0], dtype=np.float32)
    score = cosine_similarity(vec_a, vec_b)
    assert score == 0.0
