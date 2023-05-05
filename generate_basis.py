import numpy as np


def generate(QUBITS):
    # We will interate through all bitstrings.
    # For each bitstring, we will append that bitstring
    # as well as all cyclic permutations of that bitstring
    # to the list of bitstrings.

    bitstrings = np.zeros((2 ** QUBITS, 2 ** QUBITS), dtype=complex)
    # This is just for printing. omega^phase.
    phase = np.zeros((2 ** QUBITS, 2 ** QUBITS), dtype=int)

    subspace_size = (2 ** QUBITS - 2) // QUBITS

    seen = set()

    # The 0...0 and 1...1 bitstrings belong in the symmetric subspace.
    bitstrings[0][0] = 1
    bitstrings[1][2 ** QUBITS - 1] = 1

    phase[0][0] = 0
    phase[1][2 ** QUBITS - 1] = 0

    idx = 2

    for i in range(1, 2 ** QUBITS - 1):
        # Turn it into an array of bits.
        if i in seen:
            continue
        bitstring = [int(x) for x in bin(i)[2:].zfill(QUBITS)]
        for subspace in range(QUBITS):
            for j in range(QUBITS):
                rotation = np.roll(bitstring, j)
                rotation = int(''.join(str(x) for x in rotation), 2)
                seen.add(rotation)
                bitstrings[idx + subspace * subspace_size][rotation] = np.exp(
                    2 * np.pi * 1j * subspace * j / QUBITS) / np.sqrt(QUBITS)  # Symmetry
                phase[idx + subspace *
                      subspace_size][rotation] = subspace * j % QUBITS
        idx += 1
    return bitstrings, phase


if __name__ == "__main__":

    QUBITS = 3
    bitstrings, phase = generate(QUBITS)

    # Nice printing:
    np.set_printoptions(precision=3)
    np.set_printoptions(suppress=True, edgeitems=30, linewidth=100000)

    print("Bitstrings:")
    print(bitstrings)
    # print(bistrings.real)
    # print(bistrings.imag)

    print("Phase:")
    print(phase)
    print("Mathematica printout:")
    res = "{"
    for i in range(2 ** QUBITS):
        s = "{"
        # find number of nonzero entries in bitstrings[i]
        normalization = np.count_nonzero(bitstrings[i])
        for j in range(2 ** QUBITS):
            if bitstrings[i][j] == 0:
                s += "0,"
                continue
            if phase[i][j] == 0:
                s += "1,"
            else:
                s += f"w^{phase[i][j]},"
            if normalization != 1:
                s = s[:-1] + f"/Sqrt[{normalization}],"
        s = s[:-1] + "}"
        res += s + ",\n"
    res = res[:-2] + "}"
    print(res)
