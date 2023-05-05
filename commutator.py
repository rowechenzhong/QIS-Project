"""
An entry is going to be a list of pairs of the form (coefficient, pauli string)
where pauli strings contain only I, X, Y, Z.

Then, Commutator will take two entries and return a new entry.
"""

from typing import List, Tuple
from functools import reduce
from operator import mul
from itertools import product
from copy import deepcopy


def pauli_commutator_char(p, q):
    """
    :param p: single character from pauli string
    :param q: single character from pauli string
    :return: single character from pauli string, and a phase +-1
    """
    res = {
        'I': {'I': 'I', 'X': 'X', 'Y': 'Y', 'Z': 'Z'},
        'X': {'I': 'X', 'X': 'I', 'Y': 'Z', 'Z': 'Y'},
        'Y': {'I': 'Y', 'X': 'Z', 'Y': 'I', 'Z': 'X'},
        'Z': {'I': 'Z', 'X': 'Y', 'Y': 'X', 'Z': 'I'}
    }
    phase = {
        'I': {'I': 1, 'X': 1, 'Y': 1, 'Z': 1},
        'X': {'I': 1, 'X': 1, 'Y': 1, 'Z': -1},
        'Y': {'I': 1, 'X': -1, 'Y': 1, 'Z': 1},
        'Z': {'I': 1, 'X': 1, 'Y': -1, 'Z': 1}
    }
    return res[p][q], phase[p][q]


def pauli_commutator(p, q):
    """
    :param p: pauli string
    :param q: pauli string
    :return: pauli string
    """
    if len(p) != len(q):
        raise ValueError("Pauli strings must be of equal length")
    result = []
    total_phase = 1
    total_anticommute = 0
    for p_char, q_char in zip(p, q):
        res, phase = pauli_commutator_char(p_char, q_char)
        result.append(res)
        total_phase *= phase
        if res != 'I':
            total_anticommute += 1
    if total_anticommute % 2 == 0:
        return '', 0
    return ''.join(result), total_phase


def convolve_commutator(p, q):
    """
    :param p: list of tuples of the form (coefficient, pauli string)
    :param q: list of tuples of the form (coefficient, pauli string)
    :return: list of tuples of the form (coefficient, pauli string)
    """
    result = []
    for (p_coeff, p_pauli), (q_coeff, q_pauli) in product(p, q):
        pauli, phase = pauli_commutator(p_pauli, q_pauli)
        if pauli != '':
            result.append((p_coeff * q_coeff * phase, pauli))
    return result
