This repository contains Rowechen Zhong's 8.371
final project.

The various files, in order of relevance, are as follows:

- Tiercommutator encodes operators as dictionaries of {pauli string
  : coefficient}
  pairs. This takes advantage of the relative sparsity of the
  operators involved
  to accelerate computation.
- vectorcommutator encodes operators as vectors of 4^N coefficients.
- 3qubitReducedVanillaoutput.txt contains the output for N = 6 qubits,
  demonstrating the main theorem of the paper in this case.
