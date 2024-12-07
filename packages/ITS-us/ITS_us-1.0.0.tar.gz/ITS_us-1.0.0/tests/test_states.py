#Test states.py

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
import numpy as np
import math, cmath
from its_us.states import *

@pytest.fixture
def test_norm():
    """
    Tests if norm method creates a normalised initial state correctly.
    """
    sqrt2 = 1/math.sqrt(2)
    s0 = norm(1,[1,0])
    s1 = norm(1, [1, 1])
    s2 = norm(2, [1, 1, 1, 1])
    assert (s0 == np.array([[1],[0]])).all()
    assert (s1 == np.array([[sqrt2], [sqrt2]])).all()
    assert (s2 == np.array([[0.5],[0.5],[0.5],[0.5]])).all()

def test_angle():
    """
    Tests if angle method creates an initial state correctly.
    """
    s0 = angle(90,90)
    s1 = angle(0,90)
    s2 = angle(180, 45)
    assert (s0 == np.array([[0.70710678+ 0.j],[0. + 0.70710678j]])).all()
    assert (s1 == np.array([[1.+0.j], [0.+0.j]])).all()
    assert (s2 == np.array([[0. +0.j], [0.70710678+0.70710678j]])).all()

def test_tp():
    """
    1. Tests if tp function creates a tensor product correctly.
    2. Tests if tp function outputs the right dimensions.
    """
    s0 = [[1],[0]]
    s1 = [[0],[1]]
    tp_ex1 = np.array([[0],[1],[0],[0]])
    tp_test1 = tp(s0, s1)
    dim1, dim2, dimF = len(s0), len(s1), len(tp_test1)
    assert (tp_test1 == tp_ex1).all()
    assert (dim1 == 2) and (dim2 == 2)
    assert (dim1 + dim2) == dimF

def test_States(N = 1, state = [[0],[1]]):
    """
    Tests the proper initialisation and methods of the States class.

    Args:
        N (int): Number of qubits used for test as example.
        state (array-like): Array used for test as example.
    """

    # Initialisation:
    probe_state = States(N, state)

    # Test for initialsation:
    assert probe_state.N == N
    assert np.array_equal(probe_state.state, state)

    # Test for get_N():
    assert probe_state.get_N() == N

    # Test for get_state():
    array_copy = probe_state.get_state()
    assert np.array_equal(array_copy, state)
    #-- Tests that the copy is not a deep copy of probe_state.array:
    array_copy[0,0] = 5
    assert not np.array_equal(array_copy, state)

#Test built-in states
def test_Zero():
    """
    Tests if built-in subclass Zero() outputs |0> state correctlly.
    """
    test_state = np.array([[1],[0]])
    probe_state = Zero().state
    assert (test_state == probe_state).all()

def test_One():
    """
    Tests if built-in subclass One() outputs |1> state correctlly.
    """
    test_state = np.array([[0],[1]])
    probe_state = One().state
    assert (test_state == probe_state).all()

def test_Plus():
    """
    Tests if built-in subclass Plus() outputs |+> state correctlly.
    """
    test_state = (1/math.sqrt(2))*np.array([[1], [1]])
    probe_state = Plus().state
    assert (test_state == probe_state).all()

def test_Minus():
    """
    Tests if built-in subclass Minus() outputs |-> state correctlly.
    """
    test_state = (1/math.sqrt(2))*np.array([[1], [-1]])
    probe_state = Minus().state
    assert (test_state == probe_state).all()

def test_PlusI():
    """
    Tests if built-in subclass PlusI() outputs |i> state correctlly.
    """
    test_state = (1/math.sqrt(2))*np.array([[1], [complex(0,1)]])
    probe_state = PlusI().state
    assert (test_state == probe_state).all()

def test_MinusI():
    """
    Tests if built-in subclass MinusI() outputs |-i> state correctlly.
    """
    test_state = (1/math.sqrt(2))*np.array([[1], [complex(0,-1)]])
    probe_state = MinusI().state
    assert (test_state == probe_state).all()

def test_PsiPlus():
    r"""
    Tests if built-in subclass PsiPlus() outputs :math:`|\psi^+>` state correctlly.
    """
    test_state = (1/math.sqrt(2))*((np.kron(Zero().state, One().state) + np.kron(One().state, Zero().state)))
    probe_state = PsiPlus().state
    assert (test_state == probe_state).all()

def test_PsiMinus():
    r"""
    Tests if built-in subclass PsiMinus() outputs :math:`|\psi^->` state correctlly.
    """
    test_state = (1/math.sqrt(2))*((np.kron(Zero().state, One().state) - np.kron(One().state, Zero().state)))
    probe_state = PsiMinus().state
    assert (test_state == probe_state).all()

def test_PhiPlus():
    r"""
    Tests if built-in subclass PhiPlus() outputs :math:`|\phi^+>` state correctlly.
    """
    test_state = (1/math.sqrt(2))*((np.kron(Zero().state, Zero().state) + np.kron(One().state, One().state)))
    probe_state = PhiPlus().state
    assert (test_state == probe_state).all()

def test_PhiMinus():
    r"""
    Tests if built-in subclass PhiMinus() outputs :math:`|\phi^->` state correctlly.
    """
    test_state = (1/math.sqrt(2))*((np.kron(Zero().state, Zero().state) - np.kron(One().state, One().state)))
    probe_state = PhiMinus().state
    assert (test_state == probe_state).all()
