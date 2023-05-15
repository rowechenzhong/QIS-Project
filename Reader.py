import numpy as np
import random
import scipy.linalg


n = 3
qubits = 2 * n
num_basis = 4**(qubits)

TOTAL = [0, 0, 136, 1376][n]

space = []

# We can do IIIIII lol
res = np.zeros((num_basis,))
res[0] = 1
space.append(res)

# 1-qubit operators
for A in range(1, 4):
    res = np.zeros((num_basis,))
    for i in range(n):
        res[A * 4**(2 * i)] = 1
    space.append(res)
    res = np.zeros((num_basis,))
    for i in range(n):
        res[A * 4**(2 * i + 1)] = 1
    space.append(res)

# 2-qubit operators
for A in range(1, 4):
    for B in range(1, 4):
        for offset in range(n):
            res = np.zeros((num_basis,))
            for i in range(n):
                res[
                    A * 4**(2 * i) +
                    B * 4**((2 * (i + offset) + 1) % qubits)
                ] = 1
            space.append(res)

group = [i for i in range(len(space))]


def print_pauli(pauli):
    """
    Print a pauli string in the form of a 4096-tuple of real numbers.
    """
    res = ""
    for i in range(num_basis):
        if pauli[i] == 0:
            continue
        res += str(pauli[i]) + " * "
        for j in range(qubits):
            # Let a be the j-th pauli of i.
            a = (i // 4**j) % 4
            res += "IXYZ"[a]
        res += " + "
    return res[:-3]


def string_to_array(s):
    """
    Convert a string of paulis to an array.
    """
    print(s)
    res = np.zeros((num_basis,))
    tokens = s.split(" + ")
    for token in tokens:
        coeff = float(token.split(" * ")[0])
        pauli = token.split(" * ")[1]
        idx = 0
        for j in range(qubits):
            idx += "IXYZ".index(pauli[j]) * 4**j
        res[idx] = coeff
    return res


file = open("QRoutput.txt", "r")
lines = file.readlines()
file.close()
important_lines = []
"""
1 1.0 * XIIIII + 1.0 * IIXIII + 1.0 * IIIIXI
Size: 25
Rank: 25
...
10 1.0 * IXYIII + 1.0 * IIIXYI + 1.0 * YIIIIX
Size: 121
Rank: 43
"""
for i in lines:
    if "Size" in i or "Rank" in i:
        continue
    important_lines.append(i)
# Remove the number before the first space
important_lines = [i.split(" ", 1)[1] for i in important_lines]

# parse with string_to_array
important_lines = [string_to_array(i) for i in important_lines]
# create a matrix
M = np.array(important_lines)
# Compute rank
print(np.linalg.matrix_rank(M))
