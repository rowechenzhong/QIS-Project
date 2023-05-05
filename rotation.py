import numpy as np

# Create a 2**n by 2**n matrix that sends bitstring abc... to bc...a. (Rotation)


def rotation(n):
    rot = np.zeros((2**n, 2**n), dtype=np.int8)
    for i in range(2**n):
        rotate_bit = (i * 2) % (2**n) + i // (2**(n-1))
        rot[i, rotate_bit] = 1
    return rot


# Print rotation(4) with {} brackets
res = rotation(4)
print("{")
for row in res:
    print("{" + ", ".join(str(x) for x in row) + "},")
print("}")
