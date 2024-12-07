# TEST FOR GATES SCRIPT

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import numpy as np
import its_us.gates as gates


# =========================
# test Gate class
#     - test get_array
#     - test get_num_qubits

def test_Gate(num_qubits = 1, array = [[0,1],[1,0]]):
    """
    Tests the proper initialisation and methods of the Gate class. Tested via pytest.

    Args:
        num_qubits (int): Number of qubits used for test as example.
        array (array-like): Array used for test as example.
    """

    # Initialisation:
    probe_gate = gates.Gate(num_qubits, array)

    # Test for initialsation:
    assert probe_gate.num_qubits == num_qubits
    assert np.array_equal(probe_gate.array, array)

    # Test for get_num_qubits():
    assert probe_gate.get_num_qubits() == num_qubits

    # Test for get_array():
    array_copy = probe_gate.get_array()
    assert np.array_equal(array_copy, array)
    #-- Tests that the copy is not a deep copy of probe_gate.array:
    array_copy[0,0] = 5
    assert not np.array_equal(array_copy, array)


# ===========================
# test GlobalPhaseGate class
#     - test get_global_phase

def test_GlobalPhase(phase = 1):
    """
    Tests the proper initialisation and methods of the GlobalPhaseGate class. Tested via pytest.

    Args:
        phase (float): Global phase.
    """

    # Initialisation:
    probe_gph_gate = gates.GlobalPhaseGate(phase)

    # Test for (super)initialisation:
    assert probe_gph_gate.num_qubits == 1

    # Test for scalability to identity:
    assert np.all(np.isclose(probe_gph_gate.array*np.exp(-1j*phase), np.identity(2)))

    # Test for get_global_phase:
    assert probe_gph_gate.get_global_phase() == phase

    

# =============================
# test RotationGate class
#     - test get_rotation_axis
#     - test get_rotation_angle

def test_RotationGate():
    """
    Tests the proper initialisation and methods of the ControlledGate2 class. Tested via pytest.

    Args:
        None.
    """
    
    # Case 1: axis = Z (theta = 0): We should obtain a phase gate:
    phi = 1
    alpha = 2
    
    #   - Initialisation:
    probe_rot_gate = gates.RotationGate(0, phi, alpha)
    
    #   - Test for (super)initialisation:
    assert probe_rot_gate.num_qubits == 1
    
    #   - Test to check array:
    reference_array = [[np.exp(-1j*alpha/2),0],[0,np.exp(1j*alpha/2)]]
    assert np.all(np.isclose(probe_rot_gate.array, reference_array))

    # Case 2: axis = X (theta = pi/2, phi = 0): We should obtain a phase gate:
    alpha = 1
    
    #   - Initialisation:
    probe_rot_gate = gates.RotationGate(np.pi/2, 0, alpha)
    
    #   - Test to check array:
    hadamard = np.array([[1,1],[1,-1]])/np.sqrt(2)
    reference_array = hadamard @ np.array([[np.exp(-1j*alpha/2),0],[0,np.exp(1j*alpha/2)]]) @ hadamard
    assert np.all(np.isclose(probe_rot_gate.array, reference_array))

    # Test for get_rotation_axis:
    theta, phi = probe_rot_gate.get_rotation_axis()
    assert theta == np.pi/2 and phi == 0

    #Test for get_rotation_angle:
    assert probe_rot_gate.get_rotation_angle() == alpha


# ===========
# test RxGate

def test_RxGate(alpha = 1):
    """
    Tests the proper initialisation and methods of the RxGate class. Tested via pytest.

    Args:
        alpha (float): Rotation angle around the x axis.
    """

    # Initialisation:
    probe_rx_gate = gates.RxGate(alpha)

    # Test for (super)initialisation:
    theta, phi = probe_rx_gate.get_rotation_axis()
    assert theta == np.pi/2 and phi == 0

    # Test for array:
    reference_array = [[np.cos(alpha/2), -1j*np.sin(alpha/2)],
                       [-1j*np.sin(alpha/2), np.cos(alpha/2)]]
    assert np.all(np.isclose(probe_rx_gate.array, reference_array))


# ===========
# test RyGate

def test_RyGate(alpha = 1):
    """
    Tests the proper initialisation and methods of the RxGate class. Tested via pytest.

    Args:
        alpha (float): Rotation angle around the y axis.
    """

    # Initialisation:
    probe_ry_gate = gates.RyGate(alpha)

    # Test for (super)initialisation:
    theta, phi = probe_ry_gate.get_rotation_axis()
    assert theta == np.pi/2 and phi == np.pi/2

    # Test for array:
    reference_array = [[np.cos(alpha/2), -np.sin(alpha/2)],
                       [np.sin(alpha/2), np.cos(alpha/2)]]
    assert np.all(np.isclose(probe_ry_gate.array, reference_array))


# ===========
# test RzGate

def test_RzGate(alpha = 1):
    """
    Tests the proper initialisation and methods of the RxGate class. Tested via pytest.

    Args:
        alpha (float): Rotation angle around the z axis.
    """

    # Initialisation:
    probe_rz_gate = gates.RzGate(alpha)

    # Test for (super)initialisation:
    theta, phi = probe_rz_gate.get_rotation_axis()
    assert theta == 0 and phi == 0

    # Test for array:
    reference_array = [[np.exp(-1j*alpha/2), 0],
                       [0, np.exp(1j*alpha/2)]]
    assert np.all(np.isclose(probe_rz_gate.array, reference_array))
    

# ====================
# test PhaseGate class
#     - test get_phase
#     - test set_phase

def test_PhaseGate(phase = np.pi/2):
    """
    Tests the proper initialisation and methods of the PhaseGate class. Tested via pytest.

    Args:
        phase (float): Example phase used for testing.
    """

    # Initialisation:
    probe_phase_gate = gates.PhaseGate(phase)

    # Test for (super)initialisation:
    assert probe_phase_gate.num_qubits == 1
    assert probe_phase_gate.phase == phase

    # Test for get_phase():
    assert probe_phase_gate.get_phase() == phase

    # Test for set_phase(new_phase):
    new_phase = phase + np.pi/3
    probe_phase_gate.set_phase(new_phase)
    assert probe_phase_gate.phase == new_phase


# ==========================
# test ControlledGate2 class
#     - test get_control
#     - test get_target_gate

def test_ControlledGate2(control = 1, gate = gates.Gate(1, [[0, 1], [1, 0]])):
    """
    Tests the proper initialisation and methods of the ControlledGate2 class. Tested via pytest.

    Args:
        control (int): Position of controlling qubit.
        gate (Gate): Gate used as target.
    """

    # Initialisation:
    probe_controlled_gate = gates.ControlledGate2(control, gate)

    # Test for (super)initialisation:
    assert probe_controlled_gate.control == control
    array = gate.array
    assert np.array_equal(probe_controlled_gate.target_gate.array, array)
    assert probe_controlled_gate.num_qubits == 2
    if control == 1:
        ctrl_array = [[1,0,0,0],
                      [0,1,0,0],
                      [0,0,array[0,0],array[0,1]],
                      [0,0,array[1,0],array[1,1]]]
    elif control == 2:
        ctrl_array = [[1,0,0,0],
                      [0,array[0,0],0,array[0,1]],
                      [0,0,1,0],
                      [0,array[1,0],0,array[1,1]]]
    assert np.array_equal(probe_controlled_gate.array, ctrl_array)

    # Test for get_control:
    assert probe_controlled_gate.get_control() == control

    # Test for get_target_gate:
    probe_target_gate_copy = probe_controlled_gate.get_target_gate()
    assert probe_target_gate_copy.num_qubits == 1
    assert np.array_equal(probe_target_gate_copy.array, array)


# ======================
# test CNOTGate2 class
#     - test get_control

def test_CNOTGate2(control = 1):
    """
    Tests the proper initialisation and methods of the CNOTGate2 class. Tested via pytest.

    Args:
        control (int): Position of controlling qubit.
    """

    # Initialisation:
    probe_cnot_gate = gates.CNOTGate2(control)

    # Test for (super)initialisation:
    assert probe_cnot_gate.control == control

    # Test that it is a particular case of ControlledGate2:
    x_gate = gates.Gate(1, [[0,1],[1,0]])
    reference_cnot_gate = gates.ControlledGate2(control, x_gate)
    assert np.array_equal(probe_cnot_gate.array, reference_cnot_gate.array)


# ===========================
# test CPhaseGate2 class
#     - test get_target_phase

def test_CPhaseGate2():
    """
    Tests the proper initialisation and methods of the CPhaseGate2 class. Tested via pytest.

    Args:
        None.
    """
    
    # Initialisation:
    phase = np.pi
    probe_cphase_gate = gates.CPhaseGate2(phase)

    # Test for (super)initialisation:
    assert probe_cphase_gate.num_qubits == 2

    # Test case CZ:
    ctrl_z_array = np.diag([1,1,1,-1])
    assert np.all(np.isclose(probe_cphase_gate.array, ctrl_z_array))


# ===========================
# test Gate instances classes
#     - IdGate
#     - XGate
#     - YGate
#     - ZGate
#     - HGate
#     - SGate
#     - TGate
#     - SqrtXGate

#     - XXGate2
#     - YYGate2
#     - ZZGate2
#     - HHGate2
#     - CZGate2
#     - CSGate2
#     - DCNOTGate2
#     - SWAPGate2
#     - ISWAPGate2
#     - SqrtSWAPGate2
#     - SqrtISWAPGate2
#     - FTGate2

def test_builtin_gates():
    """
    Tests the proper initialisation of the built-in Gate child classes. Tested via pytest.

    Args:
        None.
    """

    # Provide gate names:
    builtin_gate1_list = ['IdGate',
                         'XGate',
                         'YGate',
                         'ZGate',
                         'HGate',
                         'SGate',
                         'TGate',
                         'SqrtXGate']
    builtin_gate2_list = ['XXGate2',
                          'YYGate2',
                          'ZZGate2',
                          'HHGate2',
                          'CZGate2',
                          'CSGate2',
                          'DCNOTGate2',
                          'SWAPGate2',
                          'ISWAPGate2',
                          'SqrtSWAPGate2',
                          'SqrtISWAPGate2',
                          'FTGate2']
    
    # Provide verified gate arrays (in the same order as the gate instances):
    builtin_gate1_arrays = [np.array([[1,0],[0,1]]),
                           np.array([[0,1],[1,0]]),
                           np.array([[0,-1j],[1j,0]]),
                           np.array([[1,0],[0,-1]]),
                           np.array([[1,1],[1,-1]])/np.sqrt(2),
                           np.array([[1,0],[0,1j]]),
                           np.array([[1,0],[0,(1+1j)/np.sqrt(2)]]),
                           np.array([[1+1j,1-1J],[1-1J,1+1j]])/2]
    builtin_gate2_arrays = [np.array([[0,0,0,1],[0,0,1,0],[0,1,0,0],[1,0,0,0]]),
                            np.array([[0,0,0,-1],[0,0,1,0],[0,1,0,0],[-1,0,0,0]]),
                            np.array([[1,0,0,0],[0,-1,0,0],[0,0,-1,0],[0,0,0,1]]),
                            np.array([[1,1,1,1],[1,-1,1,-1],[1,1,-1,-1],[1,-1,-1,1]])/2,
                            np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,-1]]),
                            np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1j]]),
                            np.array([[1,0,0,0],[0,0,0,1],[0,1,0,0],[0,0,1,0]]),
                            np.array([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]]),
                            np.array([[1,0,0,0],[0,0,1j,0],[0,1j,0,0],[0,0,0,1]]),
                            np.array([[1,0,0,0],[0,(1+1j)/2,(1-1j)/2,0],[0,(1-1j)/2,(1+1j)/2,0],[0,0,0,1]]),
                            np.array([[1,0,0,0],[0,0,1j,0],[0,1j,0,0],[0,0,0,1]]),
                            np.array([[1,1,1,1],[1,1j,-1,-1j],[1,-1,1,-1],[1,-1j,-1,1j]])/2]
    
    # Test for one-qubit built-in gates:
    for i in range(len(builtin_gate1_list)):
        gate = eval(f'gates.{builtin_gate1_list[i]}()')
        array = gate.get_array()

        # Check if unitary:
        assert np.all(np.isclose(np.identity(2),array @ array.conj().T))

        # Check attributes to the verified ones above:
        assert gate.num_qubits == 1
        assert np.array_equal(array, builtin_gate1_arrays[i])

    # Test for two-qubit built-in gates:
    for i in range(len(builtin_gate2_list)):
        gate = eval(f'gates.{builtin_gate2_list[i]}()')
        array = gate.get_array()

        # Check if unitary:
        assert np.all(np.isclose(np.identity(4),array @ array.conj().T))

        # Check attributes to the verified ones above:
        assert gate.num_qubits == 2
        assert np.array_equal(array, builtin_gate2_arrays[i])


# =========================
# test create_gate function

def test_create_gate():
    """
    Tests the function gates.create_gate(num_qubits, array). Tested via pytest.

    Args:
        None.
    """

    # Initialise input and produce output from function to be tested:
    num_qubits = 1
    array = [[1,1],[1,-1]]
    probe_gate = gates.create_gate(num_qubits, array)

    # Check that the size of the gate array is (2^n x 2^n), where n = num_qubits:
    assert probe_gate.array.shape == (2**probe_gate.num_qubits, 2**probe_gate.num_qubits)

    # Check unitarity:
    assert np.all(np.isclose(np.identity(2**num_qubits), probe_gate.array @ probe_gate.array.conj().T))

    # Check if final unitary is Hadamard:
    Hadamard_array = np.array([[1,1],[1,-1]])/np.sqrt(2)
    assert np.all(np.isclose(probe_gate.array, Hadamard_array))


# ========================
# test tensorprod function

def test_tensorprod(num_qubits1 = 1, array1 = [[0,1],[1,0]], 
                    num_qubits2 = 1, array2 = np.array([[1,1],[1,-1]])/np.sqrt(2)):
    """
    Tests the function: gates.tensorprod(gate_list). Tested via pytest.

    Args:
        num_qubits1 (int): Number of qubits for the first gate.
        array1 (ArrayLike): Components of the second gate.
        num_qubits2 (int): Number of qubits for the first gate.
        array2 (ArrayLike): Components of the second gate.
    """

    # Initialise input and produce output from function to be tested:
    gate1 = gates.Gate(num_qubits1, array1)
    gate2 = gates.Gate(num_qubits2, array2)
    gate_tp = gates.tensorprod([gate1, gate2])

    # check if added qubits agree:
    assert gate_tp.num_qubits == gate1.num_qubits + gate2.num_qubits
    
    # Check if the result is a tensor product:
    assert np.all(np.isclose(gate_tp.array, np.kron(gate1.array, gate2.array)))