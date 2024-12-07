##STATES

#documentation
r"""
States script:
==============

- Normalises given initial states for N qubits.
- Given angle(:math:`\theta,\phi`), it gives :math:`| \Psi >` state.
- Provides built-in initial states for 1 and 2 qubits.
- Performs tensor product for any state.

Dependencies:
~~~~~~~~~~~~~
- numpy
- math
- cmath

Built-in 1 qubit states:
~~~~~~~~~~~~~~~~~~~~~~~~

- zero state:
    |0> = [[1],[0]]

- one state:
    |1> = [[0],[1]]

- plus state: 

.. math::

    |+> =  \frac{1}{\sqrt{2}}(|0> + |1>)

- minus state: 

.. math::

    |-> =  \frac{1}{\sqrt{2}}(|0> - |1>)

- plus_i state: 

.. math::

    |i> =  \frac{1}{\sqrt{2}}(|0> + i|1>)

- minus_i state:

.. math::

    |-i> =  \frac{1}{\sqrt{2}}(|0> - i|1>)


Built-in Bell States (2 qubits):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- PsiPlus state: 

.. math::

    | \Psi^+ > =  \frac{1}{\sqrt{2}}(|01> + |10>)

- PsiMinus state: 

.. math::

    | \Psi^- > =  \frac{1}{\sqrt{2}}(|01> - |10>)

- PhiPlus state:

.. math::

    | \Phi^+ > =  \frac{1}{\sqrt{2}}(|00> + |11>)

- PhiMinus state: 

.. math::

    | \Phi^- > =  \frac{1}{\sqrt{2}}(|00> - |11>)

"""

import numpy as np
import warnings
import math, cmath

# Ignore warnings for clean output
warnings.filterwarnings('ignore')

#Parent Class
class States:
    def __init__(self, N = 1, state = np.array([[1], [0]])):
        """
        Initiates the States class.

        Args:
            N (int): The number of qubits that pass through the state,
            array (array_like): A 2^N by 2^N array of floats, where N (int) is the number of qubits.
        """
        self.N = N
        self.state = state
    
    def get_state(self):
        """
        Reads the initial state in vector form.

        Returns:
            ndarray: copy of state array
        """
        copy = np.copy(self.state)

        #Checks if length of the state for N qubits is 2^N or else gives error and suggested correction.
        if len(copy) != 2**self.N:
            raise TypeError("The length of initial states list for " + str(self.N) + " qubit(s) is not " + str(len(copy))+ ". It should be equal to " + str(2**self.N) +".")
        
        return copy
    
    def get_N(self):
        """
        Reads the number of qubits that pass through the state.

        Returns:
            int: number of qubits
        """
        return self.N

#Built-in subclasses
#1 qubit states
class Zero(States):
    """
    This function gives the |0> = [[1],[0]] state.

    Returns:
        array : An array of numbers.
    Args:
        None.
    """
    def __init__(self):
        num_qubits = 1
        array = np.array([[1], [0]])
        super().__init__(num_qubits, array)

class One(States):
    """
    This function gives the |1> = [[0],[1]] state.

    Returns:
        array : An array of numbers.
    Args:
        None.
    """
    def __init__(self):
        num_qubits = 1
        array = np.array([[0], [1]])
        super().__init__(num_qubits, array)

class Plus(States):
    """
    This function gives the |+> state:

    Returns:
        array : An array of numbers.

    Args:
        None.
    """
    def __init__(self):
        num_qubits = 1
        array = (1/math.sqrt(2))*np.array([[1], [1]])
        super().__init__(num_qubits, array)

class Minus(States):
    """
    This function gives the |-> state:

    Returns:
        array : An array of numbers.

    Args:
        None.
    """
    def __init__(self):
        num_qubits = 1
        array = (1/math.sqrt(2))*np.array([[1], [-1]])
        super().__init__(num_qubits, array)

class PlusI(States):
    """
    This function gives the |i> state.

    Returns:
        array : An array of numbers.

    Args:
        None.
    """
    def __init__(self):
        num_qubits = 1
        array = (1/math.sqrt(2))*np.array([[1], [complex(0,1)]])
        super().__init__(num_qubits, array)

class MinusI(States):
    """
    This function gives the |-i> state:

    Returns:
        array : An array of numbers.

    Args:
        None.
    """
    def __init__(self):
        num_qubits = 1
        array = (1/math.sqrt(2))*np.array([[1], [complex(0,-1)]])
        super().__init__(num_qubits, array)

#2 qubit states (Bell states)
class PsiPlus(States):
    r"""
    This function gives the :math:`| \Psi^+ >` state.

    Returns:
        array : An array of numbers.
    
    Args:
        None.
    """
    def __init__(self):
        num_qubits = 2
        array = (1/math.sqrt(2))*((np.kron(Zero().state, One().state) + np.kron(One().state, Zero().state)))
        super().__init__(num_qubits, array)

class PsiMinus(States):
    r"""
    This function gives the :math:`| \Psi^- >` state.

    Returns:
        array : An array of numbers.
    
    Args:
        None.
    """
    def __init__(self):
        num_qubits = 2
        array = (1/math.sqrt(2))*((np.kron(Zero().state, One().state) - np.kron(One().state, Zero().state)))
        super().__init__(num_qubits, array)

class PhiPlus(States):
    r"""
    This function gives the :math:`| \Phi^+ >` state.

    Returns:
        array : An array of numbers.
    
    Args:
        None.
    """
    def __init__(self):
        num_qubits = 2
        array = (1/math.sqrt(2))*((np.kron(Zero().state, Zero().state) + np.kron(One().state, One().state)))
        super().__init__(num_qubits, array)

class PhiMinus(States):
    r"""
    This function gives the :math:`| \Phi^- >` state.

    Returns:
        array : An array of numbers.
    
    Args:
        None.
    """
    def __init__(self):
        num_qubits = 2
        array = (1/math.sqrt(2))*((np.kron(Zero().state, Zero().state) - np.kron(One().state, One().state)))
        super().__init__(num_qubits, array)

#Functions
###########

#Initial Normalised State Function
def norm(N, coef_list):
    """
    Takes a coefficients list:
        1. Checks if list contains only complex numbers with the real and imaginary parts being type integer or float. 
        2. Checks if the length of a list for N qubits is 2^N.
        3. Normalises the list such that sum of squared magnitudes is 1.
        4. Changes list to a column if it was a row.
        5. Returns the normalised list.

    Args:
        coef_list (list): An inititial state list of complex numbers for N qubits.

    Returns:
        array: A normalised initial state array of complex numbers for N qubits.

    """
    #Checks if list contains only complex numbers with the real and imaginary parts being type integer or float.      
    try:
        np.sum(coef_list)
    except:
        raise TypeError('List should contain only complex numbers with the real and imaginary parts being type integer or float.')
    
    #Checks if length of the state for N qubits is 2^N or else gives error and suggested correction.
    if len(coef_list) != 2**N:
        raise TypeError("The length of initial states list for " + str(N) + " qubit(s) is not " + str(len(coef_list))+ ". It should be equal to " + str(2**N) +".")


    coef_arr = np.array(coef_list)
    #Squared magnitude of coeff_list.
    sqrd_mag = []
    for i in range(0,len(coef_arr)):
        coeff2 = coef_arr[i]*(coef_arr[i].conjugate())
        sqrd_mag.append(coeff2)

    #Check if it's normalised.
    if sum(sqrd_mag) == 1:
        return coef_arr.reshape(-1, 1)
    
    #If it's not normalised, normalise it.
    else:
        norm = math.sqrt(sum(sqrd_mag))
        norm_state = (1/norm)*(coef_arr)
        #Make it a column
        if coef_arr.ndim == 1:
            return norm_state.reshape(-1, 1)
        else:
            return norm_state
        
#Initial state formed from given angle theta and phi
def angle(theta = 0, phi = 0):
    r"""
    Takes angles :math:`\theta \ and \ \phi`, and outputs state: :math:`| \Psi > = cos(\frac{\theta}{2})|0> + sin(\frac{\theta}{2})e^{i\phi}|1>`.

    Args:
        theta (int): Polar angle range from :math:`0< \theta < \pi`.
        phi (int): Azimuthal angle range from :math:`0< \phi < 2 \pi`.

    Returns:
        array: A normalised initial state array of complex numbers for 2 qubits.
    
    """
    z = np.array([[1],[0]])
    o = np.array([[0],[1]])

    #if angle given in degrees, change to radians and compute Psi (approximation: works only if given degree is above 2pi)
    if theta > 2*math.pi or phi > 2*math.pi:
        theta_r = math.radians(theta)
        phi_r = math.radians(phi)
        e = cmath.exp(complex(0,phi_r))
        psi = round(math.cos(theta_r/2),8)*z + round(math.sin(theta_r/2),8)*complex(round(e.real, 8), round(e.imag, 8))*o

    #if angle in radians compute Psi directly
    else:
        psi = math.cos(theta/2)*z + math.sin(theta/2)*cmath.exp(complex(0,phi))*o
    
    return psi

#Tensor Product for only 2 qubits
def tp(state_1, state_2):
    """
    Takes an input of two states of length 2:
        1. Checks if the length of each state is 2.
        2. Applies norm function to normalise each state within list and check for errors.
        3. Returns the tensor product of the given two states.

    Args:
        lst (list): Two initial states lists.

    Returns:
        array: A normalised initial tensor product array of complex numbers for 2 qubits.

    """
    #Checks length of list
    if len(state_1) == 2 and len(state_2) == 2:
        #Normalised states 1 and 2
        s1 = norm(1, state_1)
        s2 = norm(1, state_2)
        #Create a tensor product of each item in the list
        tp_state = np.kron(s1, s2)
    else:
        raise TypeError("The length of each initial state list for states 1 and 2 should be 2.")
    return tp_state


#Calling states
state = States()

#Check
# state1 = norm(1, [3,5])
# state2 = norm(1, [8,2])
# print(norm(1, [1,8]))
# print(tp(state1, state2))
# print(angle(90,90))
# print(Zero().state)
# print(PhiPlus().state)


