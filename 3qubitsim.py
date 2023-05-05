import numpy as np
from scipy.stats import rv_continuous
from scipy.stats import unitary_group

import generate_basis


basis, _ = generate_basis.generate(3)
Sbasis = basis[:4]
# Check that it's orthonormal.
assert np.allclose(Sbasis @ Sbasis.conj().T, np.identity(4))
# projector = basis.conj().T @ basis
# print(projector)


# Nice printing:
np.set_printoptions(precision=3)
np.set_printoptions(suppress=True, edgeitems=30, linewidth=100000)

# Find some unitary matrices with Haar measure.
tests = [unitary_group.rvs(4) for i in range(1000)]

# for i in range(10):
#     print(tests[i])
#     print()

# Generate some easy tests that are guaranteed to be accesible
M = np.identity(8)

easytests = []
for i in range(100):
    U = unitary_group.rvs(2)
    UUU = np.kron(U, np.kron(U, U))
    CZ = np.diag([1, 1, 1, -1, 1, -1, -1, -1])
    M = CZ @ UUU @ M
    if i >= 50:
        easytests.append(Sbasis @ M @ Sbasis.conj().T)
print(easytests[0] @ easytests[0].conj().T)  # Should be identity.


best = [np.inf for i in range(1000)]
easybest = [np.inf for i in range(50)]
M = np.identity(8)

for i in range(10000):
    U = unitary_group.rvs(2)
    UUU = np.kron(U, np.kron(U, U))
    CZ = np.diag([1, 1, 1, -1, 1, -1, -1, -1])

    M = CZ @ UUU @ M

    # print("Diagonalized M:")
    # print(basis @ M @ basis.conj().T)

    # print("Symmetrized M:")
    # print(Sbasis @ M @ Sbasis.conj().T)

    # Find distance between M and all tests
    dists = [np.linalg.norm(Sbasis @ M @ Sbasis.conj().T - test)
             for test in tests]
    easydists = [np.linalg.norm(Sbasis @ M @ Sbasis.conj().T - test)
                 for test in easytests]
    # print(dists[:5])
    best = [min(best[i], dists[i]) for i in range(1000)]
    easybest = [min(easybest[i], easydists[i]) for i in range(50)]
    if i % 100 == 0:
        print(max(best), min(best), max(easybest), min(easybest))

print(M)
print(M @ M.conj().T)

# Find the matrix with the largest distance to all tests
print(max(best))
print(tests[best.index(max(best))])

print(min(best))
print(tests[best.index(min(best))])
