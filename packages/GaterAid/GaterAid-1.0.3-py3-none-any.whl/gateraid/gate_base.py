"""Implementation of a general 2-qubit unitary gate."""


from abc import ABC
import numpy as np

from gateraid.utilities import check_unitary
from gateraid.quantum_state import QuantumState

np.set_printoptions(formatter={'all': lambda x: "{:.4g}".format(x)})


class TwoQubitGate(ABC):
    """A 2-qubit unitary gate.

    Parameters
    ----------
    matrix : np.ndarray
        The unitary matrix of the gate.
    name : str
        The name of the gate.

    Attributes
    ----------
    matrix : np.ndarray
        The unitary matrix of the gate.
    name : str
        The name of the gate.

    Methods
    -------
    __call__(state: QuantumState) -> QuantumState
        Apply the gate to a quantum state.
    __str__()
        Return string representation of the gate.
    __repr__()
        Return canonical string representation of the gate.

    Example
    -------
    >>> import numpy as np
    >>> from gateraid.gate_base import TwoQubitGate
    >>> matrix = np.array([[1, 0, 0, 0],
                           [0, 1, 0, 0],
                           [0, 0, 0, 1],
                           [0, 0, 1, 0]], dtype=complex)
    >>> name = 'CNOT'
    >>> gate = TwoQubitGate(matrix, name)
    >>> print(gate)
    CNOT gate with matrix:
    [[1+0j 0+0j 0+0j 0+0j]
     [0+0j 1+0j 0+0j 0+0j]
     [0+0j 0+0j 0+0j 1+0j]
     [0+0j 0+0j 1+0j 0+0j]]
    """

    def __init__(self, matrix: np.ndarray, name: str):  # noqa: D107
        self.matrix = matrix
        check_unitary(matrix)
        self.name = name

    def __call__(self, state: QuantumState) -> QuantumState:
        """Apply the gate to a quantum state."""
        return state.apply_matrix(self.matrix, _skip_validation=True)

    def __str__(self):
        """Return string representation of the gate."""
        return f"{self.name} gate with matrix: \n{self.matrix}"

    def __repr__(self):
        """Return canonical string representation of the gate."""
        return f"{self.__class__.__name__}(\
            matrix={self.matrix!r}, name={self.name!r})"
