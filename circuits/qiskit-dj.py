from qiskit import QuantumCircuit, Aer, transpile, assemble
from qiskit.visualization import plot_histogram
import random
import numpy as np

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

    qc = qr.compose(qc_oracle)

    qc.h(0)
    qc.measure(0, 0)

    return qc

oracle_type, qc_oracle = random_oracle()
qc = deutsch_jozsa_circuit(oracle_type, qc_oracle)

print(f"Generated {oracle_type} oracle.")
print("Deutsch-Jozsa circuit:")
print(qc)

backend = Aer.get_backend('qasm_simulator')
t_qc = transpile(qc, backend)
result = backend.run(t_qc, shots=5).result()

counts = result.get_counts()

if '1' in counts and counts['1'] == 5:
    print("\nFunction is balanced.")
else:
    print("\nFunction is constant.")


