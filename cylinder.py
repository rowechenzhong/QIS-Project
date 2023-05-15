import numpy as np
import random

n = 3
qubits = 2 * n

cut = 4**n

num_basis = 4**(qubits)

TOTAL = 1376

RESTRICT_SUM = True


space = []

instructions = []

iqueue = []
jqueue = []

# We can do IIIIII lol
res = np.zeros(num_basis, dtype=np.int8)
res[0] = 1
instructions.append("I")

iqueue.append(len(space))
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
    instructions.append("ixyz"[A])

iqueue.append(len(space)-1)

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
        instructions.append("ixyz"[A] + "ixyz"[B])


iqueue.append(len(space)-3)
iqueue.append(len(space)-1)
jqueue = iqueue[:]


def print_pauli(pauli):
    """
    Print a pauli string in the form of a 4096-tuple of real numbers.
    """
    res = ""
    for i in range(num_basis):
        if pauli[i] == 0:
            continue
        if RESTRICT_SUM:
            for j in range(qubits):
                # Let a be the j-th pauli of i.
                a = (i // 4**j) % 4
                res += "IXYZ"[a]
            return res.strip("I")
        res += str(pauli[i]) + " * "
        for j in range(qubits):
            # Let a be the j-th pauli of i.
            a = (i // 4**j) % 4
            res += "IXYZ"[a]
        res += " + "
    return res[:-3]


# Save all output in the below in a file, appending
f = open("2output.txt", "a")


# instructions = ["Start"] * len(space)
# print(space)
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
                # Let a and b be the k-th pauli of i and j respectively.
                a = (i // 4**k) % 4
                b = (j // 4**k) % 4
                # We need the stupid phase. If a and b are both >0 and a - b = 1 mod 3,
                # then we have a phase, e.g. [Y,X] = -2iZ
                # Also, we need to count the number of flips, like [X,Y], where
                # both are different and not 1; if the number of flips is even
                # then the commutator is 0.
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


# def cycle(A):
#     # A is a pauli string. Return the pauli strings with (X, Y, Z)
#     # replaced by all permutations (3! = 6 total)
#     # In addition, try cyclic slides.
#     res = []
#     permutations = [(0, 1, 2, 3), (0, 1, 3, 2), (0, 2, 1, 3),
#                     (0, 2, 3, 1), (0, 3, 1, 2), (0, 3, 2, 1)]
#     for p in permutations:
#         new = np.zeros(num_basis, dtype=np.int8)
#         for i in range(num_basis):
#             if A[i] == 0:
#                 continue
#             idx = 0
#             for j in range(qubits):
#                 # Let a be the j-th pauli of i.
#                 a = (i // 4**j) % 4
#                 idx += p[a] * 4**j
#             new[idx] = A[i]
#         # Check that new is not close to anything in res
#         # for r in res:
#         #     if np.linalg.norm(new - r) < 1e-6:
#         #         break
#         # else:
#         res.append(new)

#     # Now, try cyclic slides.
#     for p in permutations:
#         new = np.zeros(num_basis, dtype=np.int8)
#         for i in range(num_basis):
#             if A[i] == 0:
#                 continue
#             idx = 0
#             for j in range(qubits):
#                 # Let a be the j-th pauli of i.
#                 a = (i // 4**j) % 4
#                 idx += p[a] * 4**((j + 1) % qubits)
#             new[idx] = A[i]
#         # Check that new is not close to anything in res
#         # for r in res:
#         #     if np.linalg.norm(new - r) < 1e-6:
#         #         break
#         # else:
#         res.append(new)

#     return res


# def check_complexity(A, cap):
#     """
#     Return true iff A (a vector of pauli strings) contains at most
#     cap entries that are not X, Y, or Z.
#     """
#     for i in range(num_basis):
#         if A[i] == 0:
#             continue
#         count = 0

#         for j in range(qubits):
#             # Let a be the j-th pauli of i.
#             a = (i // 4**j) % 4
#             if a > 0:
#                 count += 1
#                 if count > cap:
#                     # print("Rejected: " + print_pauli(A))
#                     return False
#     return True

# Okay, finally.
# Now, I want to see how many different linearly
# independent operators we can generate through commutators.


# queue = set()

# for i in range(len(space)):
#     for j in range(i):
#         queue.add((j, i))

# space_set = set(tuple(i) for i in space)

# print some debug...
# debug = list(space_set)[0]
# print(debug[:100])


# while len(iqueue) > 0:
#     i = iqueue.pop(0)
#     print(i, print_pauli(space[i]))
# # i = 0
# # while i < len(space):
#     # print("i = " + str(i), "len(space) = " + str(len(space)))
#     # j = 0
#     for j in range(i):
#         # while len(queue) > 0:
#         # Pick an (i,j) pair at random.
#         # i, j = random.sample(queue, 1)[0]
#         # queue.remove((i, j))
#         # i, j = queue.pop()
#         new = commutator(space[j], space[i])
#         if 0 < np.count_nonzero(new) <= n:

#             gcd = np.gcd.reduce(new)
#             new //= gcd
#             # # if check_complexity(new, 3):
#             # space.append(new)
#             # # Concatenate space into a matrix
#             # mat = np.array(space)
#             # # Find the rank of the matrix
#             # rank = np.linalg.matrix_rank(mat)
#             # # If the rank is less than the number of rows, then we have a linearly dependent set.
#             # if rank < len(space):
#             #     space.pop()
#             if tuple(new) in space_set or tuple(-new) in space_set:
#                 continue
#             else:
#                 cycle_space = cycle(new)

#                 space.append(new)
#                 space_set.add(tuple(new))

#                 # Add all the new elements to space, checking rank
#                 for c in cycle_space[1:]:  # Skip the first one, which is just new
#                     if tuple(c) in space_set or tuple(-c) in space_set:
#                         continue
#                     space.append(c)
#                     space_set.add(tuple(c))
#                     # mat = np.array(space)
#                     # rank = np.linalg.matrix_rank(mat)
#                     # if rank < len(space):
#                     #     space.pop()

#                 iqueue.append(len(space)-1)
#                 jqueue.append(len(space)-1)

#                 # Add the new commutator to the queue
#                 # for k in range(len(space)-1):
#                 #     queue.add((k, len(space)-1))
#                 # print(len(space))
#                 # if RESTRICT_SUM:
#                 # instructions.append(
#                 #     "[" + print_pauli(space[j]) + ", " + print_pauli(space[i]) + "]")

#                 print(len(space), ": ", print_pauli(
#                     new) + " = [" + print_pauli(space[j]) + ", " + print_pauli(space[i]) + "] / " + str(gcd))
#                 f.write(print_pauli(new) + " = [" + print_pauli(space[j]) +
#                         ", " + print_pauli(space[i]) + "] / " + str(gcd) + "\n")
#                 # f.write(print_pauli(new) + " = " + instructions[-1] + "\n")
#                 # else:
#                 #     instructions.append(
#                 #         "[" + instructions[j] + ", " + instructions[i] + "]")
#                 #     print(len(space), ": ", print_pauli(
#                 #         new) + " = " + instructions[-1])
#                 #     f.write(print_pauli(new) + " = " + instructions[-1] + "\n")

#                 # TODO: For the 3-qubit case, this turns out to be fast:
#                 # if len(space) >= 676:
#                 #     iqueue = []
#                 #     break

    # mat = np.array(space)
    # rank = np.linalg.matrix_rank(mat)
    # assert rank == len(space)
    # i += 1

RESTRICT_SUM = False

####################
# Vanilla
####################

print("Vanilla (random)")
f.write("Vanilla (random)\n")

while len(jqueue) > 0:
    i = jqueue.pop(0)
    print(i, print_pauli(space[i]))
    for j in range(i):
        # while len(space) < TOTAL:  # We expect there to be TOTAL operators in the end
        # i = random.randint(1, len(space)-1)
        # j = random.randint(0, i-1)
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

        # cycle_space = cycle(new)
        # # Add all the new elements to space, checking rank
        # for c in cycle_space[1:]:  # Skip the first one, which is just new
        #     space.append(c)
        #     mat = np.array(space)
        #     rank = np.linalg.matrix_rank(mat)
        #     if rank < len(space):
        #         space.pop()

        # jqueue.append(len(space)-1)

        print(len(space), ": ", print_pauli(
            new) + " = [" + print_pauli(space[j]) + ", " + print_pauli(space[i]) + "] / " + str(gcd))
        f.write(print_pauli(new) + " = [" + print_pauli(space[j]) +
                ", " + print_pauli(space[i]) + "] / " + str(gcd) + "\n")

f.close()
