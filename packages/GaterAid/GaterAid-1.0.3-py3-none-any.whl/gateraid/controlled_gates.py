"""Implementation of common and variable 2-qubit controlled gates."""


import numpy as np

from gateraid.gate_base import TwoQubitGate

control_matrix = np.array([[0, 0], [0, 1]], dtype=complex)
anti_control_matrix = np.array([[1, 0], [0, 0]], dtype=complex)
I_2 = np.eye(2, dtype=complex)


class ControlledUnitary(TwoQubitGate):
    """A controlled unitary gate.

    Parameters
    ----------
    single_qubit_unitary : np.ndarray
        The single-qubit unitary to apply.
    single_qubit_unitary_name : str
        The name of the single-qubit unitary.
    first_qubit_controlled : bool, optional
        Whether the first qubit is the control qubit. Default is True.
    anti_control : bool, optional
        Whether the control is inverted. Default is False.

    Attributes
    ----------
    matrix : np.ndarray
        The unitary matrix of the gate.
    name : str
        The name of the gate.

    Examples
    -------
    >>> import numpy as np
    >>> from gateraid.controlled_gates import ControlledUnitary
    >>> X = np.array([[0, 1], [1, 0]], dtype=complex)
    >>> gate = ControlledUnitary(X, 'X')
    >>> print(gate)
    CX1->2 gate with matrix:
    [[1+0j 0+0j 0+0j 0+0j]
     [0+0j 1+0j 0+0j 0+0j]
     [0+0j 0+0j 0+0j 1+0j]
     [0+0j 0+0j 1+0j 0+0j]]

    >>> import numpy as np
    >>> from gateraid.controlled_gates import ControlledUnitary
    >>> X = np.array([[0, 1], [1, 0]], dtype=complex)
    >>> gate = ControlledUnitary(X, 'X',
                                 first_qubit_controlled=False,
                                 anti_control=True)
    >>> print(gate)
    anti-CX2->1 gate with matrix:
    [[0+0j 0+0j 1+0j 0+0j]
     [0+0j 1+0j 0+0j 0+0j]
     [1+0j 0+0j 0+0j 0+0j]
     [0+0j 0+0j 0+0j 1+0j]]
    """

    def __init__(self,  # noqa D107
                 single_qubit_unitary: np.ndarray,
                 single_qubit_unitary_name: str,
                 first_qubit_controlled: bool = True,
                 anti_control: bool = False):
        control_a, control_b = control_matrix, anti_control_matrix
        if anti_control:
            # Swap the control matrices
            control_a, control_b = control_b, control_a
        two_qubit_unitary = np.kron(control_a, single_qubit_unitary) + \
            np.kron(control_b, I_2) if first_qubit_controlled else \
            np.kron(single_qubit_unitary, control_a) + np.kron(I_2, control_b)

        name = f'{"anti-" if anti_control else ""}' \
            f'C{single_qubit_unitary_name}'\
            f'{"1->2" if first_qubit_controlled else "2->1"}'

        super().__init__(matrix=two_qubit_unitary, name=name)


def make_CX(first_qubit_controlled=True, anti_control=False):
    """Define the controlled-X gate.

    Example
    -------
    >>> import numpy as np
    >>> from gateraid.controlled_gates import make_CX
    >>> from gateraid.quantum_state import QuantumState
    >>> state = QuantumState(np.array([0, 0, 1, 0]))
    >>> CX = make_CX()
    >>> new_state = CX(state)
    >>> print(new_state)
    State:
    0+0j|00> +
    0+0j|01> +
    0+0j|10> +
    1+0j|11>
    """
    return ControlledUnitary(single_qubit_unitary=np.matrix([[0, 1], [1, 0]],
                                                            dtype=complex),
                             single_qubit_unitary_name='X',
                             first_qubit_controlled=first_qubit_controlled,
                             anti_control=anti_control)


def make_CY(first_qubit_controlled=True, anti_control=False):
    """Define the controlled-Y gate.

    Example
    -------
    >>> import numpy as np
    >>> from gateraid.controlled_gates import make_CY
    >>> from gateraid.quantum_state import QuantumState
    >>> state = QuantumState(np.array([0, 0, 1, 0]))
    >>> CY = make_CY()
    >>> new_state = CY(state)
    >>> print(new_state)
    State:
    0+0j|00> +
    0+0j|01> +
    0+0j|10> +
    0+1j|11>
    """
    return ControlledUnitary(single_qubit_unitary=np.matrix([[0, -1j],
                                                             [1j, 0]],
                                                            dtype=complex),
                             single_qubit_unitary_name='Y',
                             first_qubit_controlled=first_qubit_controlled,
                             anti_control=anti_control)


def make_CZ(first_qubit_controlled=True, anti_control=False):
    """Define the controlled-Z gate.

    Example
    -------
    >>> import numpy as np
    >>> from gateraid.controlled_gates import make_CZ
    >>> from gateraid.quantum_state import QuantumState
    >>> state = QuantumState(np.array([0, 0, 0, 1]))
    >>> CZ = make_CZ()
    >>> new_state = CZ(state)
    >>> print(new_state)
    State:
    0+0j|00> +
    0+0j|01> +
    0+0j|10> +
    -1+0j|11>
    """
    return ControlledUnitary(single_qubit_unitary=np.matrix([[1, 0], [0, -1]],
                                                            dtype=complex),
                             single_qubit_unitary_name='Z',
                             first_qubit_controlled=first_qubit_controlled,
                             anti_control=anti_control)
