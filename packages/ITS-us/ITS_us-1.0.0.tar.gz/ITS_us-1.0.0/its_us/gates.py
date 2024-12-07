## GATES

"""
Gates script:
=============

- Provides a class of standard gates for 1 and 2 qubits.
- Allows for custom gate creation, and scales to unitary if necessary.
- Allows for controlled-gate for any gate.
- Can perform tensor product of gates.

Dependencies:
~~~~~~~~~~~~~
- numpy

Built-in one-qubit gates:
~~~~~~~~~~~~~~~~~~~~~~~

    - GlobalPhaseGate(phase): gate that adds a global phase <phase> to the system;
    - RotationGate(theta, phi, alpha): rotation of angle <alpha> around an axis on the Bloch sphere <(theta, phi)>
    - RxGate(alpha): rotation of angle <alpha> around the x axis;
    - RyGate(alpha): rotation of angle <alpha> around the y axis;
    - RzGate(alpha): rotation of angle <alpha> around the z axis;
    - PhaseGate(phase): phase gate on the second register with phase <phase>.

    - IdGate(): identity gate;
    - XGate(): X gate;
    - YGate(): Y gate;
    - ZGate(): Z gate;
    - HGate(): Hadamard gate;
    - SGate(): S gate;
    - TGate(): T gate;
    - SqrtXGate(): square root of X gate.


Built-in 2 qubit gates:
~~~~~~~~~~~~~~~~~~~~~~~

    - ControlledGate2(control, gate1): general controlled gate where the target <gate1> is controlled by qubit at position <control>;
    - CNOTGate2(control): CNOT gate with the control qubit on position <control>;
    - CPhaseGate2(phase): controlled phase gate with phase <phase>.

    - XXGate2(): XxX gate;
    - YYGate2(): YxY gate;
    - ZZGate2(): ZxZ gate;
    - HHGate2(): HxH gate;
    - CZGate2(): control-Z gate;
    - CSGate2(): control-S gate;
    - DCNOTGate2(): double CNOT gate;
    - SWAPGate2(): SWAP gate;
    - ISWAPGate2():iSWAP gate;
    - SqrtSWAPGate2(): square root of SWAP gate;
    - SqrtISWAPGate2(): square root of iSWAP gate;
    - FTGate2(): Quantum Fourier Transform gate.

For more details about the gates (such as their matrix form), check https://en.wikipedia.org/wiki/List_of_quantum_logic_gates.
"""

import numpy as np
from numpy.typing import ArrayLike


# =================
# Gate parent class
#   - Gate(object).


class Gate(object):
    """
    The Gate object is an n-qubit gate represented in the standard basis.
    
    Attributes:
        num_qubits (int): The number of qubits that pass through the gate,
        array (ndarray): 2^n by 2^n array representing the gate.
    """

    def __init__(self, num_qubits: int, array: ArrayLike):
        """
        Initiates the Gate class.

        Args:
            num_qubits (int): The number of qubits that pass through the gate,
            array (array_like): A 2^n by 2^n array of floats, where n = num_qubits (int) is the number of qubits.
        """

        self.num_qubits = num_qubits
        self.array = np.array(array)

    def get_num_qubits(self) -> int:
        """
        Reads the number of qubits that pass through the gate.

        Returns:
            int: Number of qubits.
        """

        return self.num_qubits

    def get_array(self) -> np.ndarray:
        """
        Reads the gate in matrix form.

        Returns:
            ndarray: Copy of gate array.
        """

        copy = np.copy(self.array)
        return copy


# ===================================================
# One-qubit Gate child classes with input parameters:
#   - GlobalPhaseGate(Gate);
#   - RotationGate(Gate);
#   - RxGate(RotationGate);
#   - RyGate(RotationGate);
#   - RzGate(RotationGate);
#   - PhaseGate(Gate).

class GlobalPhaseGate(Gate):
    """
    Global phase gate with given phase.

    Attributes:
        global_phase (float): the global phase.
    """
    def __init__(self, phase: float):
        """
        Initiates the global phase.

        Args:
            phase (float): The global phase.
        """
        num_qubits = 1
        array = np.array([[1,0],[0,1]])*np.exp(1j*phase)
        super().__init__(num_qubits, array)
        self.global_phase = phase
    
    def get_global_phase(self) -> float:
        """
        Reads the global phase of the gate.

        Args:
            None.
        """
        return self.global_phase


class RotationGate(Gate):
    """
    Initiates a general rotation using the coordinates of the axis on the Bloch sphere,
    and the rotation angle around that axis.

    Attributes:
        theta (float): Polar angle of axis on the Bloch sphere.
        phi (float): Azimuthal angle of axis on the Bloch sphere.
        alpha (float): Angle of rotation around the given axis.
    """

    def __init__(self, theta: float, phi: float, alpha: float):
        """
        Args:
        theta (float): Polar angle of axis on the Bloch sphere.
        phi (float): Azimuthal angle of axis on the Bloch sphere.
        alpha (float): Angle of rotation around the given axis.
        """

        num_qubits = 1
        array = [[np.exp(1j*alpha/2)*(np.sin(theta/2))**2 + np.exp(-1j*alpha/2)*(np.cos(theta/2))**2,
                  -1j*np.sin(theta)*np.exp(-1j*phi)*np.sin(alpha/2)],
                 [-1j*np.sin(theta)*np.exp(1j*phi)*np.sin(alpha/2),
                  np.exp(1j*alpha/2)*(np.cos(theta/2))**2 + np.exp(-1j*alpha/2)*(np.sin(theta/2))**2]]
        super().__init__(num_qubits, array)
        self.theta = theta
        self.phi = phi
        self.alpha = alpha
    
    def get_rotation_axis(self) -> tuple[float]:
        """
        Reads the rotation axis as a tuple(theta, phi). Equivalent to a point (theta, phi) on the Bloch sphere.

        Returns:
            tuple: The polar and azimuthal angles of the rotation axis.
        """

        return (self.theta, self.phi)
    
    def get_rotation_angle(self) -> float:
        """
        Reads the rotation angle around the axis (theta, phi).

        Returns:
            float: Angle alpha of rotation around the rotation axis.
        """

        return self.alpha
    
class RxGate(RotationGate):
    """
    Rotation with specified angle along the x axis.
    """
    
    def __init__(self, alpha: float):
        """
        Initiates an X-rotation.

        Args:
            alpha (float): Angle of rotation around the x axis.
        """
        super().__init__(np.pi/2, 0, alpha)


class RyGate(RotationGate):
    """
    Rotation with specified angle along the y axis.
    """
    
    def __init__(self, alpha: float):
        """
        Initiates an Y-rotation.

        Args:
            alpha (float): Angle of rotation around the y axis.
        """
        super().__init__(np.pi/2, np.pi/2, alpha)


class RzGate(RotationGate):
    """
    Rotation with specified angle along the z axis.
    """
    
    def __init__(self, alpha: float):
        """
        Initiates an Z-rotation.

        Args:
            alpha (float): Angle of rotation around the z axis.
        """
        super().__init__(0, 0, alpha)




class PhaseGate(Gate):
    """
    Phase gate from a given input phase. Sign convention:  |1>  ->  exp(+j*phase) |1>.

    Attributes:
        phase (float): The phase of the phase gate.
    """

    def __init__(self, phase: float):
        """
        Initiates the attributes of the phase gate.

        Args:
            phase (float): The input phase, must be a real number.
        """

        num_qubits = 1
        array = [[1,0],[0,np.exp(1j*phase)]]
        super().__init__(num_qubits, array)
        self.phase = phase

    def get_phase(self) -> float:
        """
        Reads the phase of the phase gate.

        Returns:
            float: The phase of the phase gate.
        """

        return self.phase

    def set_phase(self, new_phase: float):
        """
        Sets a new phase for the phase gate (e.g. for a phase gate with a variable input phase).

        Args:
            new_phase (float): The new phase for the phase gate.
        """

        self.phase = new_phase
        self.array = [[1,0],[0,np.exp(1j*new_phase)]]


# ===================================================
# Two-qubit Gate child classes with input parameters:
#   - ControlledGate2(Gate);
#   - CNOTGate2(ControlledGate2);
#   - CPhaseGate2(ControlledGate2).


class ControlledGate2(Gate):
    """
    Controlled gate (custom) for 2 qubit systems, with the control from specified qubit.

    Attributes:
        gate (Gate): Must be a 1-qubit gate.
        control (int): If 1, the control is the first qubit. If 2, the control is the second qubit.
    """

    def __init__(self, control: int, gate1: Gate):
        
        """
        Initiates the attributes of the controlled gate.

        Args:
            gate (Gate): Must be a 1-qubit gate.
            control (int): If 1, the control is the first qubit. If 2, the control is the second qubit.          
        """

        num_qubits = 2
        if gate1.get_num_qubits() != 1:
            raise ValueError('The gate is not a one-qubit gate.')
        U_gate = gate1.get_array()
        if control == 1:
            array = [[1,0,0,0],[0,1,0,0],[0,0,U_gate[0,0],U_gate[0,1]],[0,0,U_gate[1,0],U_gate[1,1]]]
        elif control == 2:
            array = [[1,0,0,0],[0,U_gate[0,0],0,U_gate[0,1]],[0,0,1,0],[0,U_gate[1,0],0,U_gate[1,1]]]
        super().__init__(num_qubits, array)
        self.control = control
        self.target_gate = gate1

    def get_control(self) -> int:
        """
        Reads the position of the control qubit.

        Returns:
            int: The position of the control qubit (1 or 2).
        """
        return self.control

    def get_target_gate(self) -> Gate:
        """
        Reads a copy of the target gate.

        Returns:
            Gate: The target gate used in the control gate.
        """

        target_array_copy = np.copy(self.target_gate.array)
        target_gate_copy = Gate(1, target_array_copy)
        return target_gate_copy

    
class CNOTGate2(ControlledGate2):
    """
    CNOT gate for 2 qubit systems, with the control from specified qubit.
    This is equivalent to "controlled_gate2(X_gate, control)".
    """

    def __init__(self, control: int):
        """
        Initiates the attributes of the CNOT gate.

        Args:
            control (int): If 1, the control is the first qubit. If 2, the control is the second qubit.
        """
        x_gate = Gate(1, [[0,1],[1,0]])
        super().__init__(control, x_gate)
    

class CPhaseGate2(ControlledGate2):
    """
    CNOT gate for 2 qubit systems, with the control from specified qubit.
    This is equivalent to "controlled_gate2(X_gate, control)".
    """

    def __init__(self, phase: float):
        """
        Initiates the attributes of the controlled phase gate.

        Args:
            phase (float): Gives the phase of the target phase gate.
        """
        phase_gate = Gate(1, [[1,0],[0,np.exp(1j*phase)]])
        super().__init__(1, phase_gate)
        self.target_phase = phase

    
    def get_target_phase(self) -> float:
        """
        Reads the phase of the controlled phase gate.

        Returns:
            float: Target phase.
        """
        return self.target_phase

# ======================================================
# One-qubit Gate child classes with no input parameters:
#   - IdGate(Gate);
#   - XGate(Gate);
#   - YGate(Gate);
#   - ZGate(Gate);
#   - HGate(Gate);
#   - SGate(Gate);
#   - TGate(Gate);
#   - SqrtXGate(Gate).


class IdGate(Gate):
    """
    Initiates the identity gate (used usually for tensor products).
    
    Args:
        None.
    """

    def __init__(self):
        num_qubits = 1
        array = [[1,0],[0,1]]
        super().__init__(num_qubits, array)

class XGate(Gate):
    """
    Initiates an X gate.
    
    Args:
        None.
    """

    def __init__(self):
        num_qubits = 1
        array = [[0,1],[1,0]]
        super().__init__(num_qubits, array)

class YGate(Gate):
    """
    Initiates a Y gate.
    
    Args:
        None.
    """

    def __init__(self):
        num_qubits = 1
        array = [[0,-1j],[1j,0]]
        super().__init__(num_qubits, array)

class ZGate(Gate):
    """
    Initiates a Z gate.
    
    Args:
        None.
    """

    def __init__(self):
        num_qubits = 1
        array = [[1,0],[0,-1]]
        super().__init__(num_qubits, array)

class HGate(Gate):
    """
    Initiates a Hadamard gate.
    
    Args:
        None.
    """

    def __init__(self):
        num_qubits = 1
        array = np.array([[1,1],[1,-1]])/np.sqrt(2)
        super().__init__(num_qubits, array)

class SGate(Gate):
    """
    Initiates an S gate.
    
    Args:
        None.
    """
    
    def __init__(self):
        num_qubits = 1
        array = [[1,0],[0,1j]]
        super().__init__(num_qubits, array)

class TGate(Gate):
    """
    Initiates a T gate.
    
    Args:
        None.
    """

    def __init__(self):
        num_qubits = 1
        array = [[1,0],[0,(1+1j)/np.sqrt(2)]]
        super().__init__(num_qubits, array)

class SqrtXGate(Gate):
    """
    Initiates an SX gate, which is the square root of X.
    (SX)^2 = X.
    
    Args:
        None.
    """

    def __init__(self):
        num_qubits = 1
        array = np.array([[1+1j,1-1J],[1-1J,1+1j]])/2
        super().__init__(num_qubits, array)


# ======================================================
# Two-qubit Gate child classes with no input parameters:
#   - XXGate2(Gate);
#   - YYGate2(Gate);
#   - ZZGate2(Gate);
#   - HHGate2(Gate);
#   - CZGate2(Gate);
#   - CSGate2(Gate);
#   - DCNOTGate2(Gate);
#   - SWAPGate2(Gate);
#   - ISWAPGate2(Gate);
#   - SqrtSWAPGate2(Gate);
#   - SqrtISWAPGate2(Gate);
#   - FTGate2(Gate).


class XXGate2(Gate):
    """
    Initiates a XxX gate.
    
    Args:
        None.
    """

    def __init__(self):
        num_qubits = 2
        array = [[0,0,0,1],[0,0,1,0],[0,1,0,0],[1,0,0,0]]
        super().__init__(num_qubits, array)

class YYGate2(Gate):
    """
    Initiates a XxX gate.
    
    Args:
        None.
    """

    def __init__(self):
        num_qubits = 2
        array = [[0,0,0,-1],[0,0,1,0],[0,1,0,0],[-1,0,0,0]]
        super().__init__(num_qubits, array)

class ZZGate2(Gate):
    """
    Initiates a XxX gate.
    
    Args:
        None.
    """

    def __init__(self):
        num_qubits = 2
        array = [[1,0,0,0],[0,-1,0,0],[0,0,-1,0],[0,0,0,1]]
        super().__init__(num_qubits, array)

class HHGate2(Gate):
    """
    Initiates a HxH gate.
    
    Args:
        None.
    """

    def __init__(self):
        num_qubits = 2
        array = np.array([[1,1,1,1],[1,-1,1,-1],[1,1,-1,-1],[1,-1,-1,1]])/2
        super().__init__(num_qubits, array)

class CZGate2(Gate):
    """
    Initiates a CZ (controlled-Z) gate for 2 qubits.
    
    Args:
        None.
    """

    def __init__(self):
        num_qubits = 2
        array = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,-1]]
        super().__init__(num_qubits, array)

class CSGate2(Gate):
    """
    Initiates a CS (controlled-S) gate for 2 qubits.
    
    Args:
        None.
    """

    def __init__(self):
        num_qubits = 2
        array = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1j]]
        super().__init__(num_qubits, array)

class DCNOTGate2(Gate):
    """
    Initiates a DCNOT (double-CNOT) gate for 2 qubits.
    
    Args:
        None.
    """

    def __init__(self):
        num_qubits = 2
        array = [[1,0,0,0],[0,0,0,1],[0,1,0,0],[0,0,1,0]]
        super().__init__(num_qubits, array)

class SWAPGate2(Gate):
    """
    Initiates a SWAP gate for 2 qubits.
    
    Args:
        None.
    """

    def __init__(self):
        num_qubits = 2
        array = [[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]]
        super().__init__(num_qubits, array)

class ISWAPGate2(Gate):
    """
    Initiates an iSWAP gate for 2 qubits.
    
    Args:
        None.
    """

    def __init__(self):
        num_qubits = 2
        array = [[1,0,0,0],[0,0,1j,0],[0,1j,0,0],[0,0,0,1]]
        super().__init__(num_qubits, array)

class SqrtSWAPGate2(Gate):
    """
    Initiates a square root of the SWAP gate for 2 qubits.
    (SqrtSWAP)^2 = SWAP.
    
    Args:
        None.
    """

    def __init__(self):
        num_qubits = 2
        array = [[1,0,0,0],[0,(1+1j)/2,(1-1j)/2,0],[0,(1-1j)/2,(1+1j)/2,0],[0,0,0,1]]
        super().__init__(num_qubits, array)

class SqrtISWAPGate2(Gate):
    """
    Initiates a square root of the iSWAP gate for 2 qubits.
    (SqrtiSWAP)^2 = iSWAP.
    
    Args:
        None.
    """

    def __init__(self):
        num_qubits = 2
        array = [[1,0,0,0],[0,0,1j,0],[0,1j,0,0],[0,0,0,1]]
        super().__init__(num_qubits, array)

class FTGate2(Gate):
    """
    Initiates a Quantum Fourier Transform gate.
    
    Args:
        None.
    """

    def __init__(self):
        num_qubits = 2
        array = np.array([[1,1,1,1],[1,1j,-1,-1j],[1,-1,1,-1],[1,-1j,-1,1j]])/2
        super().__init__(num_qubits, array)


# ===================================
# Functions:
#   - create_gate(num_qubits, array);
#   - tensorprod(gate_list).


def create_gate(num_qubits: int, array: ArrayLike) -> Gate:
    """
    Creates a customised gate U. It needs to be unitary or scalable to unitary, in which case it is automatically scaled to a unitary matrix.

    Args:
        num_qubits (int): The number of qubits that pass through the gate.
        array (array_like): A 2^n by 2^n array of floats, where n = num_qubits (int) is the number of qubits.
    
    Returns:
        Gate: The custom gate.
    """
    
    gate = Gate(num_qubits, array)

    # Array must contain ints, floats or complex numbers.
    try:
        np.sum(gate.array)
    except:
        raise TypeError('Input array contains non-numerical elements. Elements of the array \
                        should be integers, float points, or complex numbers of the form (<float> + <float> j).')
    
    # Array must be square of the form (2^n x 2^n).
    if gate.array.shape != (2**gate.num_qubits, 2**gate.num_qubits):
        raise ValueError('The number of qubits does not match array size. Check that a- your \
                            array is square, b- its size is (2^n x 2^n).')
    
    # Array must be unitary or scalable to a unitary matrix. For the latter case, it is rescaled to a unitary matrix.
    check_identity = gate.array @ gate.array.conj().T

    if not np.all(np.isclose(check_identity, np.identity(2**gate.num_qubits) * check_identity[0,0])):
        raise ValueError('The gate is not unitary or scalable to unitary. Check for typos in the matrix elements.')
    elif check_identity[0,0] != 1:
        gate.array = gate.array / np.sqrt(check_identity[0,0])
    
    return gate

def tensorprod(gate_list: list[Gate]) -> Gate:
    """
    Calculates the tensor product of gates from a list.

    Args:
        gate_list (list): List of Gate objects.
    
    Returns:
        Gate: Resulting gate.
    """

    # Test if input is a list of gates.
    tester = 0
    for i in range(len(gate_list)):
        try:
            tester += gate_list[i].num_qubits
        except:
            raise TypeError(f'Entry {i} from the list is not a Gate object.')

    tensor_array = gate_list[0].array
    tensor_num_qubits = gate_list[0].num_qubits
    
    for gate in gate_list[1:]:
        tensor_array = np.kron(tensor_array, gate.array)
        tensor_num_qubits += gate.num_qubits
    
    tensor_gate = Gate(tensor_num_qubits, tensor_array)
    return tensor_gate

