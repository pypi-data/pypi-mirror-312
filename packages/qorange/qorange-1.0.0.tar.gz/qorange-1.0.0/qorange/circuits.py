import numpy as np
from qorange.gates import Gate, TwoQubitGate, ControlledGate, MeasurementGate


class QuantumCircuit:
    """
    A simple object-oriented quantum circuit class.

    The `QuantumCircuit` class provides functionality to simulate quantum operations
    on a two-qubit system. It supports state updates, gate applications, partial trace calculations,
    qubit measurement, and circuit visualization.

    Attributes:
        state (numpy.ndarray): The state vector of the circuit initialized to |00⟩.
        density_matrix (numpy.ndarray): The density matrix representation of the circuit state.
        gate_history (list): A list of gates applied to the circuit, stored as dictionaries with details.
    """

    def __init__(self):
        """
        Initializes a quantum circuit.

        The circuit starts with two qubits in the |00⟩ state. The state vector
        and density matrix are initialized accordingly.

        Attributes:
            state (numpy.ndarray): The initial state vector of the circuit.
            density_matrix (numpy.ndarray): The density matrix of the initial state.
            gate_history (list): A history of all applied gates, including targets and controls.
        """

        self.state = np.kron(np.array([1, 0]), np.array([1, 0]))
        self.density_matrix = np.outer(self.state, self.state.conj())
        self.renduced_matrix_q1 = None
        self.reduced_matrix_q2 = None
        self._gates = []  # Stores the gates applied to the circuit
        self.gate_history = []  # Stores the gates applied to the circuit

    def update_state(self, new_state):
        """
        Updates the state vector and recalculates the density matrix.

        Args:
            new_state (numpy.ndarray): The new state vector.

        Raises:
            ValueError: If the provided state vector is invalid or non-normalized.
        """
        self.state = new_state
        self.density_matrix = np.outer(self.state, self.state.conj())

    def apply_gate(self, gate, q_index=None):
        """
        Applies a quantum gate to the circuit's state vector.

        Args:
            gate (Gate or ControlledGate): The quantum gate to apply.
            q_index (int or tuple): Target qubit index for single qubit gates (1 or 2)
                or a tuple (control_qubit, target_qubit) for controlled gates.

        Raises:
            Exception: If the gate is invalid or if the qubit indices are incorrect.
        """
        if isinstance(gate, Gate):
            gate_info = {"gate": gate, "control": None}
            if isinstance(gate, TwoQubitGate):
                # q_index is not necessary here.
                gate_matrix = gate.matrix
                gate_info["target"] = None
            else:
                if isinstance(q_index, int):
                    gate_info["target"] = q_index
                    if q_index == 1:
                        gate_matrix = np.kron(gate.matrix, np.eye(2))
                    elif q_index == 2:
                        gate_matrix = np.kron(np.eye(2), gate.matrix)
                    else:
                        raise Exception("Invalid indexing of qubits")
                else:
                    raise Exception(
                        "Invalid q-index data type for single qubit gate, use int")

            self.update_state(np.matmul(gate_matrix, self.state))
            self.gate_history.append(gate_info)

        elif isinstance(gate, ControlledGate):
            if isinstance(q_index, tuple):
                if q_index == (1, 2):
                    # control is on the first qubit
                    gate_matrix = np.kron(np.array([[1, 0], [0, 0]]), np.eye(
                        2)) + np.kron(np.array([[0, 0], [0, 1]]), gate.get_matrix())
                elif q_index == (2, 1):
                    # control is on the second qubit
                    gate_matrix = np.kron(np.eye(2), np.array(
                        [[1, 0], [0, 0]])) + np.kron(gate.get_matrix(), np.array([[0, 0], [0, 1]]))
                else:
                    raise Exception("Invalid indexing of qubits")

                self.update_state(np.matmul(gate_matrix, self.state))
                self.gate_history.append({
                    "gate": gate,
                    "target": q_index[1],
                    "control": q_index[0],
                })
            else:
                raise Exception(
                    "Invalid q-index data type for controlled gates, use tuple")

        else:
            raise Exception(
                "Specified gate is invalid, use Gate or ControlledGate class")

    def partial_trace(self, dims=[2, 2], keep=None):
        """
        Calculates the partial trace of the circuit's density matrix.

        Args:
            dims (list): Dimensions of the subsystems (default is [2, 2]).
            keep (int): Specifies which subsystem to keep (1 for qubit 1, 2 for qubit 2).

        Returns:
            numpy.ndarray: The reduced density matrix of the specified qubit.

        Raises:
            Exception: If the keep parameter is invalid.
        """
        dim1, dim2 = dims
        rho = self.density_matrix
        # Reshape the density matrix (axis 0 and 1 are for qubit 1, and axis 2 and 3 are for qubit 2)
        rho_reshaped = rho.reshape(dim1, dim2, dim1, dim2)

        if keep == 1:
            # Compute reduced density matrix for qubit 1
            rho_1 = np.trace(rho_reshaped, axis1=1, axis2=3)  # Sum over qubit 2
            #rho_1 /= np.trace(rho_1)  # Normalize the reduced density matrix
            return rho_1

        elif keep == 2:
            # Compute reduced density matrix for qubit 2
            rho_2 = np.trace(rho_reshaped, axis1=0, axis2=2)  # Sum over qubit 1
            #rho_2 /= np.trace(rho_2)  # Normalize the reduced density matrix
            return rho_2

        else:
            raise Exception(
                "Invalid value for keep parameter. Use 1 to keep qubit 1, and 2 to keep qubit 2")

    def measure_qubit_computational(self, qubit_to_measure):
        """
        Measures a single qubit in the computational basis (|0⟩ and |1⟩).

        This method calculates the probabilities of the given qubit being in the
        |0⟩ or |1⟩ state by performing a partial trace over the other qubit's state.
        The result is returned as a probability distribution.

        Args:
            qubit_to_measure (int): The index of the qubit to measure (1 or 2).

        Returns:
            numpy.ndarray: A 1D array with two elements:
                - The first element represents the probability of the qubit being in state |0⟩.
                - The second element represents the probability of the qubit being in state |1⟩.

        Raises:
            Exception: If the provided qubit index is not 1 or 2.

        Example:
            If the circuit is in a state where the first qubit has an equal superposition:
            .. code-block:: python

                probabilities = circuit.measure_qubit_computational(1)
                print(probabilities)  # Output: [0.5, 0.5]
        """
        gate_info = { 
            "gate": MeasurementGate(), 
            "target": qubit_to_measure,
            "control": None,
        }

        if qubit_to_measure == 1:
            rho_1 = self.partial_trace(keep=1)
            p0 = np.trace(rho_1 @ np.array([[1, 0],
                                            [0, 0]]))  # Probability of measuring 0 p_0 = Tr(|0><0| * rho)
            p1 = np.trace(rho_1 @ np.array([[0, 0],
                                           [0, 1]]))  # Probability of measuring 1 p_1 = Tr(|1><1| * rho)
            outcome = np.array([p0, p1])
            self.gate_history.append(gate_info)
            return np.real(outcome)

        elif qubit_to_measure == 2:
            rho_2 = self.partial_trace(keep=2)
            p0 = np.trace(rho_2 @ np.array([[1, 0],
                                            [0, 0]]))
            p1 = np.trace(rho_2 @ np.array([[0, 0],
                                           [0, 1]]))
            outcome = np.array([p0, p1])
            self.gate_history.append(gate_info)
            return np.real(outcome)

        else:
            raise Exception(
                "Invalid value for qubit_to_measure parameter. Use 1 for qubit 1 and 2 for qubit 2")

    def draw(self):
        """
        Draws an ASCII representation of the quantum circuit.

        The method generates a visual representation of the quantum circuit,
        illustrating the sequence of gates applied to each qubit and the connections
        between qubits for controlled gates. The diagram aligns all gates and ensures
        proper spacing for clarity.

        Example:
            Consider a circuit with a Hadamard gate on qubit 1 and a CNOT gate
            with qubit 1 as control and qubit 2 as target. The output would look like:

            .. code-block:: text

                Qubit 1: ───H───●────
                                │
                Qubit 2: ───────X────

        Details:
            - Single-qubit gates are represented with their symbols (e.g., H, X, RZ).
            - Controlled gates display the control qubit as "●" and the target qubit
              with the corresponding gate symbol (e.g., X, Z).

        Raises:
            ValueError: If the gate history contains invalid data or is improperly formatted.

        """

        EMPTY_SEGMENT = [
            "           ",
            "───────────",
            "           ",
        ]

        diagram = [
            [],  # Qubit 1 line
            [],  # Qubit 2 line
        ]

        for gate_info in self.gate_history:
            control_qubit = gate_info["control"]
            target_qubit = gate_info["target"]

            if not target_qubit:
                # If there's no target qubit then apply the gate to both qubits.
                # Easiest way to do this is to arbitrarily assign the qubits as control and target. 
                # It's not pretty but it works :')
                control_qubit = 1
                target_qubit = 2

            if control_qubit:
                num_gates_control = len(diagram[control_qubit - 1])
                num_gates_target = len(diagram[target_qubit - 1])
                if (num_gates_control > num_gates_target):
                    # Add some padding to the target line to make sure everything aligns
                    diagram[target_qubit - 1].extend(
                        [EMPTY_SEGMENT for i in range(
                            num_gates_control - num_gates_target)]
                    )
                elif (num_gates_control < num_gates_target):
                    # Add some padding to the control line to make sure everything aligns
                    diagram[control_qubit - 1].extend(
                        [EMPTY_SEGMENT for i in range(
                            num_gates_target - num_gates_control)]
                    )
                diagram[control_qubit - 1].append(
                    gate_info["gate"].draw(control_qubit, is_target=False)
                )

            diagram[target_qubit - 1].append(
                gate_info["gate"].draw(target_qubit, is_target=True)
            )

        if len(diagram[0]) < len(diagram[1]):
            # Pad the end of qubit line 1 to match the length of qubit line 2
            diagram[0].extend([EMPTY_SEGMENT for i in range(
                len(diagram[1]) - len(diagram[0]))])
        elif len(diagram[0]) > len(diagram[1]):
            # Pad the end of qubit line 2 to match the length of qubit line 1
            diagram[1].extend([EMPTY_SEGMENT for i in range(
                len(diagram[0]) - len(diagram[1]))])

        for qubit_line_n in range(2):
            for printed_line_m in range(3):
                line = "".join([
                    printed_lines[printed_line_m] for printed_lines in diagram[qubit_line_n]
                ])
                print(line)
