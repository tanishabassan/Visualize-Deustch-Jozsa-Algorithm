import pennylane as qml
from pennylane import numpy as np
import random

def random_oracle():
    oracle_type = random.choice(["constant", "balanced"])

    def oracle(q):
        if oracle_type == "balanced":
            qml.CNOT(wires=[0, 1])
        else:
            pass  # Identity is the default operation, so no need to add anything

    return oracle_type, oracle

def deutsch_jozsa_circuit(oracle):
    # Initialize quantum and classical registers
    dev = qml.device('default.qubit', wires=2, shots=5)

    @qml.qnode(dev)
    def qcircuit():
        # Initialize state |1> for the second qubit
        qml.PauliX(wires=1)

        # Apply Hadamard gates to both qubits
        qml.Hadamard(wires=0)
        qml.Hadamard(wires=1)

        oracle(qml)

        # Apply Hadamard gate to the first qubit and measure it
        qml.Hadamard(wires=0)
        return qml.sample(qml.PauliZ(0))

    return qcircuit

oracle_type, oracle = random_oracle()
qc = deutsch_jozsa_circuit(oracle)

print(f"Generated {oracle_type} oracle.")
print("Deutsch-Jozsa circuit:")

# Draw the circuit using qml.draw
print(qml.draw(qc)())

result = qc()

if np.all(result == -1):
    print("\nFunction is balanced.")
else:
    print("\nFunction is constant.")