import numpy as np


class Gate:
    """
    A base class for quantum gates, ensuring that the matrix representation
    of the gate is unitary.

    Quantum gates are represented by unitary matrices, which preserve the norm
    of quantum states during transformations. This class provides a foundation
    for creating specific quantum gates.

    Attributes:
        matrix (numpy.ndarray): The unitary matrix representing the quantum gate.
        span (int): The dimension of the quantum gate, default is 2 (for qubits).

    Methods:
        __init__(matrix, span=2): Initializes the gate with the given unitary matrix.
        __repr__(): Returns a string representation of the gate.
    """

    def __init__(self, matrix, span=2):
        """
        Initializes the quantum gate with the given matrix.
        Ensures that the matrix is unitary and of the correct dimension.

        Args:
            matrix (numpy.ndarray): The matrix representation of the quantum gate.
            span (int, optional): The dimension of the quantum gate. Defaults to 2.

        Raises:
            TypeError: If the provided matrix is not a numpy array.
            ValueError: If the matrix is not square or not unitary.
        """
        if not isinstance(matrix, np.ndarray):
            raise TypeError("Matrix must be a numpy array.")
        if np.shape(matrix) != (span, span):
            raise ValueError(
                f"Matrix must be square with dimensions ({span}, {span}).")

        # Check unitarity: U†U = I
        if not np.allclose(np.eye(matrix.shape[0]), np.dot(matrix, matrix.conj().T)):
            raise ValueError("Matrix is not unitary!")

        self.matrix = matrix
        self.span = span

    def __repr__(self):
        """
        Returns a string representation of the Gate object, including its matrix.

        Returns:
            str: A string representation of the quantum gate.
        """
        return f"Gate(matrix={self.matrix}, span={self.span})"


class Identity(Gate):
    """
    Represents the Identity quantum gate (I), which leaves the quantum state unchanged.

    The Identity gate has the matrix representation:

    .. math::
        I = \\begin{bmatrix}
            1 & 0 \\\\
            0 & 1
        \\end{bmatrix}
    """

    def __init__(self):
        """
        Initializes the Identity gate.

        This constructor sets up the matrix representation of the Identity gate:

        .. math::
            \\text{Matrix: } \\begin{bmatrix}
                1 & 0 \\\\
                0 & 1
            \\end{bmatrix}

        Inherits from:
            Gate: A base class for quantum gates.
        """
        Gate.__init__(self, np.array([[1, 0],
                                      [0, 1]]))

    def draw(self, *args, **kwargs):
        """
        Returns the ASCII representation of the Identity gate.

        Example:
            Drawing the Identity gate:


       .. code-block:: text

                   ┌───┐   
                ───│ I │─── == ---------
                   └───┘   
        """
        return [
            "   ┌───┐   ",
            "───│ I │───",
            "   └───┘   ",
        ]


class PauliX(Gate):
    """
    Represents the Pauli-X quantum gate, also known as the NOT gate.

    The Pauli-X gate flips the state of a qubit:

    .. math::
        \\vert 0\\rangle \\leftrightarrow \\vert 1\\rangle

    The Pauli-X gate has the matrix representation:

    .. math::
        X = \\begin{bmatrix}
            0 & 1 \\\\
            1 & 0
        \\end{bmatrix}
    """

    def __init__(self):
        """
        Initializes the Pauli-X gate.

        This constructor sets up the matrix representation of the Pauli-X gate:

        .. math::
            \\text{Matrix: } \\begin{bmatrix}
                0 & 1 \\\\
                1 & 0
            \\end{bmatrix}

        Inherits from:
            Gate: A base class for quantum gates.
        """
        Gate.__init__(self, np.array([[0, 1],
                                      [1, 0]]))

    def draw(self, *args, **kwargs):
        """
        Returns the ASCII representation of the Pauli-X gate.

        Example:
            Drawing the Pauli-X gate:

            .. code-block:: text

                   ┌───┐   
                ───│ X │───
                   └───┘   
        """
        return [
            "   ┌───┐   ",
            "───│ X │───",
            "   └───┘   ",
        ]


class PauliY(Gate):
    """
    Represents the Pauli-Y quantum gate.

    The Pauli-Y gate applies a 180° rotation around the Y-axis on the Bloch sphere.

    The Pauli-Y gate has the matrix representation:

    .. math::
        Y = \\begin{bmatrix}
            0 & -i \\\\
            i & 0
        \\end{bmatrix}
    """

    def __init__(self):
        """
        Initializes the Pauli-Y gate.

        This constructor sets up the matrix representation of the Pauli-Y gate:

        .. math::
            \\text{Matrix: } \\begin{bmatrix}
                0 & -i \\\\
                i & 0
            \\end{bmatrix}

        Inherits from:
            Gate: A base class for quantum gates.
        """
        Gate.__init__(self, np.array([[0, -1j],
                                      [1j, 0]]))

    def draw(self, *args, **kwargs):
        """
        Returns the ASCII representation of the Pauli-Y gate.

        Example:
            Drawing the Pauli-Y gate:

            .. code-block:: text

                   ┌───┐   
                ───│ Y │───
                   └───┘   
        """
        return [
            "   ┌───┐   ",
            "───│ Y │───",
            "   └───┘   ",
        ]


class PauliZ(Gate):
    """
    Represents the Pauli-Z quantum gate.

    The Pauli-Z gate applies a 180° rotation around the Z-axis on the Bloch sphere.

    The Pauli-Z gate has the matrix representation:

    .. math::
        Z = \\begin{bmatrix}
            1 & 0 \\\\
            0 & -1
        \\end{bmatrix}
    """

    def __init__(self):
        """
        Initializes the Pauli-Z gate.

        This constructor sets up the matrix representation of the Pauli-Z gate:

        .. math::
            \\text{Matrix: } \\begin{bmatrix}
                1 & 0 \\\\
                0 & -1
            \\end{bmatrix}

        Inherits from:
            Gate: A base class for quantum gates.
        """
        Gate.__init__(self, np.array([[1, 0],
                                      [0, -1]]))

    def draw(self, *args, **kwargs):
        """
        Returns the ASCII representation of the Pauli-Z gate.

        Example:
            Drawing the Pauli-Z gate:

            .. code-block:: text

                   ┌───┐   
                ───│ Z │───
                   └───┘   
        """
        return [
            "   ┌───┐   ",
            "───│ Z │───",
            "   └───┘   ",
        ]


class Hadamard(Gate):
    """
    Represents the Hadamard quantum gate (H).

    The Hadamard gate creates superpositions by transforming quantum states as follows:

    .. math::
        \\vert 0\\rangle \\to \\frac{\\vert 0\\rangle + \\vert 1\\rangle}{\\sqrt{2}}, \\quad
        \\vert 1\\rangle \\to \\frac{\\vert 0\\rangle - \\vert 1\\rangle}{\\sqrt{2}}

    The Hadamard gate has the matrix representation:

    .. math::
        H = \\frac{1}{\\sqrt{2}} \\begin{bmatrix}
            1 & 1 \\\\
            1 & -1
        \\end{bmatrix}
    """

    def __init__(self):
        """
        Initializes the Hadamard gate.

        This constructor sets up the matrix representation of the Hadamard gate:

        .. math::
            \\text{Matrix: } \\frac{1}{\\sqrt{2}} \\begin{bmatrix}
                1 & 1 \\\\
                1 & -1
            \\end{bmatrix}

        Inherits from:
            Gate: A base class for quantum gates.
        """
        Gate.__init__(self, np.array([[1, 1],
                                      [1, -1]]) / np.sqrt(2))

    def draw(self, *args, **kwargs):
        """
        Returns the ASCII representation of the Hadamard gate.

        Example:
            Drawing the Hadamard gate:

            .. code-block:: text

                   ┌───┐   
                ───│ H │───
                   └───┘   
        """
        return [
            "   ┌───┐   ",
            "───│ H │───",
            "   └───┘   ",
        ]


class S(Gate):
    """
    Represents the S gate (phase gate).

    The S gate applies a 90° phase shift to the \\vert 1\\rangle state.

    The S gate has the matrix representation:

    .. math::
        S = \\begin{bmatrix}
            1 & 0 \\\\
            0 & i
        \\end{bmatrix}
    """

    def __init__(self):
        """
        Initializes the S gate.

        This constructor sets up the matrix representation of the S gate:

        .. math::
            \\text{Matrix: } \\begin{bmatrix}
                1 & 0 \\\\
                0 & i
            \\end{bmatrix}

        Inherits from:
            Gate: A base class for quantum gates.
        """
        Gate.__init__(self, np.array([[1, 0],
                                      [0, 1j]]))

    def draw(self, *args, **kwargs):
        """
        Returns the ASCII representation of the S gate.

        Example:
            Drawing the S gate:

            .. code-block:: text

                   ┌───┐   
                ───│ S │───
                   └───┘   
        """
        return [
            "   ┌───┐   ",
            "───│ S │───",
            "   └───┘   ",
        ]


class T(Gate):
    """
    Represents the T gate (π/8 gate).

    The T gate applies a π/4 phase shift to the \\vert 1\\rangle state.

    The T gate has the matrix representation:

    .. math::
        T = \\begin{bmatrix}
            1 & 0 \\\\
            0 & e^{i\\pi/4}
        \\end{bmatrix}

    where:

    .. math::
        e^{i\\pi/4} = \\frac{1}{\\sqrt{2}} + i\\frac{1}{\\sqrt{2}}
    """

    def __init__(self):
        """
        Initializes the T gate.

        This constructor sets up the matrix representation of the T gate:

        .. math::
            \\text{Matrix: } \\begin{bmatrix}
                1 & 0 \\\\
                0 & \\frac{1}{\\sqrt{2}} + i\\frac{1}{\\sqrt{2}}
            \\end{bmatrix}

        Inherits from:
            Gate: A base class for quantum gates.
        """
        Gate.__init__(self, np.array([[1, 0],
                                      [0, 1/np.sqrt(2) + 1j/np.sqrt(2)]]))

    def draw(self, *args, **kwargs):
        """
        Returns the ASCII representation of the T gate.

        Example:
            Drawing the T gate:

            .. code-block:: text

                   ┌───┐   
                ───│ T │───
                   └───┘   
        """
        return [
            "   ┌───┐   ",
            "───│ T │───",
            "   └───┘   ",
        ]


class PhaseGate(Gate):
    """
    Represents the phase gate.

    The phase gate is a single-qubit gate that applies a phase shift of \\( \\phi \\)
    to the \\( \\vert 1 \\rangle \\) state while leaving the \\( \\vert 0 \\rangle \\)
    state unchanged. It is commonly used for phase adjustments in quantum circuits.

    The matrix representation of the phase gate is:

    .. math::
        P(\\phi) = \\begin{bmatrix}
            1 & 0 \\\\
            0 & e^{i\\phi}
        \\end{bmatrix}
    """

    def __init__(self, phi):
        """
        Initializes the phase gate.

        This constructor sets up the matrix representation of the phase gate for a
        given phase shift \\( \\phi \\):

        .. math::
            P(\\phi) = \\begin{bmatrix}
                1 & 0 \\\\
                0 & e^{i\\phi}
            \\end{bmatrix}

        Args:
            phi (float): The phase shift in radians.
        """
        Gate.__init__(self, np.array([
            [1, 0],
            [0, np.exp(1j * phi)]
        ]))

    def draw(self, *args, **kwargs):
        """
        Returns the ASCII representation of the phase gate.

        Example:
            .. code-block:: text

                   ┌───┐
                ───│ P │───
                   └───┘

        Args:
            *args: Additional positional arguments (not used).
            **kwargs: Additional keyword arguments (not used).

        Returns:
            list: A list of strings representing the ASCII art of the phase gate.
        """
        return [
            "   ┌───┐   ",
            "───│ P │───",
            "   └───┘   ",
        ]


class RotationXGate(Gate):
    """
    Represents the Rotation-X (RX) gate.

    The RX gate is a single-qubit gate that applies a rotation around the X-axis of the Bloch sphere
    by an angle \\( \\theta \\). It is commonly used for implementing arbitrary single-qubit rotations.

    The matrix representation of the RX gate is:

    .. math::
        RX(\\theta) = \\begin{bmatrix}
            \\cos(\\theta / 2) & -i \\sin(\\theta / 2) \\\\
            -i \\sin(\\theta / 2) & \\cos(\\theta / 2)
        \\end{bmatrix}
    """

    def __init__(self, theta):
        """
        Initializes the RX gate.

        This constructor sets up the matrix representation of the RX gate for a given angle \\( \\theta \\):

        .. math::
            RX(\\theta) = \\begin{bmatrix}
                \\cos(\\theta / 2) & -i \\sin(\\theta / 2) \\\\
                -i \\sin(\\theta / 2) & \\cos(\\theta / 2)
            \\end{bmatrix}

        Args:
            theta (float): The rotation angle in radians.
        """
        Gate.__init__(self, np.array([
            [np.cos(theta / 2), -1j * np.sin(theta / 2)],
            [-1j * np.sin(theta / 2), np.cos(theta / 2)]
        ]))

    def draw(self, *args, **kwargs):
        """
        Returns the ASCII representation of the RX gate.

        Example:
            .. code-block:: text

                   ┌────┐
                 ──│ RX │──
                   └────┘

        Args:
            *args: Additional positional arguments (not used).
            **kwargs: Additional keyword arguments (not used).

        Returns:
            list: A list of strings representing the ASCII art of the RX gate.
        """
        return [
            "  ┌────┐  ",
            "──│ RX │──",
            "  └────┘  ",
        ]


class RotationYGate(Gate):
    """
    Represents the Rotation-Y (RY) gate.

    The RY gate is a single-qubit gate that applies a rotation around the Y-axis of the Bloch sphere
    by an angle \\( \\theta \\). It is commonly used for implementing arbitrary single-qubit rotations.

    The matrix representation of the RY gate is:

    .. math::
        RY(\\theta) = \\begin{bmatrix}
            \\cos(\\theta / 2) & -\\sin(\\theta / 2) \\\\
            \\sin(\\theta / 2) & \\cos(\\theta / 2)
        \\end{bmatrix}
    """

    def __init__(self, theta):
        """
        Initializes the RY gate.

        This constructor sets up the matrix representation of the RY gate for a given angle \\( \\theta \\):

        .. math::
            RY(\\theta) = \\begin{bmatrix}
                \\cos(\\theta / 2) & -\\sin(\\theta / 2) \\\\
                \\sin(\\theta / 2) & \\cos(\\theta / 2)
            \\end{bmatrix}

        Args:
            theta (float): The rotation angle in radians.
        """
        Gate.__init__(self, np.array([
            [np.cos(theta / 2), -np.sin(theta / 2)],
            [np.sin(theta / 2), np.cos(theta / 2)]
        ]))

    def draw(self, *args, **kwargs):
        """
        Returns the ASCII representation of the RY gate.

        Example:
            .. code-block:: text

                   ┌────┐
                 ──│ RY │──
                   └────┘

        Args:
            *args: Additional positional arguments (not used).
            **kwargs: Additional keyword arguments (not used).

        Returns:
            list: A list of strings representing the ASCII art of the RY gate.
        """
        return [
            "  ┌────┐  ",
            "──│ RY │──",
            "  └────┘  ",
        ]


class RotationZGate(Gate):
    """
    Represents the Rotation-Z (RZ) gate.

    The RZ gate is a single-qubit gate that applies a rotation around the Z-axis of the Bloch sphere
    by an angle \\( \\theta \\). It is commonly used for phase adjustments and is a key component
    in building universal quantum gates.

    The matrix representation of the RZ gate is:

    .. math::
        RZ(\\theta) = \\begin{bmatrix}
            e^{-i\\theta / 2} & 0 \\\\
            0 & e^{i\\theta / 2}
        \\end{bmatrix}
    """

    def __init__(self, theta):
        """
        Initializes the RZ gate.

        This constructor sets up the matrix representation of the RZ gate for a given angle \\( \\theta \\):

        .. math::
            RZ(\\theta) = \\begin{bmatrix}
                e^{-i\\theta / 2} & 0 \\\\
                0 & e^{i\\theta / 2}
            \\end{bmatrix}

        Args:
            theta (float): The rotation angle in radians.
        """
        Gate.__init__(self, np.array([
            [np.exp(-1j * theta / 2), 0],
            [0, np.exp(1j * theta / 2)]
        ]))

    def draw(self, *args, **kwargs):
        """
        Returns the ASCII representation of the RZ gate.

        Example:
            .. code-block:: text

                   ┌────┐
                 ──│ RZ │──
                   └────┘

        Args:
            *args: Additional positional arguments (not used).
            **kwargs: Additional keyword arguments (not used).

        Returns:
            list: A list of strings representing the ASCII art of the RZ gate.
        """
        return [
            "  ┌────┐  ",
            "──│ RZ │──",
            "  └────┘  ",
        ]


class ArbSingleQubitGate(Gate):
    """
    Represents an arbitrary single-qubit quantum gate.

    The `ArbSingleQubitGate` class allows for the creation of single-qubit gates with
    user-defined unitary matrix representations. This provides flexibility for custom
    quantum gate designs.

    Attributes:
        matrix (numpy.ndarray): The unitary matrix representing the arbitrary single-qubit gate.

    Methods:
        __init__(matrix): Initializes the gate with the provided matrix representation.
        draw(*args, **kwargs): Returns the ASCII representation of the gate.
    """

    def __init__(self, matrix):
        """
        Initializes the arbitrary single-qubit gate.

        Args:
            matrix (numpy.ndarray): A 2x2 unitary matrix representing the single-qubit gate.

        Raises:
            TypeError: If the provided matrix is not a numpy array.
            ValueError: If the matrix is not 2x2 or not unitary.
        """
        super().__init__(matrix)

    def draw(self, *args, **kwargs):
        """
        Returns the ASCII representation of the arbitrary single-qubit gate.

        Example:
            .. code-block:: text

                   ┌───┐
                ───│ U │───
                   └───┘

        Args:
            *args: Additional positional arguments (not used).
            **kwargs: Additional keyword arguments (not used).

        Returns:
            list: A list of strings representing the ASCII art of the gate.
        """
        return [
            "   ┌───┐   ",
            "───│ U │───",
            "   └───┘   ",
        ]


class MeasurementGate(Gate):
    """
    Represents the Measurement gate (M). This gate is only used for circuit drawing.
    """

    def __init__(self):
        """
        Initializes the Measurement gate.

        Inherits from:
            Gate: A base class for quantum gates.
        """
        Gate.__init__(self, np.array([[1, 0],
                                      [0, 1]])) # Initialise to any matrix: we're not using this

    def draw(self, *args, **kwargs):
        """
        Returns the ASCII representation of the Measurement gate.
        """
        return [
            "   ┌───┐   ",
            "───│ M │───",
            "   └───┘   ",
        ]


class ControlledGate():
    """
    Represents a controlled quantum gate.

    A controlled gate applies a specified quantum gate (`gate`) conditionally,
    based on the state of a control qubit. The `ControlledGate` class wraps around
    a `Gate` object to provide its controlled version.

    Attributes:
        gate (Gate): The quantum gate to be controlled.

    Methods:
        __init__(gate): Initializes the controlled gate with the specified quantum gate.
        get_matrix(): Returns the matrix representation of the controlled quantum gate.
    """

    def __init__(self, gate):
        """
        Initializes the controlled quantum gate.

        Args:
            gate (Gate): An instance of the `Gate` class representing the target gate.

        Raises:
            TypeError: If the provided `gate` is not an instance of the `Gate` class.
        """
        if isinstance(gate, Gate):
            self.gate = gate
        else:
            raise TypeError(
                "Specified gate object is invalid. It must be an instance of the Gate class.")

    def get_matrix(self):
        """
        Returns the matrix representation of the controlled quantum gate.

        The controlled gate matrix is determined by the target gate matrix and typically
        expands the gate's dimensionality to include the control qubit.

        Returns:
            numpy.ndarray: The matrix representation of the controlled gate.
        """
        # Expand the gate to include control logic (this implementation is minimal for now).
        return self.gate.matrix


class CNOT(ControlledGate):
    """
    Represents the Controlled-NOT (CNOT) gate.

    The CNOT gate is a two-qubit gate that flips the target qubit if the control qubit
    is in the \\vert 1\\rangle state. It is a fundamental gate in quantum computing,
    often used to create entanglement.

    The matrix representation of the CNOT gate is:

    .. math::
        \\text{CNOT} = \\begin{bmatrix}
            1 & 0 & 0 & 0 \\\\
            0 & 1 & 0 & 0 \\\\
            0 & 0 & 0 & 1 \\\\
            0 & 0 & 1 & 0
        \\end{bmatrix}

    Attributes:
        gate (Gate): The underlying quantum gate being controlled (Pauli-X in this case).

    Methods:
        __init__(): Initializes the CNOT gate.
        draw(qubit_number, is_target=False): Returns the ASCII representation of the CNOT gate.
    """

    def __init__(self):
        """
        Initializes the CNOT gate.

        The CNOT gate is implemented as a ControlledGate with a Pauli-X gate
        acting as the controlled operation.
        """
        super().__init__(PauliX())

    def draw(self, qubit_number, is_target=False):
        """
        Returns the ASCII representation of the CNOT gate for a specific qubit.

        The CNOT gate has a visual distinction for control (●) and target (○) qubits.

        Args:
            qubit_number (int): The qubit's position in the circuit (1 for control, 2 for target).
            is_target (bool, optional): Whether the qubit is the target qubit. Defaults to False.

        Returns:
            list: A list of strings representing the ASCII art for the CNOT gate.


        Control qubit (●):
            .. code-block:: text

                         │     
                    ─────●─────

        Target qubit (○):
            .. code-block:: text

                    ─────○─────
                         │     
            """
        symbol = "○" if is_target else "●"
        if qubit_number == 1:
            return [
                "           ",
                f"─────{symbol}─────",
                "     │     ",
            ]
        else:
            return [
                "     │     ",
                f"─────{symbol}─────",
                "           ",
            ]


class CZ(ControlledGate):
    """
    Represents the Controlled-Z (CZ) gate.

    The CZ gate is a two-qubit gate that applies a Z gate to the target qubit
    if the control qubit is in the \\vert 1\\rangle state. It is often used in
    quantum circuits for conditional phase flips.

    The matrix representation of the CZ gate is:

    .. math::
        \\text{CZ} = \\begin{bmatrix}
            1 & 0 & 0 & 0 \\\\
            0 & 1 & 0 & 0 \\\\
            0 & 0 & 1 & 0 \\\\
            0 & 0 & 0 & -1
        \\end{bmatrix}

    Attributes:
        gate (Gate): The underlying quantum gate being controlled (Pauli-Z in this case).

    Methods:
        __init__(): Initializes the CZ gate.
        draw(qubit_number, is_target=False): Returns the ASCII representation of the CZ gate.
    """

    def __init__(self):
        """
        Initializes the CZ gate.

        The CZ gate is implemented as a ControlledGate with a Pauli-Z gate
        acting as the controlled operation.
        """
        super().__init__(PauliZ())

    def draw(self, qubit_number, is_target=False):
        """
        Returns the ASCII representation of the CZ gate for a specific qubit.

        The CZ gate distinguishes between control (●) and target qubits, where
        the target qubit displays the Z gate symbol.

        Args:
            qubit_number (int): The qubit's position in the circuit (1 for control, 2 for target).
            is_target (bool, optional): Whether the qubit is the target qubit. Defaults to False.

        Returns:
            list: A list of strings representing the ASCII art for the CZ gate.

        Control qubit (●):
            .. code-block:: text

                         │     
                    ─────●─────

        Target qubit (Z):
            .. code-block:: text

                       ┌───┐   
                    ───│ Z │───
                       └───┘   
        """
        if is_target:
            return [
                "   ┌───┐   ",
                "───│ Z │───",
                "   └───┘   ",
            ]
        else:
            if qubit_number == 1:
                return [
                    "           ",
                    "─────●─────",
                    "     │     ",
                ]
            else:
                return [
                    "     │     ",
                    "─────●─────",
                    "           ",
                ]


class CPhase(ControlledGate):
    """
    Represents the Controlled-Phase (CPhase) gate.

    The Controlled-Phase gate applies a phase shift of \\( \\phi \\) to the target qubit
    when the control qubit is in the \\( \\vert 1 \\rangle \\) state. It is an extension
    of the PhaseGate to two-qubit systems.

    Attributes:
        gate (PhaseGate): The phase gate applied as the controlled operation.

    Methods:
        __init__(phi): Initializes the CPhase gate with a given phase shift \\( \\phi \\).
        draw(qubit_number, is_target=False): Returns the ASCII representation of the CPhase gate.
    """

    def __init__(self, phi):
        """
        Initializes the Controlled-Phase (CPhase) gate.

        This constructor creates a ControlledGate with a PhaseGate as the target gate.

        Args:
            phi (float): The phase shift in radians.

        Example:
            To create a Controlled-Phase gate with a phase shift of \\( \\pi/2 \\):

            .. code-block:: python

                cphase_gate = CPhase(np.pi / 2)
        """
        super().__init__(PhaseGate(phi))

    def draw(self, qubit_number, is_target=False):
        """
        Returns the ASCII representation of the Controlled-Phase (CPhase) gate.

        The CPhase gate uses a dot (●) to represent the control qubit and a "P" symbol
        for the target qubit to indicate the phase shift.

        Args:
            qubit_number (int): The qubit's position in the circuit (1 for control, 2 for target).
            is_target (bool, optional): Whether the qubit is the target qubit. Defaults to False.

        Returns:
            list: A list of strings representing the ASCII art for the CPhase gate.

        Example:
            Control qubit (●):
            .. code-block:: text

                 │     
            ─────●─────

            Target qubit (P):
            .. code-block:: text

               ┌───┐   
            ───│ P │───
               └───┘   
        """
        if is_target:
            return [
                "   ┌───┐   ",
                "───│ P │───",
                "   └───┘   ",
            ]
        else:
            if qubit_number == 1:
                return [
                    "           ",
                    "─────●─────",
                    "     │     ",
                ]
            else:
                return [
                    "     │     ",
                    "─────●─────",
                    "           ",
                ]


class ArbControlledGate(ControlledGate):

    def __init__(self, gate):
        super().__init__(gate)

    def draw(self, qubit_number, is_target=False):
        if is_target:
            return [
                "   ┌───┐   ",
                "───│ A │───",
                "   └───┘   ",
            ]
        else:
            if qubit_number == 1:
                return [
                    "           ",
                    "─────●─────",
                    "     │     ",
                ]
            else:
                return [
                    "     │     ",
                    "─────●─────",
                    "           ",
                ]


class TwoQubitGate(Gate):
    """
    Represents a two-qubit quantum gate.

    The `TwoQubitGate` class is a specialized subclass of `Gate` designed to handle
    quantum gates that operate on two qubits. These gates have a 4x4 matrix representation.

    Attributes:
        matrix (numpy.ndarray): The 4x4 unitary matrix representing the two-qubit gate.

    Methods:
        __init__(matrix): Initializes the two-qubit gate with the given unitary matrix.
    """

    def __init__(self, matrix):
        """
        Initializes a two-qubit gate.

        Ensures that the provided matrix is 4x4 and unitary.

        Args:
            matrix (numpy.ndarray): The 4x4 matrix representation of the two-qubit gate.

        Raises:
            TypeError: If the provided matrix is not a numpy array.
            ValueError: If the matrix is not 4x4 or not unitary.
        """
        super().__init__(matrix, span=4)


class SWAP(TwoQubitGate):
    """
    Represents the SWAP gate.

    The SWAP gate is a two-qubit gate that exchanges the states of two qubits. 
    It is commonly used in quantum circuits for rearranging qubit states.

    The matrix representation of the SWAP gate is:

    .. math::
        \\text{SWAP} = \\begin{bmatrix}
            1 & 0 & 0 & 0 \\\\
            0 & 0 & 1 & 0 \\\\
            0 & 1 & 0 & 0 \\\\
            0 & 0 & 0 & 1
        \\end{bmatrix}
    """

    def __init__(self):
        """
        Initializes the SWAP gate.

        This constructor sets up the matrix representation of the SWAP gate:

        .. math::
            \\text{SWAP} = \\begin{bmatrix}
                1 & 0 & 0 & 0 \\\\
                0 & 0 & 1 & 0 \\\\
                0 & 1 & 0 & 0 \\\\
                0 & 0 & 0 & 1
            \\end{bmatrix}

        Inherits from:
            TwoQubitGate: A specialized gate class for two-qubit operations.
        """
        super().__init__(np.array([
            [1, 0, 0, 0],  # |00⟩ → |00⟩
            [0, 0, 1, 0],  # |01⟩ → |10⟩
            [0, 1, 0, 0],  # |10⟩ → |01⟩
            [0, 0, 0, 1]   # |11⟩ → |11⟩
        ]))

    def draw(self, qubit_number, **kwargs):
        """
        Returns the ASCII representation of the SWAP gate for a specific qubit.

        The SWAP gate has a visual distinction with an "X" symbol connecting the two qubits.

        Args:
            qubit_number (int): The qubit's position in the circuit (1 or 2).

        Returns:
            list: A list of strings representing the ASCII art for the SWAP gate.

        Example:
            .. code-block:: text

                Qubit 1:
                     │     
                ─────✕─────
                     │     

                Qubit 2:
                     │     
                ─────✕─────
                     │     
        """
        if qubit_number == 1:
            return [
                "           ",
                "─────✕─────",
                "     │     ",
            ]
        else:
            return [
                "     │     ",
                "─────✕─────",
                "           ",
            ]


class ArbTwoQubitGate(TwoQubitGate):
    """
    Represents an arbitrary two-qubit quantum gate.

    The `ArbTwoQubitGate` class allows for the creation of two-qubit gates with
    user-defined unitary matrix representations. This provides flexibility for
    designing custom two-qubit quantum gates.

    Attributes:
        matrix (numpy.ndarray): The 4x4 unitary matrix representing the two-qubit gate.

    Methods:
        __init__(matrix): Initializes the gate with the provided matrix representation.
    """

    def __init__(self, matrix):
        """
        Initializes the arbitrary two-qubit gate.

        Ensures that the provided matrix is 4x4 and unitary.

        Args:
            matrix (numpy.ndarray): A 4x4 unitary matrix representing the two-qubit gate.

        Raises:
            TypeError: If the provided matrix is not a numpy array.
            ValueError: If the matrix is not 4x4 or not unitary.
        """
        super().__init__(matrix)
