"""Implementation of a 2-qubit quantum state."""


import numpy as np

from gateraid.utilities import check_unitary


class QuantumState:
    """A 2-qubit quantum state.

    Parameters
    ----------
    state : np.ndarray, optional
        The state to initialize. Default is |00>=np.array([1, 0, 0, 0]).

    Attributes
    ----------
    state : np.ndarray
        The state of the quantum system.

    Raises
    ------
    ValueError
        If the state is not a 4x1 column vector.
    ValueError
        If the state is not normalized.

    Methods
    -------
    __str__()
        Return string representation of the quantum state.
    __repr__()
        Return canonical string representation of the quantum state.
    apply_matrix(matrix: np.ndarray, _skip_validation=False) -> QuantumState
        Apply a matrix to the state.

    Examples
    --------
    >>> from gateraid.quantum_state import QuantumState
    >>> state = QuantumState()
    >>> print(state)
    State:
    1+0j|00> +
    0+0j|01> +
    0+0j|10> +
    0+0j|11>

    >>> import numpy as np
    >>> from gateraid.quantum_state import QuantumState
    >>> state = QuantumState(np.array([1, 0, 0, 1])/np.sqrt(2))
    >>> print(state)
    State:
    0.7071+0j|00> +
    0+0j|01> +
    0+0j|10> +
    0.7071+0j|11>
    """

    def __init__(self, state=None):  # noqa: D107
        if state is None:
            state = np.array([1, 0, 0, 0], dtype=complex)
        state = state.astype(complex)
        if state.shape == (4,):
            # Make the state a column vector suitable for matrix multiplication
            state = state[:, None]
        if state.shape != (4, 1):
            raise ValueError(f"State has shape {state.shape}, "
                             "but it should be (4,1) or (4,)")
        if not np.allclose(np.linalg.norm(state), 1):
            raise ValueError("Provided state has a norm of "
                             f"{np.linalg.norm(state)}, but "
                             "this should be (approximately) 1.")
        self.state = state

    def __repr__(self):
        """Return canonical string representation of the quantum state."""
        return f"{self.__class__.__name__}({self.state!r})"

    def __str__(self):
        """Return string representation of the quantum state."""
        return f"State: \
            \n{self.state[0, 0]:.4g}|00> + \n{self.state[1, 0]:.4g}|01> + \
            \n{self.state[2, 0]:.4g}|10> + \n{self.state[3, 0]:.4g}|11>"

    def apply_matrix(self, matrix: np.ndarray, _skip_validation=False):
        """Apply a matrix to the state.

        Parameters
        ----------
        matrix : np.ndarray
            The matrix to apply.
        _skip_validation : bool, optional
            Skip the validation of the matrix, by default False.

        Returns
        -------
        QuantumState
            The updated quantum state.

        Example
        -------
        >>> state = QuantumState(np.array([0, 0, 1, 0]))
        >>> matrix = np.array([[1, 0, 0, 0],
                               [0, 1, 0, 0],
                               [0, 0, 0, 1],
                               [0, 0, 1, 0]], dtype=complex)
        >>> state.apply_matrix(matrix)
        >>> print(state)
        State:
        0+0j|00> +
        0+0j|01> +
        0+0j|10> +
        1+0j|11>
        """
        if not _skip_validation:
            # If applying this using the Gate(State) notation,
            # no need to repeat the checks
            check_unitary(matrix)
        self.state = matrix @ self.state
        return self
