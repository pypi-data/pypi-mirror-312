import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import numpy as np
from its_us.states import *
from its_us.gates import *
from its_us.circuits import Circuits
import random


def test_add_single_gates():
    """
    Test to ensure that the gate added to the Gates.gates list of tuples is added correctly
    """
    # check a Hadamard is added on the 0th wire
    H_gate = HGate()
    tuple_to_check = (0, H_gate)

    circuit_test = Circuits()
    circuit_test.add_single_qubit_gate(H_gate)

    circuit_test_entry = circuit_test.get_gates()[0]

    assert circuit_test_entry == tuple_to_check


def test_add_two_qubit_gates():
    """
    Test to ensure that the gate added to the Gates.gates list of tuples is added correctly
    """
    # check a Hadamard is added on the 0th wire
    CNOT = CNOTGate2(control=2)
    tuple_to_check = ([0, 1], CNOT)

    zero_two_wires = tp([1, 0], [1, 0])
    circuit_test = Circuits(N_wires=2, state_init=States(N=2, state=zero_two_wires))

    circuit_test.add_two_qubit_gate(CNOT, [0, 1])

    circuit_test_entry = circuit_test.get_gates()[0]

    assert circuit_test_entry == tuple_to_check


def test_run_one_wire():
    """
    Test the run_circuits method on a few cases:

    H|-> = |1>

    """
    state_test_p = One()  # |->
    circuit = Circuits(state_init=Minus())
    H_gate = HGate()
    circuit.add_single_qubit_gate(H_gate, 0)
    state_final = circuit.run_circuit()
    assert np.sum(state_final.get_state() - state_test_p.get_state()) < 10e-10


test_run_one_wire()

#     raise NotImplementedError


def test_run_one_qubit_two_wires():
    """
    Test the run_circuits method on a few cases:

    H⊗I|11> = |-1>

    H⊗H|00> = |++>, added as two different states
    """

    state_test_p1 = States(N=2, state=1 / np.sqrt(2) * np.array([0, 1, 0, -1]))  # |-1>
    state_init_11 = States(N=2, state=np.array([0, 0, 0, 1]))
    circuit = Circuits(N_wires=2, state_init=state_init_11)
    H_gate = HGate()
    circuit.add_single_qubit_gate(H_gate, 0)
    state_final = circuit.run_circuit()

    assert (state_final.get_state() == state_test_p1.get_state()).all()

    state_test_pp = States(N=2, state=1 / 2 * np.array([1, 1, 1, 1]))  # |++>
    state_init_00 = States(N=2, state=np.array([1, 0, 0, 0]))
    circuit = Circuits(N_wires=2, state_init=state_init_00)
    circuit.add_single_qubit_gate(H_gate, 0)
    circuit.add_single_qubit_gate(H_gate, 1)
    state_final_2 = circuit.run_circuit()

    assert (
        np.abs(np.sum(state_final_2.get_state() - state_test_pp.get_state())) < 10e-10
    )  # floating point junk


def test_run_two_qubit_two_wires():
    """
    Test the run_curcuits method on a few cases:

    CNOT|10> = |11>

    """
    state_to_check = States(N=2, state=np.array([0, 0, 0, 1]))
    state_init = States(N=2, state=np.array([0, 0, 1, 0]))
    circuit = Circuits(N_wires=2, state_init=state_init)
    CNOT = CNOTGate2(control=1)
    circuit.add_two_qubit_gate(CNOT, [0, 1])
    state_final = circuit.run_circuit()

    assert (state_final.get_state() == state_to_check.get_state()).all()


def test_prepare_bell():
    """
    Construct the Bell state by running run_curcuits method on a few cases:

    (CNOT_12)(H⊗I)|00> = (|00> + |11>)/sqrt(2)
    """

    state_to_check = PhiPlus()
    H_gate = HGate()
    CNOT = CNOTGate2(control=1)
    state_init = States(N=2, state=np.array([1, 0, 0, 0]))
    circuit = Circuits(N_wires=2, state_init=state_init)

    circuit.add_single_qubit_gate(H_gate, 0)
    circuit.add_two_qubit_gate(CNOT, [0, 1])

    final_state = circuit.run_circuit()

    assert np.abs(np.sum(final_state.get_state() - state_to_check.get_state())) < 10e-10


def test_getfinal_isnonetype():
    """
    Asserts that if measurement is not run, the get_state_final is a nonetype
    """
    circuit = Circuits()
    assert circuit.get_state_final() is None


def test_runcircuit_identity():
    """
    Tests whether adding no gates to the circuit will still run the circuit for N = 1 or
    2 wires
    """
    circuit = Circuits()
    circuit.run_circuit()  # passing no gates to the circuit
    state_tocheck = np.array([1, 0]).reshape(-1, 1)
    assert (circuit.get_state_final() == state_tocheck).all()

    circuit = Circuits(N_wires=2, state_init=States(N=2, state=tp([1, 0], [1, 0])))
    circuit.run_circuit()
    state_tocheck = np.array([1, 0, 0, 0]).reshape(-1, 1)
    assert (circuit.get_state_final() == state_tocheck).all()


def test_circuit_ran_flag():
    """
    Tests if the circuit is ran flag changes form False to True after running the circuit
    """
    circuit = Circuits()
    assert circuit.circuit_ran == False
    circuit.run_circuit()
    assert circuit.circuit_ran == True


def test_measurement_collapse_one_wire():
    """
    Asserts the final measurement outcome after appying X|0>=|1>
    """
    # construct initial states
    state_init = States()
    state_tocheck = States(1, np.array([0, 1]))
    # construct circuit
    circuit = Circuits()
    circuit.add_single_qubit_gate(XGate())
    # run and measure
    circuit.run_circuit()
    outcome = circuit.measure_qubits()
    assert (state_tocheck.get_state() == outcome.get_state()).all()


def test_measurement_collapse_two_wires():
    """
    Asserts the final measurement outcome after appying CNOT|11>=|10> is |10>
    """
    # construct initial state
    state_init = States(2, np.array([0, 0, 0, 1]))
    state_tocheck = States(2, np.array([0, 0, 1, 0]))
    # construct circuit
    circuit = Circuits(N_wires=2, state_init=state_init)
    circuit.add_two_qubit_gate(CNOTGate2(control=1), [0, 1])
    # run and measure
    circuit.run_circuit()
    outcome = circuit.measure_qubits()
    assert (state_tocheck.get_state() == outcome.get_state()).all()


def test_seed():
    """
    Asserts random seed can be set for measurement outcomes

    Runs circuit H|0> = |+> gives the same measurement outcome for a particular seed

    """
    seed = 1

    # construct circuit
    circuit = Circuits()
    circuit.add_single_qubit_gate(HGate())

    circuit.run_circuit()
    state_init = circuit.measure_qubits(seed=seed).get_state()

    # run 100 shots with the same seed to ensure the outcome is identical

    for i in range(100):
        circuit = Circuits()
        circuit.add_single_qubit_gate(HGate())
        circuit.run_circuit()
        state_tocheck = circuit.measure_qubits(seed=seed).get_state()
        assert (state_init == state_tocheck).all()
