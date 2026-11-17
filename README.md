# CC-QC-Comparison

A comparison between classical and quantum computing, developed as part of the Bachelor's Thesis (TFG) **"Quantum Artificial Intelligence"**.

This repository contains the thesis experiments: each quantum algorithm is implemented alongside its classical counterpart, and the results, running times and scalability are compared. Experiments run on a simulator (Qiskit Aer) and, for small cases, on real quantum hardware (IBM Quantum).

## Thesis background

The thesis introduces quantum computing and its relationship with artificial intelligence algorithms. It covers qubits, superposition, entanglement and the quantum computing model, reviews representative quantum algorithms, and studies quantum machine learning proposals. It then compares their potential with classical approaches and discusses open challenges and future research directions.

## Experiments

### Cryptography (`cryptography/`)

| Experiment | Comparison | Notebook |
|---|---|---|
| Brute-force search | Grover's algorithm vs. linear and binary search | `cryptography/brute_force/real_grover_comparison.ipynb` |
| Integer factoring | Shor's algorithm vs. trial division and Pollard's Rho | `cryptography/factoring/real_shor_comparison.ipynb` |

### Artificial intelligence (`ai/`)

Each module has three parts: a classical implementation (`classical/`), a quantum one (`quantum/`) and a comparison notebook (`comparison/`).

| Module | Classical | Quantum |
|---|---|---|
| `ai/classification` | SVM | Variational Quantum Classifier (VQC) |
| `ai/kernel_classification` | SVM with classical kernel | SVM with quantum kernel (QKSVM) |
| `ai/neural_network` | Multilayer Perceptron (MLP) | Quantum Neural Network (QNN) |

### Authentication (`authentication/`)

Scripts to save and verify your IBM Quantum credentials.

## Repository structure

```
CC-QC-Comparison/
├── ai/
│   ├── classification/
│   │   ├── classical/        svm.ipynb
│   │   ├── quantum/          vqc.ipynb
│   │   └── comparison/       comparison.ipynb
│   ├── kernel_classification/
│   │   ├── classical/        svm.ipynb
│   │   ├── quantum/          qksvm.ipynb
│   │   └── comparison/       comparison.ipynb
│   └── neural_network/
│       ├── classical/        mlp.ipynb
│       ├── quantum/          qnn.ipynb
│       └── comparison/       comparison.ipynb
├── authentication/           save_credentials.py, verify_credentials.py
├── cryptography/
│   ├── brute_force/          real_grover_comparison.ipynb
│   └── factoring/            real_shor_comparison.ipynb
├── EXECUTION_GUIDE.md        Detailed execution guide (English)
├── GUIA_EJECUCION.md         Detailed execution guide (Spanish)
├── contexto_tfg.md           Thesis context and status (in Spanish)
├── commands.txt
├── hello_world.ipynb
├── quickstart.ipynb
└── .gitignore
```

## Technologies

- Python
- [Qiskit](https://qiskit.org/) (main quantum framework)
- Qiskit Aer (simulator)
- Qiskit IBM Runtime / IBM Quantum (real hardware)
- JupyterLab

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/peri21/CC-QC-Comparison.git
   cd CC-QC-Comparison
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # On Windows: .venv\Scripts\activate
   ```

3. Install the dependencies (adjust this line to match your `requirements.txt`, if you add one):

   ```bash
   pip install qiskit qiskit-aer qiskit-ibm-runtime qiskit-machine-learning scikit-learn jupyterlab matplotlib numpy
   ```

4. Set up your IBM Quantum credentials (only needed once):

   ```bash
   python authentication/save_credentials.py
   python authentication/verify_credentials.py
   ```

   You need a free [IBM Quantum](https://quantum.cloud.ibm.com/) account and your own API key.

## Usage

> For the full step-by-step instructions on running every experiment, see the **[Execution Guide](EXECUTION_GUIDE.md)**. What follows is a short summary.

Start JupyterLab:

```bash
jupyter lab
```

Open the notebook you want and run it from top to bottom with **Kernel > Restart & Run All**. The modules are independent of each other.

### Execution order in the AI modules

In each folder under `ai/`, run the notebooks in this order, because the comparison reads the results of the previous ones:

1. The classical notebook (writes a `.json` results file).
2. The quantum notebook (writes another `.json` file).
3. The notebook in `comparison/` (reads both and generates the plots).

### Simulator or real quantum hardware

- **AI modules:** the `RUN_ON_REAL_HW` variable (second cell) is `False` by default, so everything runs on the simulator. With `True`, after training on the simulator the inference is sent to IBM Quantum.
- **Cryptography modules:** the `REAL_MAX_N` variable sets the largest problem size run on real hardware (5 for Grover, 35 for Shor). Set it to `0` to use the simulator only.
- **Four-feature experiment:** change `N_FEATURES` from `2` to `4`, run the notebook, then set it back to `2`. Results are saved with the `_4f` suffix.
