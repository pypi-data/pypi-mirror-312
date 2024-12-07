import numpy as np
import numpy.testing as npt
from qorange.circuits import QuantumCircuit
from qorange.gates import *

def test_circuit_meas_1():
    '''
    Test the circuit with a Hadamrd gate on the first qubit and a CNOT gate.
    '''
    # Apply the gates
    circuit = QuantumCircuit()
    circuit.apply_gate(Hadamard(), 1)  # Apply Hadamard on qubit 1
    circuit.apply_gate(CNOT(), (1, 2))  # Apply CNOT with qubit 1 as control, qubit 2 as target

    expected_outcome_1 = [0.5, 0.5]
    expected_outcome_2 = [0.5, 0.5]
    # Measure qubit 1
    outcome_1 = circuit.measure_qubit_computational(1)
    # Measure qubit 2
    outcome_2 = circuit.measure_qubit_computational(2)
    npt.assert_allclose(outcome_1, expected_outcome_1)
    npt.assert_allclose(outcome_2, expected_outcome_2)

def test_circuit_meas_2():
    '''
    Test the circuit with a Pauli-X gate on the first qubit and a SWAP gate.
    '''
    # Apply the gates
    circuit = QuantumCircuit()
    circuit.apply_gate(PauliX(), 1)  # Apply X gate to the first qubit
    circuit.apply_gate(SWAP())  # Apply SWAP gate between qubits 1 and 2

    expected_outcome_1 = [1, 0]
    expected_outcome_2 = [0, 1]
    # Measure qubit 1
    outcome_1 = circuit.measure_qubit_computational(1)
    # Measure qubit 2
    outcome_2 = circuit.measure_qubit_computational(2)
    npt.assert_allclose(outcome_1, expected_outcome_1)
    npt.assert_allclose(outcome_2, expected_outcome_2)

def test_circuit_meas_3():
    '''
    Test the circuit with Hadamard, X, and Hadamard gates on the first qubit.
    '''
    # Apply the gates
    circuit = QuantumCircuit()
    circuit.apply_gate(Hadamard(), 1)  # Apply Hadamard to the first qubit
    circuit.apply_gate(PauliX(), 1)   # Apply X gate to the first qubit
    circuit.apply_gate(Hadamard(), 1)  # Apply Hadamard again to the first qubit

    expected_outcome_1 = [1, 0]
    expected_outcome_2 = [1, 0]
    # Measure qubit 1
    outcome_1 = circuit.measure_qubit_computational(1)
    # Measure qubit 2
    outcome_2 = circuit.measure_qubit_computational(2)
    npt.assert_allclose(outcome_1, expected_outcome_1)
    npt.assert_allclose(outcome_2, expected_outcome_2)

def test_circuit_meas_4():
    '''
    Test the circuit with the S gate applied to a qubit initialized in the 1 state.
    '''
    # Apply the gates
    circuit = QuantumCircuit()
    circuit.apply_gate(PauliX(), 1)  # Apply X gate to the first qubit
    circuit.apply_gate(S(), 1)  # Apply S gate to the first qubit

    # Expected outcomes:
    # The S gate applies a phase of i to the |1> state.
    expected_outcome_1 = [0, 1]  # Probability of measuring |1> is 1
    expected_outcome_2 = [1, 0]  # Qubit 2 remains untouched in |0>

    # Measure qubit 1
    outcome_1 = circuit.measure_qubit_computational(1)
    # Measure qubit 2
    outcome_2 = circuit.measure_qubit_computational(2)

    # Assertions
    npt.assert_allclose(outcome_1, expected_outcome_1)
    npt.assert_allclose(outcome_2, expected_outcome_2)

def test_circuit_meas_5():
    '''
    Test the circuit with the T gate applied to a qubit initialized in the 1 state.
    '''
    # Apply the gates
    circuit = QuantumCircuit()
    circuit.apply_gate(PauliX(), 1)  # Apply X gate to the first qubit
    circuit.apply_gate(T(), 1)  # Apply T gate to the first qubit

    # Expected outcomes:
    # The T gate applies a phase of e^(iπ/4) to the |1> state.
    expected_outcome_1 = [0, 1]  # Probability of measuring |1> is 1
    expected_outcome_2 = [1, 0]  # Qubit 2 remains untouched in |0>

    # Measure qubit 1
    outcome_1 = circuit.measure_qubit_computational(1)
    # Measure qubit 2
    outcome_2 = circuit.measure_qubit_computational(2)

    # Assertions
    npt.assert_allclose(outcome_1, expected_outcome_1)
    npt.assert_allclose(outcome_2, expected_outcome_2)
