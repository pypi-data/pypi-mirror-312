import numpy as np
import numpy.testing as npt
from qorange.circuits import QuantumCircuit
from qorange.gates import *

STATE_00 = np.array([1, 0, 0, 0])
STATE_01 = np.array([0, 1, 0, 0])
STATE_10 = np.array([0, 0, 1, 0])
STATE_11 = np.array([0, 0, 0, 1])

###########################
# 1-QUBIT GATES
###########################

def test_identity_q1_state_00():
    '''
    Test the identity operator acting on qubit 1 of state |00>.
    '''
    circuit = QuantumCircuit()
    circuit.apply_gate(Identity(), 1)

    npt.assert_array_equal(circuit.state, STATE_00)

def test_identity_q1_state_01():
    '''
    Test the identity operator acting on qubit 1 of state |01>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_01
    circuit.apply_gate(Identity(), 1)

    npt.assert_array_equal(circuit.state, STATE_01)

def test_identity_q1_state_10():
    '''
    Test the identity operator acting on qubit 1 of state |10>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_10
    circuit.apply_gate(Identity(), 1)

    npt.assert_array_equal(circuit.state, STATE_10)

def test_identity_q1_state_11():
    '''
    Test the identity operator acting on qubit 1 of state |11>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_11
    circuit.apply_gate(Identity(), 1)

    npt.assert_array_equal(circuit.state, STATE_11)

def test_identity_q2_state_00():
    '''
    Test the identity operator acting on qubit 2 of state |00>.
    '''
    circuit = QuantumCircuit()
    circuit.apply_gate(Identity(), 2)

    npt.assert_array_equal(circuit.state, STATE_00)

def test_identity_q2_state_01():
    '''
    Test the identity operator acting on qubit 2 of state |01>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_01
    circuit.apply_gate(Identity(), 2)

    npt.assert_array_equal(circuit.state, STATE_01)

def test_identity_q2_state_10():
    '''
    Test the identity operator acting on qubit 2 of state |10>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_10
    circuit.apply_gate(Identity(), 2)

    npt.assert_array_equal(circuit.state, STATE_10)

def test_identity_q2_state_11():
    '''
    Test the identity operator acting on qubit 2 of state |11>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_11
    circuit.apply_gate(Identity(), 2)

    npt.assert_array_equal(circuit.state, STATE_11)

def test_pauli_x_q1_state_00():
    '''
    Test the Pauli X operator acting on qubit 1 of state |00>.
    '''
    circuit = QuantumCircuit()
    circuit.apply_gate(PauliX(), 1)

    npt.assert_array_equal(circuit.state, STATE_10)

def test_pauli_x_q1_state_01():
    '''
    Test the Pauli X operator acting on qubit 1 of state |01>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_01
    circuit.apply_gate(PauliX(), 1)

    npt.assert_array_equal(circuit.state, STATE_11)

def test_pauli_x_q1_state_10():
    '''
    Test the Pauli X operator acting on qubit 1 of state |10>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_10
    circuit.apply_gate(PauliX(), 1)

    npt.assert_array_equal(circuit.state, STATE_00)

def test_pauli_x_q1_state_11():
    '''
    Test the Pauli X operator acting on qubit 1 of state |11>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_11
    circuit.apply_gate(PauliX(), 1)

    npt.assert_array_equal(circuit.state, STATE_01)

def test_pauli_x_q2_state_00():
    '''
    Test the Pauli X operator acting on qubit 2 of state |00>.
    '''
    circuit = QuantumCircuit()
    circuit.apply_gate(PauliX(), 2)

    expected = np.array([0, 1, 0, 0]) # |01>

    npt.assert_array_equal(circuit.state, expected)

def test_pauli_x_q2_state_01():
    '''
    Test the Pauli X operator acting on qubit 2 of state |01>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_01
    circuit.apply_gate(PauliX(), 2)

    npt.assert_array_equal(circuit.state, STATE_00)

def test_pauli_x_q2_state_10():
    '''
    Test the Pauli X operator acting on qubit 2 of state |10>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_10
    circuit.apply_gate(PauliX(), 2)

    npt.assert_array_equal(circuit.state, STATE_11)

def test_pauli_x_q2_state_11():
    '''
    Test the Pauli X operator acting on qubit 2 of state |11>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_11
    circuit.apply_gate(PauliX(), 2)

    npt.assert_array_equal(circuit.state, STATE_10)

def test_pauli_y_q1_state_00():
    '''
    Test the Pauli Y operator acting on qubit 1 of state |00>.
    '''
    circuit = QuantumCircuit()
    circuit.apply_gate(PauliY(), 1)

    npt.assert_array_equal(circuit.state, 1j * STATE_10)

def test_pauli_y_q1_state_01():
    '''
    Test the Pauli Y operator acting on qubit 1 of state |01>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_01
    circuit.apply_gate(PauliY(), 1)

    npt.assert_array_equal(circuit.state, 1j * STATE_11)

def test_pauli_y_q1_state_10():
    '''
    Test the Pauli Y operator acting on qubit 1 of state |10>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_10
    circuit.apply_gate(PauliY(), 1)

    npt.assert_array_equal(circuit.state, -1j * STATE_00)

def test_pauli_y_q1_state_11():
    '''
    Test the Pauli Y operator acting on qubit 1 of state |11>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_11
    circuit.apply_gate(PauliY(), 1)

    npt.assert_array_equal(circuit.state, -1j * STATE_01)

def test_pauli_y_q2_state_00():
    '''
    Test the Pauli Y operator acting on qubit 2 of state |00>.
    '''
    circuit = QuantumCircuit()
    circuit.apply_gate(PauliY(), 2)

    npt.assert_array_equal(circuit.state, 1j * STATE_01)

def test_pauli_y_q2_state_01():
    '''
    Test the Pauli Y operator acting on qubit 2 of state |01>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_01
    circuit.apply_gate(PauliY(), 2)

    npt.assert_array_equal(circuit.state, -1j * STATE_00)

def test_pauli_y_q2_state_10():
    '''
    Test the Pauli Y operator acting on qubit 2 of state |10>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_10
    circuit.apply_gate(PauliY(), 2)

    npt.assert_array_equal(circuit.state, 1j * STATE_11)

def test_pauli_y_q2_state_11():
    '''
    Test the Pauli Y operator acting on qubit 2 of state |11>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_11
    circuit.apply_gate(PauliY(), 2)

    npt.assert_array_equal(circuit.state, -1j * STATE_10)

def test_pauli_z_q1_state_00():
    '''
    Test the Pauli Z operator acting on qubit 1 of state |00>.
    '''
    circuit = QuantumCircuit()
    circuit.apply_gate(PauliZ(), 1)

    npt.assert_array_equal(circuit.state, STATE_00)

def test_pauli_z_q1_state_01():
    '''
    Test the Pauli Z operator acting on qubit 1 of state |01>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_01
    circuit.apply_gate(PauliZ(), 1)

    npt.assert_array_equal(circuit.state, STATE_01)

def test_pauli_z_q1_state_10():
    '''
    Test the Pauli Z operator acting on qubit 1 of state |10>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_10
    circuit.apply_gate(PauliZ(), 1)

    npt.assert_array_equal(circuit.state, -STATE_10)

def test_pauli_z_q1_state_11():
    '''
    Test the Pauli Z operator acting on qubit 1 of state |11>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_11
    circuit.apply_gate(PauliZ(), 1)

    npt.assert_array_equal(circuit.state, -STATE_11)

def test_pauli_z_q2_state_00():
    '''
    Test the Pauli Z operator acting on qubit 2 of state |00>.
    '''
    circuit = QuantumCircuit()
    circuit.apply_gate(PauliZ(), 2)

    npt.assert_array_equal(circuit.state, STATE_00)

def test_pauli_z_q2_state_01():
    '''
    Test the Pauli Z operator acting on qubit 2 of state |01>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_01
    circuit.apply_gate(PauliZ(), 2)

    npt.assert_array_equal(circuit.state, -STATE_01)

def test_pauli_z_q2_state_10():
    '''
    Test the Pauli Z operator acting on qubit 2 of state |10>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_10
    circuit.apply_gate(PauliZ(), 2)

    npt.assert_array_equal(circuit.state, STATE_10)

def test_pauli_z_q2_state_11():
    '''
    Test the Pauli Z operator acting on qubit 2 of state |11>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_11
    circuit.apply_gate(PauliZ(), 2)

    npt.assert_array_equal(circuit.state, -STATE_11)

def test_hadamard_q1_state_00():
    '''
    Test the Hadamard operator acting on qubit 1 of state |00>.
    '''
    circuit = QuantumCircuit()
    circuit.apply_gate(Hadamard(), 1)
    
    npt.assert_allclose(circuit.state, 1 / np.sqrt(2) * (STATE_00 + STATE_10))

def test_hadamard_q1_state_01():
    '''
    Test the Hadamard operator acting on qubit 1 of state |01>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_01
    circuit.apply_gate(Hadamard(), 1)
    
    npt.assert_allclose(circuit.state, 1 / np.sqrt(2) * (STATE_01 + STATE_11))

def test_hadamard_q1_state_10():
    '''
    Test the Hadamard operator acting on qubit 1 of state |10>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_10
    circuit.apply_gate(Hadamard(), 1)
    
    npt.assert_allclose(circuit.state, 1 / np.sqrt(2) * (STATE_00 - STATE_10))

def test_hadamard_q1_state_11():
    '''
    Test the Hadamard operator acting on qubit 1 of state |11>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_11
    circuit.apply_gate(Hadamard(), 1)
    
    npt.assert_allclose(circuit.state, 1 / np.sqrt(2) * (STATE_01 - STATE_11))

def test_hadamard_q2_state_00():
    '''
    Test the Hadamard operator acting on qubit 2 of state |00>.
    '''
    circuit = QuantumCircuit()
    circuit.apply_gate(Hadamard(), 2)

    npt.assert_allclose(circuit.state, 1 / np.sqrt(2) * (STATE_00 + STATE_01))

def test_hadamard_q2_state_01():
    '''
    Test the Hadamard operator acting on qubit 2 of state |01>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_01
    circuit.apply_gate(Hadamard(), 2)
    
    npt.assert_allclose(circuit.state, 1 / np.sqrt(2) * (STATE_00 - STATE_01))

def test_hadamard_q2_state_10():
    '''
    Test the Hadamard operator acting on qubit 2 of state |10>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_10
    circuit.apply_gate(Hadamard(), 2)
    
    npt.assert_allclose(circuit.state, 1 / np.sqrt(2) * (STATE_10 + STATE_11))

def test_hadamard_q2_state_11():
    '''
    Test the Hadamard operator acting on qubit 2 of state |11>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_11
    circuit.apply_gate(Hadamard(), 2)
    
    npt.assert_allclose(circuit.state, 1 / np.sqrt(2) * (STATE_10 - STATE_11))

def test_s_q1_state_00():
    '''
    Test the S operator acting on qubit 1 of state |00>.
    '''
    circuit = QuantumCircuit()
    circuit.apply_gate(S(), 1)
    
    npt.assert_array_equal(circuit.state, STATE_00)

def test_s_q1_state_01():
    '''
    Test the S operator acting on qubit 1 of state |01>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_01
    circuit.apply_gate(S(), 1)
    
    npt.assert_array_equal(circuit.state, STATE_01)

def test_s_q1_state_10():
    '''
    Test the S operator acting on qubit 1 of state |10>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_10
    circuit.apply_gate(S(), 1)
    
    npt.assert_array_equal(circuit.state, 1j * STATE_10)

def test_s_q1_state_11():
    '''
    Test the S operator acting on qubit 1 of state |11>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_11
    circuit.apply_gate(S(), 1)
    
    npt.assert_array_equal(circuit.state, 1j * STATE_11)

def test_s_q2_state_00():
    '''
    Test the S operator acting on qubit 2 of state |00>.
    '''
    circuit = QuantumCircuit()
    circuit.apply_gate(S(), 2)
    
    npt.assert_array_equal(circuit.state, STATE_00)

def test_s_q2_state_01():
    '''
    Test the S operator acting on qubit 2 of state |01>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_01
    circuit.apply_gate(S(), 2)
    
    npt.assert_array_equal(circuit.state, 1j * STATE_01)

def test_s_q2_state_10():
    '''
    Test the S operator acting on qubit 2 of state |10>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_10
    circuit.apply_gate(S(), 2)
    
    npt.assert_array_equal(circuit.state, STATE_10)

def test_s_q2_state_11():
    '''
    Test the S operator acting on qubit 2 of state |11>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_11
    circuit.apply_gate(S(), 2)
    
    npt.assert_array_equal(circuit.state, 1j * STATE_11)

def test_t_q1_state_00():
    '''
    Test the T operator acting on qubit 1 of state |00>.
    '''
    circuit = QuantumCircuit()
    circuit.apply_gate(T(), 1)
    
    npt.assert_array_equal(circuit.state, STATE_00)

def test_t_q1_state_01():
    '''
    Test the T operator acting on qubit 1 of state |01>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_01
    circuit.apply_gate(T(), 1)
    
    npt.assert_array_equal(circuit.state, STATE_01)

def test_t_q1_state_10():
    '''
    Test the T operator acting on qubit 1 of state |10>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_10
    circuit.apply_gate(T(), 1)
    
    npt.assert_allclose(circuit.state, np.exp(1j * np.pi / 4) * STATE_10)

def test_t_q1_state_11():
    '''
    Test the T operator acting on qubit 1 of state |11>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_11
    circuit.apply_gate(T(), 1)
    
    npt.assert_allclose(circuit.state, np.exp(1j * np.pi / 4) * STATE_11)

def test_t_q2_state_00():
    '''
    Test the T operator acting on qubit 2 of state |00>.
    '''
    circuit = QuantumCircuit()
    circuit.apply_gate(T(), 2)
    
    npt.assert_array_equal(circuit.state, STATE_00)

def test_t_q2_state_01():
    '''
    Test the T operator acting on qubit 2 of state |01>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_01
    circuit.apply_gate(T(), 2)
    
    npt.assert_allclose(circuit.state, np.exp(1j * np.pi / 4) * STATE_01)

def test_t_q2_state_10():
    '''
    Test the T operator acting on qubit 2 of state |10>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_10
    circuit.apply_gate(T(), 2)
    
    npt.assert_array_equal(circuit.state, STATE_10)

def test_t_q2_state_11():
    '''
    Test the T operator acting on qubit 2 of state |11>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_11
    circuit.apply_gate(T(), 2)
    
    npt.assert_allclose(circuit.state, np.exp(1j * np.pi / 4) * STATE_11)

###########################
# CONTROLLED GATES
###########################

def test_cnot_c1_t2_state_00():
    '''
    Test the CNOT gate with control qubit 1, target qubit 2 on state |00>.
    '''
    circuit = QuantumCircuit()
    circuit.apply_gate(CNOT(), (1,2))

    npt.assert_array_equal(circuit.state, STATE_00)

def test_cnot_c1_t2_state_01():
    '''
    Test the CNOT gate with control qubit 1, target qubit 2 on state |01>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_01
    circuit.apply_gate(CNOT(), (1,2))

    npt.assert_array_equal(circuit.state, STATE_01)

def test_cnot_c1_t2_state_10():
    '''
    Test the CNOT gate with control qubit 1, target qubit 2 on state |10>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_10
    circuit.apply_gate(CNOT(), (1,2))

    npt.assert_array_equal(circuit.state, STATE_11)

def test_cnot_c1_t2_state_11():
    '''
    Test the CNOT gate with control qubit 1, target qubit 2 on state |11>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_11
    circuit.apply_gate(CNOT(), (1,2))

    npt.assert_array_equal(circuit.state, STATE_10)

def test_cnot_c2_t1_state_00():
    '''
    Test the CNOT gate with control qubit 2, target qubit 1 on state |00>.
    '''
    circuit = QuantumCircuit()
    circuit.apply_gate(CNOT(), (2,1))

    npt.assert_array_equal(circuit.state, STATE_00)

def test_cnot_c2_t1_state_01():
    '''
    Test the CNOT gate with control qubit 2, target qubit 1 on state |01>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_01
    circuit.apply_gate(CNOT(), (2,1))

    npt.assert_array_equal(circuit.state, STATE_11)

def test_cnot_c2_t1_state_10():
    '''
    Test the CNOT gate with control qubit 2, target qubit 1 on state |10>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_10
    circuit.apply_gate(CNOT(), (2,1))

    npt.assert_array_equal(circuit.state, STATE_10)

def test_cnot_c2_t1_state_11():
    '''
    Test the CNOT gate with control qubit 2, target qubit 1 on state |11>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_11
    circuit.apply_gate(CNOT(), (2,1))

    npt.assert_array_equal(circuit.state, STATE_01)

def test_cz_c1_t2_state_00():
    '''
    Test the CZ gate with control qubit 1, target qubit 2 on state |00>.
    '''
    circuit = QuantumCircuit()
    circuit.apply_gate(CZ(), (1,2))

    npt.assert_array_equal(circuit.state, STATE_00)

def test_cz_c1_t2_state_01():
    '''
    Test the CZ gate with control qubit 1, target qubit 2 on state |01>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_01
    circuit.apply_gate(CZ(), (1,2))

    npt.assert_array_equal(circuit.state, STATE_01)

def test_cz_c1_t2_state_10():
    '''
    Test the CZ gate with control qubit 1, target qubit 2 on state |10>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_10
    circuit.apply_gate(CZ(), (1,2))

    npt.assert_array_equal(circuit.state, STATE_10)

def test_cz_c1_t2_state_11():
    '''
    Test the CZ gate with control qubit 1, target qubit 2 on state |11>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_11
    circuit.apply_gate(CZ(), (1,2))

    npt.assert_array_equal(circuit.state, -STATE_11)

def test_cz_c2_t1_state_00():
    '''
    Test the CZ gate with control qubit 2, target qubit 1 on state |00>.
    '''
    circuit = QuantumCircuit()
    circuit.apply_gate(CZ(), (2,1))

    npt.assert_array_equal(circuit.state, STATE_00)

def test_cz_c2_t1_state_01():
    '''
    Test the CZ gate with control qubit 2, target qubit 1 on state |01>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_01
    circuit.apply_gate(CZ(), (2,1))

    npt.assert_array_equal(circuit.state, STATE_01)

def test_cz_c2_t1_state_10():
    '''
    Test the CZ gate with control qubit 2, target qubit 1 on state |10>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_10
    circuit.apply_gate(CZ(), (2,1))

    npt.assert_array_equal(circuit.state, STATE_10)

def test_cz_c2_t1_state_11():
    '''
    Test the CZ gate with control qubit 2, target qubit 1 on state |11>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_11
    circuit.apply_gate(CZ(), (2,1))

    npt.assert_array_equal(circuit.state, -STATE_11)    

###########################
# 2-QUBIT GATES
###########################

def test_swap_state_00():
    '''
    Test the SWAP gate on state |00>.
    '''
    circuit = QuantumCircuit()
    circuit.apply_gate(SWAP())

    npt.assert_array_equal(circuit.state, STATE_00)

def test_swap_state_01():
    '''
    Test the SWAP gate on state |01>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_01
    circuit.apply_gate(SWAP())

    npt.assert_array_equal(circuit.state, STATE_10)

def test_swap_state_10():
    '''
    Test the SWAP gate on state |10>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_10
    circuit.apply_gate(SWAP())

    npt.assert_array_equal(circuit.state, STATE_01)

def test_swap_state_11():
    '''
    Test the SWAP gate on state |11>.
    '''
    circuit = QuantumCircuit()
    circuit.state = STATE_11
    circuit.apply_gate(SWAP())

    npt.assert_array_equal(circuit.state, STATE_11)
