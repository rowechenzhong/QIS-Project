import numpy as np
from scipy.stats import rv_continuous
from scipy.stats import unitary_group


X = np.array([[0, 1], [1, 0]])
Y = np.array([[0, -1j], [1j, 0]])
Z = np.array([[1, 0], [0, -1]])


def prettyprint(M):
    """
    Print a matrix with only 1, -1, i, -i, 0
    print as '  1 ', ' -1 ', '  i ', ' -i ', '  0 '
    """
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            if M[i, j] == 1:
                print('  1 ', end='')
            elif M[i, j] == -1:
                print(' -1 ', end='')
            elif M[i, j] == 1j:
                print('  i ', end='')
            elif M[i, j] == -1j:
                print(' -i ', end='')
            elif M[i, j] == 0:
                print('  0 ', end='')
            else:
                print(M[i, j], end='')
        print()


seen = [
    1j * np.kron(X, np.eye(2)),
    1j * np.kron(np.diag([0, 1]), X),
    # 1j * np.kron(Y, Z)
    # 1j * np.kron(X, X) # We can't actually make this one.

    # 1j * np.kron(np.diag([0, 1]), Y)
    1j * np.diag([0, 0, -1, 1])
    # 1j * np.diag([1, -1, 0, 0])
]
names = ["MF", "MG", "MH"]
#   "MI"]
# , "MJ", "MK"]


def split(M):
    """
    Take a 4x4 matrix M and
    turn it into a (32,) array
    with the real entries followed by the imaginary entries
    """
    return np.concatenate((M.real.flatten(), M.imag.flatten()))


flattened_seen = [split(i) for i in seen]

for i in seen:
    prettyprint(i)
    print()

print("-------------------------")
checked = 0
# do = 0
while len(seen) != checked:
    print(len(seen))
    M = seen[checked]
    for j in range(checked + 1, len(seen)):
        # do += 1
        # if do > 2:
        #     break
        N = seen[j]
        K = M @ N - N @ M
        # If K is linearly independent from all seen matrices, add it to seen.
        if np.allclose(K, 0):
            continue
        # prettyprint(K)
        # print()

        flattened_seen.append(split(K))

        arrayflattened = np.array(flattened_seen)
        u, s, vh = np.linalg.svd(arrayflattened)
        # print(s)
        if s[-1] > 1e-3:
            print(names[checked], names[j])

            seen.append(K)
            print("Added")
            names.append("K[" + names[checked] + "," + names[j] + "]")
        else:
            flattened_seen.pop()
            # print("Not added")
    checked += 1
print(len(seen))
