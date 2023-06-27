# Import necessary libraries
import cirq
import numpy as np
import random

# Define a random oracle (either constant or balanced)
def random_oracle(qubits):
    oracle_type = random.choice(["constant", "balanced"])
    oracle_gate = []
    
    if oracle_type == "balanced":
        # Flip qubits[1] based on the value of qubits[0] (balanced)
        oracle_gate.append(cirq.CNOT(qubits[0], qubits[1]))
    else:
        # Apply Identity (I) to qubits[0] to create a constant oracle
        oracle_gate.append(cirq.I(qubits[0]))
    
    return oracle_type, oracle_gate

# Function to create the Deutsch-Jozsa circuit
def deutsch_jozsa_circuit(oracle_type, oracle_gate):
    qr = [cirq.LineQubit(i) for i in range(2)]
    circuit = cirq.Circuit()
    
    circuit.append(cirq.X(qr[1]))
    circuit.append([cirq.H(qr[0]), cirq.H(qr[1])])

    circuit.append(oracle_gate)

    circuit.append(cirq.H(qr[0]))
    circuit.append(cirq.measure(qr[0], key="result"))

    return circuit

# Generate a random oracle and construct the corresponding Deutsch-Jozsa circuit
oracle_type, oracle_gate = random_oracle(cirq.LineQubit.range(2))
circuit = deutsch_jozsa_circuit(oracle_type, oracle_gate)

print(f"Generated {oracle_type} oracle.")
print("Deutsch-Jozsa circuit:")
print(circuit)

# Run the circuit using cirq's simulator
simulator = cirq.Simulator()
result = simulator.run(circuit, repetitions=5)

# Analyze the results
output = "Function is "
if np.all(result.measurements["result"] == 1):  # If we measure 1, the function is balanced
    output += "balanced."
else:  # If we measure 0, the function is constant
    output += "constant."

print("\n" + output)