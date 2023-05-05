"""
Our operators are very sparse. Thus, we will encode one operator as a dictionary
of {pauli: coefficient} pairs.
Pauli is an integer. For instance,
XYZ would be encoded as 1 * 4^0 + 2 * 4^1 + 3 * 4^2 = 1 + 8 + 48 = 57.

Observe that we are now basically working base 16. One qublock is two qubits.

XZX really represents
XZX + IIXZX + IIIIXZX + ...

and is thus different from IXZX (but is the same as IIXZX).

Cool. Now, a convolution operation on two Pauli strings will return a dictionary of {pauli : coefficient}

If the first string is a qublocks long and the second is b qublocks long, then the final
strings are at most a + b - 1 qublocks long.

We'll start with the ability to do AB for all A,B in {I,X,Y,Z}^2 and IAB for all A,B in {X,Y,Z}^2.
"""

import numpy as np
import random

n = 3
qubits = 2 * n
num_basis = 4**(qubits)


def reduce(A):
    """
    Divide A by 16 until A is not divisible by 16.
    """
    while A % 16 == 0:
        A //= 16
    return A


def commute(A, B):
    """
    A and B are unreduced pauli strings.
    Return reduced commutator of A,B, in the form {pauli : coefficient}
    """
    res = A ^ B  # XOR
    # Other than res, we also need to keep track of the phase.
    flips = 0  # Difference in phase between AB and BA, mod 2.
    phase = 0  # i^phase is the phase.
    while A > 0 and B > 0:
        # Let a and b be the k-th pauli of i and j respectively.
        a = A % 4
        b = B % 4
        if a > 0 and b > 0 and a != b:  # Else no phase.
            flips = 1 - flips
            if (b - a) % 3 == 1:  # XY = iZ for instance.
                phase += 1
            elif (b - a) % 3 == 2:  # XZ = -iY for instance.
                phase += 3
        A //= 4
        B //= 4
    # phase -= 1  # We absorb one i.
    if flips:
        if phase % 4 == 3:
            phase = -1
        elif phase % 4 == 1:
            phase = 1
        else:
            raise Exception("Something went wrong with the phase.")
        return reduce(res), phase
    else:
        return None, 0


def single_convolve(A, B):
    """
    A and B are single pauli strings

    :param A: pauli string
    :param B: pauli string
    :return: dictionary of {pauli : coefficient}
    """
    res = {}
    for i in range(n):
        shift_B = B * (16 ** i)
        truncate_top = shift_B % (16 ** n)  # Rotate
        truncate_bottom = shift_B // (16 ** n)  # Rotate

        # E.g., ABC00 -> C00 + AB

        key, val = commute(A, truncate_bottom + truncate_top)
        if key is not None:
            if key in res:
                res[key] += val
            else:
                res[key] = val
    return res


def convolve(A, B):
    """
    A and B are dictionaries of {pauli : coefficient}
    """
    res = {}
    for a in A:
        for b in B:
            new = single_convolve(a, b)
            for n in new:
                if n in res:
                    res[n] += A[a] * B[b] * new[n]
                else:
                    res[n] = A[a] * B[b] * new[n]
    # Remove zero coefficients
    remove = []
    for r in res.keys():
        if res[r] == 0:
            remove.append(r)
    for r in remove:
        del res[r]
    return res


def pretty(A):
    """
    Print a pauli dictionary in a pretty way.
    """
    res = ""
    for a in A:
        if A[a] != 1 and A[a] != -1:
            res += str(A[a])
        elif A[a] == -1:
            res += "-"
        if a == 0:
            res += "I"
        else:
            while a > 0:
                res += "IXYZ"[a % 4]
                a //= 4
        res += " + "
    return res[:-3]


def array(A):
    """
    Return a numpy array of the pauli dictionary
    """
    res = np.zeros(num_basis)
    for a in A:
        res[a] = A[a]
    return res


def cycle(A):
    res = []
    permutations = [(0, 1, 2, 3), (0, 1, 3, 2), (0, 2, 1, 3),
                    (0, 2, 3, 1), (0, 3, 1, 2), (0, 3, 2, 1)]
    for p in permutations:
        new = {}
        for i in A:
            idx = 0
            for j in range(n):  # lmao oof
                # Let a be the j-th pauli of i.
                a = (i // 4**j) % 4
                idx += p[a] * 4**j
            new[reduce(idx)] = A[i]
        res.append(new)

    # Now, try cyclic slides.
    for p in permutations:
        new = {}
        for i in A:
            idx = 0
            for j in range(n):
                # Let a be the j-th pauli of i.
                a = (i // 4**j) % 4
                idx += p[a] * 4**(j + 1)
            new[reduce(idx)] = A[i]
        res.append(new)

    return res


space = []
iqueue = []

for i in range(16):
    space.append({i: 1})  # AB

iqueue.append(0)  # I lol
iqueue.append(1)  # X
iqueue.append(4)  # IX

for i in range(1, 4):
    for j in range(1, 4):
        space.append({i*4 + j * 16: 1})  # IAB for A,B in {X,Y,Z}


iqueue.append(len(space)-2)  # ZY
# ZZ # These are the only two distinguishable under cycling.
iqueue.append(len(space)-1)

# Pretty-print the space

# instructions = []
vector_space = []
for i, s in enumerate(space):
    # print(i, pretty(s))
    # instructions.append(pretty(s))
    vector_space.append(array(s))

# Representative elements of 3-qubit Paulis are
# ZZZ, XYX (which are known to be doable)
# and XYZ, XXY. Add XYZ = 1 * 4^ 0 + 2 * 4^1 + 3 * 4^2 = 1 + 8 + 48 = 57
# and XXY = 1 * 4^0 + 1 * 4^1 + 2 * 4^2 = 1 + 4 + 32 = 37
# and XIX = 1 * 4^0 + 0 * 4^1 + 1 * 4^2 = 1 + 16 = 17
# and XIY = 1 * 4^0 + 0 * 4^1 + 2 * 4^2 = 1 + 32 = 33
# Similarly, add:
# XXXX = 1 * 4^0 + 1 * 4^1 + 1 * 4^2 + 1 * 4^3 = 1 + 4 + 16 + 64 = 85
# XXXY = 1 * 4^0 + 1 * 4^1 + 1 * 4^2 + 2 * 4^3 = 1 + 4 + 16 + 128 = 149
# XXYY = 1 * 4^0 + 1 * 4^1 + 2 * 4^2 + 2 * 4^3 = 1 + 4 + 32 + 128 = 165
# XYXY = 1 * 4^0 + 2 * 4^1 + 1 * 4^2 + 2 * 4^3 = 1 + 8 + 16 + 128 = 153
# XXYZ = 1 * 4^0 + 1 * 4^1 + 2 * 4^2 + 3 * 4^3 = 1 + 4 + 32 + 192 = 229
# XYYZ = 1 * 4^0 + 2 * 4^1 + 2 * 4^2 + 3 * 4^3 = 1 + 8 + 32 + 192 = 233
target_qubits = [57, 37, 17, 33]
#  , 85, 149, 165, 153, 229, 233]
target_vectors = [array({target_qubits[i]: 1})
                  for i in range(len(target_qubits))]


def singular(M):
    mat = np.array(M)
    rank = np.linalg.matrix_rank(mat)
    return rank < len(M)


# i = 0


# Save all output in the below in a file, appending
f = open("tier_output.txt", "a")

SIMPLE_ONLY = True

while len(iqueue) > 0:
    i = iqueue.pop(0)
    print(" ------------------ ")
    # print("iqueue: ", iqueue)
    print(i, " => ", pretty(space[i]))
    f.write(" ------------------ \n")
    f.write(str(i) + " => " + pretty(space[i]) + "\n")
    for j in range(i):
        assert len(vector_space) == len(space)
        res = convolve(space[i], space[j])
        if len(res) == 0:
            continue
        if SIMPLE_ONLY and len(res) > 1:
            continue

        # print(pretty(res), " = (", pretty(
        #     space[i]), " * ", pretty(space[j]), ")")
        vector = array(res)
        # Check if vector is in span of vector_space
        vector_space.append(vector)
        # print([i[:25] for i in vector_space])
        if singular(vector_space):
            vector_space.pop()
            # print("Rejected")
        else:
            # print("Accepted")
            space.append(res)
            cycle_space = cycle(res)
            # Add all the new elements to space, checking rank
            for c in cycle_space[1:]:  # Skip the first one, which is just new
                vector_space.append(array(c))
                if singular(vector_space):
                    vector_space.pop()
                else:
                    space.append(c)

            iqueue.append(len(space)-1)

            # instructions.append(
            #     "(" + instructions[i] + " * " + instructions[j] + ")")
            # print(pretty(res), " = ", instructions[-1])
            print(pretty(res), " = (", pretty(
                space[i]), " * ", pretty(space[j]), ")")

            f.write(pretty(res) + " = (" + pretty(space[i]) +
                    " * " + pretty(space[j]) + ")\n")

            # Check if 3-qubit Paulis are in the space
            # print(len(vector_space), len(space))
            # k = [_[:] for _ in vector_space]

            # for l in range(len(target_vectors)):
            #     vector_space.append(target_vectors[l])
            #     if singular(vector_space):
            #         print("\n\nPauli",
            #               pretty({target_qubits[l]: 1}), "is in the space!!\n\n")
            #         f.write("\n\nPauli" + pretty({target_qubits[l]: 1}) +
            #                 "is in the space!!\n\n")
            #         target_vectors.remove(target_vectors[l])
            #         target_qubits.remove(target_qubits[l])
            #     vector_space.pop()

            # print(all((vector_space[i] == k[i]).all()
            #       for i in range(len(k))))
            # print(len(vector_space), len(space))

    # i += 1
    f.flush()

f.close()
