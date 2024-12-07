"""
Circuits module
==============

- Provides a class of constructing a circuit on either 1 or two qubits
- Both single qubit and two qubit files can be added to the circuit
- Can perform measurements in the computational basis

Dependencies:
~~~~~~~~~~~~~
- numpy
- gates
- states
- copy
- random

"""

import numpy as np
from its_us.states import *
from its_us.gates import Gate, HGate, CNOTGate2
from copy import deepcopy
from random import Random


class Circuits:
    """
    The Circuits object is a representation of a quantum circuit that stores the
    sequential order of unitary operations

    Attributes:
        N_wires (int): The number of qubits/wires of the circuit
        State_init (States): The initial state of the circuit
    """

    def __init__(self, N_wires=1, state_init=Zero()):

        self.N_wires = N_wires
        self.state_init = state_init
        self.state_final = None  # NoneType update after circuit_ran method
        self.gates = []
        self.circuit_ran = False

        # checks on the input variables
        if isinstance(state_init, States) == False:
            raise TypeError("Initial state must be State type")
        while N_wires not in [1, 2]:
            raise TypeError("Number of wires must be 1 or 2")

        # check that the initial state has the correct dimension for the number of wires
        if np.log2(len(state_init.get_state())) != N_wires:
            raise ValueError(
                "The initial state dimension must match the number of wires."
            )

    def get_gates(self):
        """
        Returns the current list of gates in the circuit

        Returns:
            list: a list of tuples ([i], gate), where [i] is a list indicating which
            wire the circuit is on and gate is the Gate object
        """
        return self.gates

    def get_state_init(self):
        """
        Returns the initial quantum state of the circuit as an array

        Returns:
            array: The state as a numpy array

        """
        return self.state_init.get_state()

    def get_state_final(self):
        """
        Returns the final quantum state after running circuit. If the
        circuit has not been called, returns a NoneType with a warning message

        Returns:
            array: The final state as a numpy array
            NoneType: If the circuit has not been run

        """
        if self.state_final is None:
            print("Warning: Circuit has not been run, returning NoneType")
            return None

        return self.state_final.get_state()

    def add_single_qubit_gate(self, gate: Gate, target_wire: int = 0):
        """
        Function to add a single qubit gate to the circuit at a given wire.
        Creates a tuple of the gate and the target wire and appends it to the gates list.

        Args:
            gate (Gates): The gate to be added to the circuit.
            target_wire (int): The wire the gate is to be applied to.
        """
        if target_wire > self.N_wires - 1:
            raise ValueError(
                "target wire must not exceed the number of wires in the circuit."
            )
        if gate.get_num_qubits() != 1:
            raise ValueError("The gate must be a single qubit gate.")

        gate_target_tuple = (target_wire, gate)
        self.gates.append(gate_target_tuple)

    def add_two_qubit_gate(self, gate: Gate, target_wires: list = [0, 1]):
        """
        Function to add a two qubit gate to the circuit at a given wire.
        Creates a tuple of the gate and the target wires and appends it to the gates list.

        Args:
            gate (Gates): The gate to be added to the circuit.
            target_wire (int): The wire the gate is to be applied to.
        """
        if max(target_wires) > self.N_wires - 1 or min(target_wires) < 0:
            raise ValueError(
                "Target wires must not exceed the number of wires in the circuit."
            )
        if gate.get_num_qubits() != 2:
            raise ValueError("The gate must be a single qubit gate.")

        gate_target_tuple = (target_wires, gate)
        self.gates.append(gate_target_tuple)

    def run_circuit(self):
        """
        Applies the circuit to the initial state

        Returns:
            State: Final state after running the circuit
        """
        # prepare initial state array
        state_array = deepcopy(self.get_state_init())
        for gate in self.gates:
            # create a temporary identity matrix based on the number of wires

            if gate[1].num_qubits == 1:
                identity_list = [np.eye(2)] * self.N_wires
                identity_list[gate[0]] = gate[1].get_array()
                try:
                    # for 2 wires
                    N_wire_gate = np.kron(*identity_list)
                except TypeError:
                    # for 1 wire
                    N_wire_gate = gate[1].get_array()

            elif gate[1].num_qubits == 2:
                N_wire_gate = gate[1].get_array()

            state_array = N_wire_gate @ state_array

        # override previous class variables
        self.circuit_ran = True
        self.state_final = States(state=state_array, N=self.N_wires)
        return self.state_final

    def measure_qubits(self, seed: int = None, print_outcome=False):
        """
        Applies a projection operator in the computational Z basis to the final state with
        a probability distribution constructed from the final states' amplitudes, also
        in the Z basis. Collapses the final state into a basis state of the computational
        basis, overwriting it and destroying its quantum information.

        Args:
            seed (int): seed to fix probability distribution
            print (Bool): print the measurement outcome
        Returns:

            States: The final projected state. Calling this function overwrites the
            final state post-application of the quantum circuit. If run_circuit has not
            been called, then a NoneType is returned.

        """
        if seed is None:
            rng = Random()

        else:
            rng = Random()
            rng.seed(seed)

        # return NoneType
        if not self.circuit_ran:
            print("The circuit has not been run - no measurement performed")
            return None

        # construct final probability distribution as an array of P(i) = |<i|psi>|**2
        distribution = self.state_final.get_state() * np.conj(
            self.state_final.get_state()
        )

        # construct binary outcome list and randomly choose the outcome
        outcome_sequence = np.arange(2**self.N_wires)
        outcome = rng.choices(outcome_sequence, weights=distribution, k=1)[
            0
        ]  # choices returns an array...

        # construct the final state array
        state_array = np.zeros(2**self.N_wires)
        state_array[outcome] = 1

        if print_outcome:
            print(f"Final measurement outcome is {str(bin(outcome)[2:]).zfill(self.N_wires)}")

        self.state_final = States(N=self.N_wires, state=state_array)

        # reset seed post measurement

        return self.state_final