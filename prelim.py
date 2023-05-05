import numpy as np
from scipy.stats import rv_continuous


def haar_random_unitary():
    alpha, psi, chi = 2 * np.pi * np.random.uniform(size=3)

    eta = np.arcsin(np.sqrt(np.random.uniform(0, 1)))

    U = np.exp(1j * alpha) * np.array(
        [
            [np.exp(1j * psi) * np.cos(eta), np.exp(1j * chi) * np.sin(eta)],
            [-np.exp(-1j * chi) * np.sin(eta),
             np.exp(-1j * psi) * np.cos(eta)],
        ]
    )
    return U


# Nice printing:
np.set_printoptions(precision=3)
np.set_printoptions(suppress=True, edgeitems=30, linewidth=100000)


U = haar_random_unitary()
print(U)

eigenvals, eig = np.linalg.eig(U)
print("Eigenvalues:\n", eigenvals)
print("Eigenvectors:\n", eig)

print("Diagonalization:\n", eig.T.conjugate() @ U @ eig)

# Okay, here's the 3-qubit run.

UUU = np.kron(U, np.kron(U, U))
print("Big matrix (Real Part):")
print(UUU.real)
eigenvals, eig = np.linalg.eig(UUU)
# print("Eigenvalues:\n", eigenvals)
# print("Eigenvectors:\n", eig)

CZ = np.diag([1, 1, 1, -1, 1, -1, -1, -1])
print("CZ:")
print(CZ)

round_1 = UUU @ CZ
print("Round 1: (Real part)")
print(round_1.real)
print("Round 1: (Imaginary part)")
print(round_1.imag)
eigenvals, eig = np.linalg.eig(round_1)
print("Eigenvalues: (Real part)\n", eigenvals.real)
print("Eigenvalues: (Imaginary part)\n", eigenvals.imag)
print("Eigenvectors: (Real part)\n", eig.real)
print("Eigenvectors: (Imaginary part)\n", eig.imag)
print("Diagonalization: (Real part)\n",
      (eig.T.conjugate() @ round_1 @ eig).real)
print("Diagonalization: (Imaginary part)\n",
      (eig.T.conjugate() @ round_1 @ eig).imag)
