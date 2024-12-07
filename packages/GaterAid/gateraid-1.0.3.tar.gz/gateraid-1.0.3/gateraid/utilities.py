"""Utilities for gateraid."""


import numpy as np


def check_unitary(matrix: np.ndarray) -> None:
    """Verify that a matrix is unitary.

    Parameters
    ----------
    matrix : np.ndarray
        The matrix to verify.

    Raises
    ------
    TypeError
        If the matrix is not a numpy array.
    TypeError
        If the matrix is not of dtype float, complex or int.
    ValueError
        If the matrix shape is not (4, 4).
    ValueError
        If the matrix is not unitary.
    """
    if not isinstance(matrix, np.ndarray):
        raise TypeError("Matrix should be a 4x4 numpy array, "
                        f"but a {type(matrix).__name__} was provided.")
    if matrix.shape != (4, 4):
        raise ValueError(f"Matrix has shape {matrix.shape}, "
                         "but should be (4,4).")
    if matrix.dtype not in (complex, float, int):
        raise TypeError(f"Matrix has dtype {matrix.dtype}, "
                        f"but should be float, complex or int.")
    if not np.allclose(matrix.conj().T @ matrix, np.eye(4)):
        raise ValueError("Input matrix is not unitary. Should have U†U = I, "
                         f"but U†U =\n{matrix.conj().T @ matrix}")
