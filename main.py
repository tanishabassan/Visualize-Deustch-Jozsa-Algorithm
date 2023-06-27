from flask import Flask, render_template, request, jsonify
import random
import json
from deustch_jozsa_demo import run_deustch_jozsa_cirq, run_deustch_jozsa_qiskit, run_deustch_jozsa_pennylane

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/run_deustch_jozsa", methods=["POST"])
def run_deustch_jozsa():
    sdk = request.form.get("sdk")
    if sdk == "cirq":
        result = run_deustch_jozsa_cirq()
    if sdk == "qiskit":
        result = run_deustch_jozsa_qiskit()
    if sdk == "pennylane":
        result = run_deustch_jozsa_pennylane()

    return jsonify(result)
  
if __name__ == "__main__":
  from waitress import serve
  serve(app, host="0.0.0.0", port=8080)
