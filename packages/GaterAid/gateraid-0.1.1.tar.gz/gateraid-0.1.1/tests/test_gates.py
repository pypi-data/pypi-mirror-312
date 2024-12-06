import numpy as np
from scipy.linalg import expm
from gateraid.other_gates import *
from gateraid.controlled_gates import *

def test_GeneralUnitary():
    theta = 3.5
    input_1 = {'IZ': theta}
    input_2 = {'ZZ': theta}
    Z = make_Z()
    single_qubit_unitary = expm(theta*1j*Z)
    U0 = LocalUnitary(single_qubit_unitary, f"exp(i{theta}Z)", 1)
    U1 = GeneralUnitary(input_1)
    U2 = GeneralUnitary(input_2)
    assert np.allclose(U0.matrix, U1.matrix) 
    assert not np.allclose(U0.matrix, U2.matrix) 

def test_SWAP():
    Rxx = GeneralUnitary({'XX': -np.pi/4}).matrix
    Ryy = GeneralUnitary({'YY': -np.pi/4}).matrix
    Rzz = GeneralUnitary({'ZZ': -np.pi/4}).matrix
    SWAP_1 = (1+1j)/np.sqrt(2) * Rxx @ Ryy @ Rzz
    SWAP_2 = make_SWAP().matrix
    assert np.allclose(SWAP_1, SWAP_2)

def test_iSWAP():
    Rxx = GeneralUnitary({'XX': np.pi/4}).matrix
    Ryy = GeneralUnitary({'YY': np.pi/4}).matrix
    iSWAP_1 = Rxx @ Ryy 
    iSWAP_2 = make_iSWAP().matrix
    assert np.allclose(iSWAP_1, iSWAP_2)

def test_sqrt_SWAP():
    input = {'II': np.pi/8, 'XX': -np.pi/8, 'YY': -np.pi/8, 'ZZ': -np.pi/8}
    sqrt_SWAP_1 = GeneralUnitary(input).matrix
    sqrt_SWAP_2 = make_sqrt_SWAP().matrix
    assert np.allclose(sqrt_SWAP_1, sqrt_SWAP_2)

def test_sqrt_iSWAP():
    Rxx = GeneralUnitary({'XX': np.pi/8}).matrix
    Ryy = GeneralUnitary({'YY': np.pi/8}).matrix
    sqrt_iSWAP_1 = Rxx @ Ryy 
    sqrt_iSWAP_2 = make_sqrt_iSWAP().matrix
    assert np.allclose(sqrt_iSWAP_1, sqrt_iSWAP_2)

def test_CNOT():
    Ry1 = GeneralUnitary({'YI': np.pi/4}).matrix
    Rx1 = GeneralUnitary({'XI': np.pi/4}).matrix
    Rx2 = GeneralUnitary({'IX': np.pi/4}).matrix
    Rxx = GeneralUnitary({'XX': -np.pi/4}).matrix
    Ry2 = GeneralUnitary({'YI': -np.pi/4}).matrix
    CNOT_1 = (1-1j)/np.sqrt(2) * Ry1 @ Rx1 @ Rx2 @ Rxx @ Ry2
    CNOT_2 = make_CX().matrix
    assert np.allclose(CNOT_1, CNOT_2)

def test_CZ():
    CNOT = make_CX().matrix
    H = make_H()
    IH = LocalUnitary(H, 'H', 1).matrix
    CZ_1 = IH @ CNOT @ IH
    CZ_2 = make_CZ().matrix
    assert np.allclose(CZ_1, CZ_2)
