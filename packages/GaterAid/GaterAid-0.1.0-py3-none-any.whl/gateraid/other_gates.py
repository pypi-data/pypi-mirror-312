"""Implementation of common and variable 2-qubit gates."""


import numpy as np

from scipy.linalg import expm
from gateraid.gate_base import TwoQubitGate


class GeneralUnitary(TwoQubitGate):
    """Initialise a 2-qubit gate, in the form U = exp(i[∑_i c_i P_i]), where \
    P_i are Pauli matrices and c_i the coefficients.

    Parameters
    ----------
    pauli_dict : dict[str, float]
        A dictionary where the keys represent 2-qubit Pauli matricies
        and the values are the coefficients of the Pauli matrices.

    Attributes
    ----------
    matrix : np.ndarray
        The unitary matrix of the gate.
    name : str
        The name of the gate.

    Raises
    ------
    ValueError
        If the keys of the dictionary are not 2-character strings, made up of
        'I', 'X', 'Y' and 'Z'.
    ValueError
        If the values of the dictionary are not real numbers.

    Example
    -------
    >>> import numpy as np
    >>> from gateraid.other_gates import GeneralUnitary
    >>> pauli_dict = {'II': 1, 'XX': 1, 'YY': 1, 'ZZ': 1}
    >>> gate = GeneralUnitary(pauli_dict)
    >>> print(gate)
    exp(i[+1II+1XX+1YY+1ZZ]) gate with matrix:
    [[-0.4161+0.9093j 0+0j 0+0j 0+0j]
     [0+0j -0.4161+0j 0+0.9093j 0+0j]
     [0+0j 0+0.9093j -0.4161+0j 0+0j]
     [0+0j 0+0j 0+0j -0.4161+0.9093j]]
    """

    def __init__(self,  # noqa D107
                 pauli_dict: dict[str, float]):

        # Lookup dictionary for the 1-qubit Paulis
        lookup = {'I': np.eye(2, dtype=complex),
                  'X': np.array([[0, 1], [1, 0]], dtype=complex),
                  'Y': np.array([[0, -1j], [1j, 0]], dtype=complex),
                  'Z': np.array([[1, 0], [0, -1]], dtype=complex)}

        name = 'exp(i['

        # Generate a linear combination of 2-qubit Pauli strings
        operator = np.zeros((4, 4), dtype=complex)
        for key in pauli_dict:
            paulis = list(key)
            if (
                (len(paulis) != 2)
                or (paulis[0] not in lookup.keys())
                or (paulis[1] not in lookup.keys())
            ):
                raise ValueError("Keys of dictionary should be 2-character "
                                 "strings where the characters are either "
                                 "'I', 'X', 'Y' or 'Z'.")
            pauli_string = np.kron(lookup[paulis[0]], lookup[paulis[1]])

            coeff = pauli_dict[key]
            if not np.isreal(coeff):
                raise ValueError("Values of dictionary should be real "
                                 "numbers.")

            operator += coeff * pauli_string
            name += f'+{round(coeff, 2)}{key}'

        name += '])'

        # Take the exponential of this hermitian operator times
        # the imaginary unit
        two_qubit_unitary = expm(1j*operator)

        super().__init__(matrix=two_qubit_unitary, name=name)


class LocalUnitary(TwoQubitGate):
    """Initialise a 2-qubit gate that acts on a single qubit.

    Parameters
    ----------
    single_qubit_unitary : np.ndarray
        The single-qubit unitary that acts on the specified site.
    single_qubit_unitary_name : str
        The name of the single-qubit unitary.
    site : int
        The index of the qubit that the single-qubit unitary acts on.

    Attributes
    ----------
    matrix : np.ndarray
        The unitary matrix of the gate.
    name : str
        The name of the gate.

    Raises
    ------
    ValueError
        If the site index is not 0 or 1.

    Example
    -------
    >>> import numpy as np
    >>> from gateraid.other_gates import LocalUnitary
    >>> X = np.array([[0, 1], [1, 0]], dtype=complex)
    >>> gate = LocalUnitary(X, 'X', 0)
    >>> print(gate)
    X_I gate with matrix:
    [[0+0j 0+0j 1+0j 0+0j]
     [0+0j 0+0j 0+0j 1+0j]
     [1+0j 0+0j 0+0j 0+0j]
     [0+0j 1+0j 0+0j 0+0j]]
    """

    def __init__(self,  # noqa D107
                 single_qubit_unitary: np.ndarray,
                 single_qubit_unitary_name: str,
                 site: int):
        I = np.eye(2, dtype=complex)  # noqa: E741, N806
        if site not in [0, 1]:
            raise ValueError("Site index is out of range - "
                             "should take values of 0 or 1.")

        # Take tensor product of the single-qubit unitary on specifiied site
        # with the identity on unused site
        elif site == 0:
            two_qubit_unitary = np.kron(single_qubit_unitary, I)
            name = single_qubit_unitary_name + '_I'
        else:
            two_qubit_unitary = np.kron(I, single_qubit_unitary)
            name = 'I_' + single_qubit_unitary_name

        super().__init__(matrix=two_qubit_unitary, name=name)


def make_SWAP():
    """Define the SWAP gate.

    Example
    -------
    >>> import numpy as np
    >>> from gateraid.other_gates import make_SWAP
    >>> from gateraid.quantum_state import QuantumState
    >>> state = QuantumState(np.array([0, 1, 0, 0]))
    >>> SWAP = make_SWAP()
    >>> new_state = SWAP(state)
    >>> print(new_state)
    State:
    0+0j|00> +
    0+0j|01> +
    1+0j|10> +
    0+0j|11>
    """
    matrix = np.array([[1, 0, 0, 0],
                       [0, 0, 1, 0],
                       [0, 1, 0, 0],
                       [0, 0, 0, 1]], dtype=complex)
    return TwoQubitGate(matrix=matrix, name='SWAP')


def make_iSWAP():
    """Define the iSWAP gate.

    Example
    -------
    >>> import numpy as np
    >>> from gateraid.other_gates import make_iSWAP
    >>> from gateraid.quantum_state import QuantumState
    >>> state = QuantumState(np.array([0, 1, 0, 0]))
    >>> iSWAP = make_iSWAP()
    >>> new_state = iSWAP(state)
    >>> print(new_state)
    State:
    0+0j|00> +
    0+0j|01> +
    0+1j|10> +
    0+0j|11>
    """
    matrix = np.array([[1, 0, 0, 0],
                       [0, 0, 1j, 0],
                       [0, 1j, 0, 0],
                       [0, 0, 0, 1]], dtype=complex)
    return TwoQubitGate(matrix=matrix, name='iSWAP')


def make_sqrt_SWAP():
    """Define the √SWAP gate.

    Example
    -------
    >>> import numpy as np
    >>> from gateraid.other_gates import make_sqrt_SWAP
    >>> from gateraid.quantum_state import QuantumState
    >>> state = QuantumState(np.array([0, 1, 0, 0]))
    >>> sqrt_SWAP = make_sqrt_SWAP()
    >>> new_state = sqrt_SWAP(state)
    >>> print(new_state)
    State:
    0+0j|00> +
    0.5+0.5j|01> +
    0.5-0.5j|10> +
    0+0j|11>
    """
    matrix = np.array([[1, 0, 0, 0],
                       [0, (1+1j)/2, (1-1j)/2, 0],
                       [0, (1-1j)/2, (1+1j)/2, 0],
                       [0, 0, 0, 1]], dtype=complex)
    return TwoQubitGate(matrix=matrix, name='√SWAP')


def make_sqrt_iSWAP():
    """Define the √iSWAP gate.

    Example
    -------
    >>> import numpy as np
    >>> from gateraid.other_gates import make_sqrt_iSWAP
    >>> from gateraid.quantum_state import QuantumState
    >>> state = QuantumState(np.array([0, 1, 0, 0]))
    >>> sqrt_iSWAP = make_sqrt_iSWAP()
    >>> new_state = sqrt_iSWAP(state)
    >>> print(new_state)
    State:
    0+0j|00> +
    0.7071+0j|01> +
    0+0.7071j|10> +
    0+0j|11>
    """
    matrix = np.array([[1, 0, 0, 0],
                       [0, 1/np.sqrt(2), 1j/np.sqrt(2), 0],
                       [0, 1j/np.sqrt(2), 1/np.sqrt(2), 0],
                       [0, 0, 0, 1]], dtype=complex)
    return TwoQubitGate(matrix=matrix, name='√iSWAP')


def make_X():
    """Define the X gate.

    Example
    -------
    >>> from gateraid.other_gates import make_X, LocalUnitary
    >>> from gateraid.quantum_state import QuantumState
    >>> state = QuantumState()
    >>> X = make_X()
    >>> XI = LocalUnitary(X, 'X', 0)
    >>> new_state = XI(state)
    >>> print(new_state)
    State:
    0+0j|00> +
    0+0j|01> +
    1+0j|10> +
    0+0j|11>
    """
    return np.array([[0, 1], [1, 0]], dtype=complex)


def make_Y():
    """Define the Y gate.

    Example
    -------
    >>> from gateraid.other_gates import make_Y, LocalUnitary
    >>> from gateraid.quantum_state import QuantumState
    >>> state = QuantumState()
    >>> Y = make_Y()
    >>> YI = LocalUnitary(Y, 'Y', 0)
    >>> new_state = YI(state)
    >>> print(new_state)
    State:
    0+0j|00> +
    0+0j|01> +
    0+1j|10> +
    0+0j|11>
    """
    return np.array([[0, -1j], [1j, 0]], dtype=complex)


def make_Z():
    """Define the Z gate.

    Example
    -------
    >>> import numpy as np
    >>> from gateraid.other_gates import make_Z, LocalUnitary
    >>> from gateraid.quantum_state import QuantumState
    >>> state = QuantumState(np.array([0, 0, 1, 0]))
    >>> Z = make_Z()
    >>> ZI = LocalUnitary(Z, 'Z', 0)
    >>> new_state = ZI(state)
    >>> print(new_state)
    State:
    0+0j|00> +
    0+0j|01> +
    -1+0j|10> +
    0+0j|11>
    """
    return np.array([[1, 0], [0, -1]], dtype=complex)


def make_H():
    """Define the Hadamard gate.

    Example
    -------
    >>> from gateraid.other_gates import make_H, LocalUnitary
    >>> from gateraid.quantum_state import QuantumState
    >>> state = QuantumState()
    >>> H = make_H()
    >>> HI = LocalUnitary(H, 'H', 0)
    >>> new_state = HI(state)
    >>> print(new_state)
    State:
    0.7071+0j|00> +
    0+0j|01> +
    0.7071+0j|10> +
    0+0j|11>
    """
    return np.array([[1, 1], [1, -1]], dtype=complex)/np.sqrt(2)


def make_S():
    """Define the S gate.

    Example
    -------
    >>> import numpy as np
    >>> from gateraid.other_gates import make_S, LocalUnitary
    >>> from gateraid.quantum_state import QuantumState
    >>> state = QuantumState(np.array([0, 0, 1, 0]))
    >>> S = make_S()
    >>> SI = LocalUnitary(S, 'S', 0)
    >>> new_state = SI(state)
    >>> print(new_state)
    State:
    0+0j|00> +
    0+0j|01> +
    0+1j|10> +
    0+0j|11>
    """
    return np.array([[1, 0], [0, 1j]], dtype=complex)


def make_T():
    """Define the T gate.

    Example
    -------
    >>> import numpy as np
    >>> from gateraid.other_gates import make_T, LocalUnitary
    >>> from gateraid.quantum_state import QuantumState
    >>> state = QuantumState(np.array([0, 0, 1, 0]))
    >>> T = make_T()
    >>> TI = LocalUnitary(T, 'T', 0)
    >>> new_state = TI(state)
    >>> print(new_state)
    State:
    0+0j|00> +
    0+0j|01> +
    0.7071+0.7071j|10> +
    0+0j|11>
    """
    return np.array([[1, 0], [0, (1+1j)/np.sqrt(2)]], dtype=complex)
