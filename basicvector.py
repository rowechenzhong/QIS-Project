import numpy as np
import random

n = 2
qubits = 2 * n
num_basis = 4**(qubits)

space = []
instructions = []

# We can do IIIIII lol
res = np.zeros(num_basis, dtype=np.int8)
res[0] = 1
instructions.append("I")

space.append(res)

for A in range(1, 4):
    # 1-qubit operators
    res = np.zeros(num_basis, dtype=np.int8)
    for i in range(n):
        res[A * 4**(2 * i)] = 1
    space.append(res)
    instructions.append("IXYZ"[A])
    res = np.zeros(num_basis, dtype=np.int8)
    for i in range(n):
        res[A * 4**(2 * i + 1)] = 1
    space.append(res)
    instructions.append("I" + "IXYZ"[A])

for A in range(1, 4):
    for B in range(1, 4):
        # 2-qubit operators
        res = np.zeros(num_basis, dtype=np.int8)
        for i in range(n):
            res[(A + 4 * B) * 4**(2 * i)] = 1
        space.append(res)
        instructions.append("IXYZ"[A] + "IXYZ"[B])
        res = np.zeros(num_basis, dtype=np.int8)
        for i in range(n-1):
            res[(A + 4 * B) * 4**(2 * i + 1)] = 1
        # Finally, BIIIIA
        res[B + 4**(qubits - 1) * A] = 1
        space.append(res)
        instructions.append("I" + "IXYZ"[A] + "IXYZ"[B])


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
f = open("2output.txt", "a")

for i in range(len(space)):
    print(print_pauli(space[i]), instructions[i])
    f.write(print_pauli(space[i]) + " " + instructions[i] + "\n")


def commutator(A, B):
    """
    A is a pauli string in the form of a 4096-tuple of real numbers.
    B is also a pauli string.
    """
    res = np.zeros(num_basis, dtype=np.int8)

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
                if a > 0 and b > 0:
                    if a != b:
                        if (b - a) % 3 == 1:
                            phase += 1
                        elif (a - b) % 3 == 1:
                            phase += 3
            phase %= 4
            if phase == 1:
                res[i ^ j] += A[i] * B[j]
            elif phase == 3:
                res[i ^ j] -= A[i] * B[j]
    return res


RESTRICT_SUM = False

####################
# Vanilla
####################

print("Vanilla (random)")
f.write("Vanilla (random)\n")

i = 0
while i < len(space):
    print(i, print_pauli(space[i]))
    for j in range(i):
        new = commutator(space[j], space[i])
        if np.count_nonzero(new) == 0:
            continue
        gcd = np.gcd.reduce(new)
        new //= gcd
        space.append(new)
        mat = np.array(space)
        rank = np.linalg.matrix_rank(mat)
        if rank < len(space):
            space.pop()
            continue
        print(len(space), ": ", print_pauli(
            new) + " = [" + print_pauli(space[j]) + ", " + print_pauli(space[i]) + "] / " + str(gcd))
        f.write(print_pauli(new) + " = [" + print_pauli(space[j]) +
                ", " + print_pauli(space[i]) + "] / " + str(gcd) + "\n")
    i += 1
f.close()
