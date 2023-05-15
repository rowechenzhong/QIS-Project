import pickle
import numpy as np
import scipy.linalg


# load the data
with open("cylinderQR4spaceSKIP.pkl", "rb") as f:
    space = pickle.load(f)


# with open("cylinderQR4space.pkl", "rb") as f:
#     space2 = pickle.load(f)

space = np.array(space)
# space2 = np.array(space2)
print(space.shape)
# print(space2.shape)

# print rank of space
M = np.array(space).T
# r, = scipy.linalg.qr(M, mode='r')  # scipy linalg
# indicies = np.logical_not(np.isclose(np.diagonal(r), 0))
# print("Rank:", sum(indicies))

# print rank of space using SVD
u, s, vh = np.linalg.svd(M)
print("Rank:", sum(s > 1e-10))

# bothspaces = np.concatenate((space, space2), axis=0)
# print(bothspaces.shape)

# # print rank of space
# M = np.array(bothspaces).T
# r, = scipy.linalg.qr(M, mode='r')  # scipy linalg
# indicies = np.logical_not(np.isclose(np.diagonal(r), 0))
# print("Rank:", sum(indicies))

# # print rank of space using SVD
# u, s, vh = np.linalg.svd(bothspaces)
# print("Rank:", sum(s > 1e-10))

# n = 3
# qubits = 2*n
# num_basis = 4**qubits


# def print_pauli(pauli):
#     """
#     Print a pauli string in the form of a 4096-tuple of real numbers.
#     """
#     res = ""
#     for i in range(num_basis):
#         if pauli[i] == 0:
#             continue
#         res += str(pauli[i]) + " * "
#         for j in range(qubits):
#             # Let a be the j-th pauli of i.
#             a = (i // 4**j) % 4
#             res += "IXYZ"[a]
#         res += " + "
#     return res[:-3]


# # For all symmetric operators...
# for i in range(num_basis):
#     # construct all cylic permutations of the operator
#     res = np.zeros((num_basis,))
#     for j in range(n):
#         # Let a be the j-th pauli of i.
#         a = (i // 16**j)
#         b = i % 16**j
#         res[b*16**(n-j) + a] = 1
#     print(print_pauli(res))

#     # Concate the operator to space
#     newspace = np.concatenate((space, [res]), axis=0)
#     # Find the rank of the new space
#     M = np.array(newspace).T
#     r, = scipy.linalg.qr(M, mode='r')  # scipy linalg
#     indicies = np.logical_not(np.isclose(np.diagonal(r), 0))
#     print("Rank:", sum(indicies))

#     if sum(indicies) > 1374:
#         print("Found a new operator!")
#         print("---------------------------------")
