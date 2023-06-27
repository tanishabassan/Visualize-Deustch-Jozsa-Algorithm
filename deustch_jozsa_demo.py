import cirq
import numpy as np
import random
import pennylane as qml
from pennylane import numpy as np
from qiskit import QuantumCircuit, Aer, transpile, assemble
from qiskit.visualization import plot_histogram
from io import StringIO
from qiskit.providers.aer import Aer
from qiskit import execute
from qiskit.visualization import circuit_drawer

# cirq implementation
def run_deustch_jozsa_cirq():
    def random_oracle(qubits):
        oracle_type = random.choice(["constant", "balanced"])
        oracle_gate = []

        if oracle_type == "balanced":
            oracle_gate.append(cirq.CNOT(qubits[0], qubits[1]))
        else:
            oracle_gate.append(cirq.I(qubits[0]))

        return oracle_type, oracle_gate

    def deutsch_jozsa_circuit(oracle_type, oracle_gate):
        qr = [cirq.LineQubit(i) for i in range(2)]
        circuit = cirq.Circuit()

        circuit.append(cirq.X(qr[1]))
        circuit.append([cirq.H(qr[0]), cirq.H(qr[1])])

        circuit.append(oracle_gate)

        circuit.append(cirq.H(qr[0]))
        circuit.append(cirq.measure(qr[0], key="result"))

        return circuit

    oracle_type, oracle_gate = random_oracle(cirq.LineQubit.range(2))
    circuit = deutsch_jozsa_circuit(oracle_type, oracle_gate)

    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=5)

    output = "Function is "
    if np.all(result.measurements["result"] == 1):
        output += "balanced."
    else:
        output += "constant."

    code_output = '''
def random_oracle(qubits):
    oracle_type = random.choice(["constant", "balanced"])
    oracle_gate = []

    if oracle_type == "balanced":
        oracle_gate.append(cirq.CNOT(qubits[0], qubits[1]))
    else:
        oracle_gate.append(cirq.I(qubits[0]))

    return oracle_type, oracle_gate

def deutsch_jozsa_circuit(oracle_type, oracle_gate):
    qr = [cirq.LineQubit(i) for i in range(2)]
    circuit = cirq.Circuit()

    circuit.append(cirq.X(qr[1]))
    circuit.append([cirq.H(qr[0]), cirq.H(qr[1])])

    circuit.append(oracle_gate)

    circuit.append(cirq.H(qr[0]))
    circuit.append(cirq.measure(qr[0], key="result"))

    return circuit
'''

    return {
        "code": code_output,
        "circuit": str(circuit),
        "output": output
    }

# pennylane implementation

def run_deustch_jozsa_pennylane():
    def random_oracle():
        oracle_type = random.choice(["constant", "balanced"])

        def oracle(q):
            if oracle_type == "balanced":
                qml.CNOT(wires=[0, 1])
            else:
                pass

        return oracle_type, oracle

    def deutsch_jozsa_circuit(oracle):
        dev = qml.device('default.qubit', wires=2, shots=5)

        @qml.qnode(dev)
        def qcircuit():
            qml.PauliX(wires=1)
            qml.Hadamard(wires=0)
            qml.Hadamard(wires=1)

            oracle(qml)

            qml.Hadamard(wires=0)
            return qml.sample(qml.PauliZ(0))

        return qcircuit

    oracle_type, oracle = random_oracle()
    qc = deutsch_jozsa_circuit(oracle)

    result = qc()
    output = "Function is "
    if np.all(result == -1):
        output += "balanced."
    else:
        output += "constant."

    code_output = '''
def random_oracle():
    oracle_type = random.choice(["constant", "balanced"])

    def oracle(q):
        if oracle_type == "balanced":
            qml.CNOT(wires=[0, 1])
        else:
            pass

    return oracle_type, oracle

def deutsch_jozsa_circuit(oracle):
    dev = qml.device('default.qubit', wires=2, shots=5)

    @qml.qnode(dev)
    def qcircuit():
        qml.PauliX(wires=1)
        qml.Hadamard(wires=0)
        qml.Hadamard(wires=1)

        oracle(qml)

        qml.Hadamard(wires=0)
        return qml.sample(qml.PauliZ(0))

    return qcircuit
'''

    return {
        "code": code_output,
        "circuit": qml.draw(qc)(),
        "output": output
    }


# qiskit implementation
def run_deustch_jozsa_qiskit():
    def random_oracle():
        oracle_type = random.choice(["constant", "balanced"])
        qc_oracle = QuantumCircuit(2)

        if oracle_type == "balanced":
            qc_oracle.cx(0, 1)
        else:
            pass  # Identity is the default operation, so no need to add anything

        return oracle_type, qc_oracle

    def deutsch_jozsa_circuit(oracle_type, qc_oracle):
        qr = QuantumCircuit(2, 1)
    
        qr.x(1)
        qr.h([0, 1])
    
        # Use the compose method to combine qr with qc_oracle
        qc = qr.compose(qc_oracle)
    
        qc.h(0)
        qc.measure(0, 0)
    
        return qc

    oracle_type, qc_oracle = random_oracle()
    qc = deutsch_jozsa_circuit(oracle_type, qc_oracle)

    backend = Aer.get_backend('qasm_simulator')

    # Replace `assemble`, `backend.run` with `execute` function
    result = execute(qc, backend, shots=5).result()
    counts = result.get_counts()

    output = "Function is "
    if '1' in counts and counts['1'] == 5:
        output += "balanced."
    else:
        output += "constant."

    code_output = '''
def random_oracle():
    oracle_type = random.choice(["constant", "balanced"])
    qc_oracle = QuantumCircuit(2)

    if oracle_type == "balanced":
        qc_oracle.cx(0, 1)
    else:
        pass

    return oracle_type, qc_oracle

def deutsch_jozsa_circuit(oracle_type, qc_oracle):
    qr = QuantumCircuit(2, 1)
    
    qr.x(1)
    qr.h([0, 1])
    
    # Use the compose method to combine qr with qc_oracle
    qc = qr.compose(qc_oracle)
    
    qc.h(0)
    qc.measure(0, 0)
    
    return qc
'''

    # Use StringIO to capture the output of the draw method and convert to a string
    qiskit_drawing_string = str(circuit_drawer(qc, output='text', fold=100))

    return {
        "code": code_output,
        "circuit": qiskit_drawing_string,
        "output": output
    }