# QORANGE

## Installation

To install the qorange package:

```
pip install qorange
```

![screenshot](qorange_logo.png)
# Quantum Circuit Design Notes

## Overview
This document outlines the initial design goals and structure for building a quantum circuit simulation program. The Minimum Viable Product (MVP) requirements, potential future features, and suggested structure are provided below.

---

## Minimum Viable Product (MVP)

### Input
- **Qubits**: `{|q_1>, |q_2>}`
  - Each qubit can be represented as a complex vector in 2-dimensional space.
  - Provide a method to construct the combined state of qubits, specifically using the tensor product.

### Gates
- **4x4 Unitary Matrices**:
  - Allow users to specify arbitrary unitary 4x4 matrices.
  - Provide a standard library of predefined single and two-qubit gates for common operations.

### Output
- **State Representation**:
  - Implement functionality to display the state of the output qubits as a complex vector of length 4.
- **Measurement**:
  - Optionally include a Monte Carlo backend to simulate "shots" (experiments) and produce statistically reliable measurement outcomes.

---

## Future Features

### Visualizations
- Add capabilities to visualize the quantum circuit and its operations.

### Ancilla Qubits
- Support for additional auxiliary qubits (ancilla qubits) to facilitate advanced quantum algorithms.

---

## Structure

The program is organized using an Object-Oriented Programming (OOP) approach. The primary classes are:

1. **Circuit Class**: Represents the entire quantum circuit and manages the sequence of operations.
2. **Qubit Class**: Represents individual qubits with their associated state information.
3. **Gate Class**: Represents various quantum gates, including unitary transformations and standard gate operations.

--- 
# Generating Documentation

To generate the documentation for the `qorange` package, run the following from the terminal:
NOTE: Ensure you are in the `QORANGE` main folder. You may be required to run `conda install nbsphinx`.
```
sphinx-apidoc -o docs/source/ qorange
cd docs
make clean
make html
```
Pre-generated documentation can be found in `QORANGE\docs\build\html`

# Distribution

To create a new build, run:

```
python3 setup.py sdist bdist_wheel
```

Then to upload to PyPI, run the following. (You will need a PyPI account and an API key.)

```
python3 -m twine upload dist/*
```
