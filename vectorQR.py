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
        res = np.zeros((num_basis,))
        for i in range(n):
            res[(A + 4 * B) * 4**(2 * i)] = 1
        space.append(res)
        res = np.zeros((num_basis,))
        for i in range(n-1):
            res[(A + 4 * B) * 4**(2 * i + 1)] = 1
        # Finally, BIIIIA
        res[B + 4**(qubits - 1) * A] = 1
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


# Save all output in the below in a file, appending
f = open("QRoutput.txt", "a")


def fprint(*args):
    print(*args)
    f.write(" ".join([str(i) for i in args]))
    f.write("\n")


for i in range(len(space)):
    fprint(i, print_pauli(space[i]))


def commutator(A, B):
    """
    A is a pauli string in the form of a 4096-tuple of real numbers.
    B is also a pauli string.
    """
    res = np.zeros((num_basis,))
    for i in range(num_basis):
        if A[i] == 0:
            continue
        for j in range(num_basis):
            if B[j] == 0:
                continue
            phase = 0
            for k in range(qubits):
                a = (i // 4**k) % 4
                b = (j // 4**k) % 4
                phase += [
                    [0, 0, 0, 0],
                    [0, 0, 1, 3],
                    [0, 3, 0, 1],
                    [0, 1, 3, 0]
                ][a][b]
            phase %= 4
            if phase == 1:
                res[i ^ j] += A[i] * B[j]
            elif phase == 3:
                res[i ^ j] -= A[i] * B[j]
    return res


def cycle(A):
    """
    A is a pauli string. Return the pauli strings with (X, Y, Z)
    replaced by all permutations (3! = 6 total)
    In addition, try cyclic slides.
    """
    res = []
    permutations = [(0, 1, 2, 3), (0, 1, 3, 2), (0, 2, 1, 3),
                    (0, 2, 3, 1), (0, 3, 1, 2), (0, 3, 2, 1)]
    for p in permutations:
        new = np.zeros((num_basis,))
        for i in range(num_basis):
            if A[i] == 0:
                continue
            idx = 0
            for j in range(qubits):
                # Let a be the j-th pauli of i.
                a = (i // 4**j) % 4
                idx += p[a] * 4**j
            new[idx] = A[i]
        res.append(new)

    # Now, try cyclic slides.
    for p in permutations:
        new = np.zeros((num_basis,))
        for i in range(num_basis):
            if A[i] == 0:
                continue
            idx = 0
            for j in range(qubits):
                # Let a be the j-th pauli of i.
                a = (i // 4**j) % 4
                idx += p[a] * 4**((j + 1) % qubits)
            new[idx] = A[i]
        res.append(new)

    return res

# Okay, finally.
# Now, I want to see how many different linearly
# independent operators we can generate through commutators.


i = 0
seen = []
while i < len(space):
    # if group[i] in seen:
    #     i += 1
    #     continue
    # seen.append(group[i])
    i += 1
    print(i, print_pauli(space[i]))
    before = len(space)
    for j in range(i):
        new = commutator(space[j], space[i])
        if np.count_nonzero(new) == 0:
            continue
        # if sum([i != 0 for i in new]) == 0:
        #     continue
        cycle_space = cycle(new)

        # Add all the new elements to space, checking rank
        for c in cycle_space:
            space.append(c)
        group += [group[-1] + 1]*len(cycle_space)

    print("Size:", len(space))
    assert len(space) == len(group)
    M = np.array(space).T
    r, = scipy.linalg.qr(M, mode='r')  # scipy linalg
    indicies = np.logical_not(np.isclose(np.diagonal(r), 0))
    # pad indicies to length of space with False
    indicies = np.pad(indicies, (0, len(space) - len(indicies)), 'constant')
    assert len(indicies) == len(space)
    assert all(indicies[i] for i in range(before))
    print("Rank:", sum(indicies))
    space = [space[i] for i in range(len(space)) if indicies[i]]
    group = [group[i] for i in range(len(group)) if indicies[i]]

    if sum(indicies) == TOTAL:
        break
f.close()
