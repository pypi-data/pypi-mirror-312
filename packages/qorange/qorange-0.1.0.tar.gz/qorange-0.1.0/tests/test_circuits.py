import numpy as np
import numpy.testing as npt
from qorange.circuits import QuantumCircuit
from qorange.gates import *

def test_circuit_bell():
    '''
    Test the Bell circuit for creating entanglement.
    '''
    circuit = QuantumCircuit()
    circuit.apply_gate(Hadamard(),1)
    circuit.apply_gate(CNOT(),(1,2))
    
    npt.assert_allclose(
        circuit.state, 
        np.array([1, 0, 0, 1])/np.sqrt(2)
    )

def test_circuit_1():
    '''
    Test the circuit with a Pauli-X gate on the first qubit and a SWAP gate.
    '''
    circuit = QuantumCircuit()
    circuit.apply_gate(PauliX(),1)  # Apply X gate to the first qubit
    circuit.apply_gate(SWAP())  # Apply SWAP gate between qubits 1 and 2

    expected_state = np.array([0, 1, 0, 0])

    # Verify the output state matches the expected state
    npt.assert_allclose(
        circuit.state,
        expected_state,
        rtol=1e-5,
        atol=1e-8
    )

def test_circuit_2():
    '''
    Test the circuit with Hadamard, X, and Hadamard gates on the first qubit.
    '''
    circuit = QuantumCircuit()
    circuit.apply_gate(Hadamard(),1)  # Apply Hadamard to the first qubit
    circuit.apply_gate(PauliX(),1)   # Apply X gate to the first qubit
    circuit.apply_gate(Hadamard(),1)  # Apply Hadamard again to the first qubit
    
    expected_state = np.array([1, 0, 0, 0])

    # Verify the output state matches the expected state
    npt.assert_allclose(
        circuit.state,
        expected_state,
        rtol=1e-5,
        atol=1e-8
    )

def test_circuit_3():
    '''
    Test the circuit with X, Hadamard, and CNOT gates.
    '''
    circuit = QuantumCircuit()
    circuit.apply_gate(PauliX(),1)  # Apply X gate to the first qubit
    circuit.apply_gate(Hadamard(),1)  # Apply Hadamard to the first qubit
    circuit.apply_gate(CNOT(),(1,2))  # Apply CNOT with qubit 1 as control, qubit 2 as target
    
    expected_state = np.array([1/np.sqrt(2), 0, 0, -1/np.sqrt(2)])

    # Verify the output state matches the expected state
    npt.assert_allclose(
        circuit.state,
        expected_state,
        rtol=1e-5,
        atol=1e-8
    )

def test_circuit_4():
    '''
    Test the circuit with a Pauli-Y gate on the first qubit and a SWAP gate.
    '''
    circuit = QuantumCircuit()
    circuit.apply_gate(PauliY(),1)  # Apply Y gate to the first qubit
    circuit.apply_gate(SWAP())  # Apply SWAP gate between qubits 1 and 2
    
    expected_state = np.array([0, 1j, 0, 0])

    npt.assert_allclose(
        circuit.state,
        expected_state
    )

def test_circuit_5():
    '''
    Test the circuit with Hadamard, Pauli-Z, and Hadamard gates on the first qubit.
    '''
    circuit = QuantumCircuit()
    circuit.apply_gate(Hadamard(),1)  # Apply Hadamard to the first qubit
    circuit.apply_gate(PauliZ(),1)   # Apply Z gate to the first qubit
    circuit.apply_gate(Hadamard(),1)  # Apply Hadamard again to the first qubit
    
    expected_state = np.array([0, 0, 1, 0])

    npt.assert_allclose(
        circuit.state,
        expected_state
    )

def test_circuit_6():
    '''
    Test the circuit with Hadamard on the first qubit and CZ gate.
    '''
    circuit = QuantumCircuit()
    circuit.apply_gate(Hadamard(),1)
    circuit.apply_gate(CZ(),(1,2))
    
    npt.assert_allclose(
        circuit.state, 
        np.array([1, 0, 1, 0])/np.sqrt(2)
    )

def test_circuit_7():
    '''
    Test the circuit with X, S on first qubit and SWAP gate.
    '''
    circuit = QuantumCircuit()
    circuit.apply_gate(PauliX(),1)  # Apply X gate to the first qubit
    circuit.apply_gate(S(), 1)      # Apply S gate (phase gate) to the first qubit
    circuit.apply_gate(SWAP())  # Apply SWAP gate between qubits 1 and 2

    expected_state = np.array([0, 1j, 0, 0])

    npt.assert_allclose(
        circuit.state,
        expected_state,
        rtol=1e-5,
        atol=1e-8
    )

def test_circuit_8():
    '''
    Test the circuit with X, T, and CNOT gates.
    '''
    circuit = QuantumCircuit()
    circuit.apply_gate(PauliX(),1)  # Apply X gate to the first qubit
    circuit.apply_gate(T(), 1)      # Apply T gate (phase gate) to the first qubit
    circuit.apply_gate(CNOT(),(1,2))  # Apply CNOT with qubit 1 as control and qubit 2 as target
    
    expected_state = np.array([0, 0, 0, np.sqrt(2) / 2 + 1j * np.sqrt(2) / 2])

    npt.assert_allclose(
        circuit.state,
        expected_state,
        rtol=1e-5,
        atol=1e-8
    )
