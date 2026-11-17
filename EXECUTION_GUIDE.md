# Execution Guide

## 1. Environment

Activate the virtual environment (`.venv`) before running anything:

```bash
source .venv/bin/activate
```

Launch JupyterLab:

```bash
jupyter lab
```

## 2. IBM Quantum credentials

Credentials are already saved locally, so you do not need to authenticate in every session.

- **Verify** that the credentials are available:

  ```bash
  python authentication/verify_credentials.py
  ```

- **Save them again** if they are lost (for example, after changing machines or reinstalling):

  ```bash
  python authentication/save_credentials.py
  ```

- **In notebooks**, the service loads automatically:

  ```python
  from qiskit_ibm_runtime import QiskitRuntimeService
  service = QiskitRuntimeService()
  ```

The backend is chosen automatically with `least_busy()`, so you do not need to specify it manually.

## 3. Hardware execution modes

### Type A: `RUN_ON_REAL_HW` flag (AI modules)

Set in the second cell of the notebook:

```python
RUN_ON_REAL_HW = False   # True -> runs on IBM Quantum after training
```

- `False` (default): trains and evaluates only on the Aer simulator. Fast, with no queue.
- `True`: after training on the simulator, the circuit is sent to IBM Quantum for inference. Requires a connection and may involve waiting in a queue.

| Notebook | With `True` |
|---|---|
| `ai/classification/quantum/vqc.ipynb` | VQC inference on IBM Quantum |
| `ai/kernel_classification/quantum/qksvm.ipynb` | Kernel demo (10 points) on IBM Quantum |
| `ai/neural_network/quantum/qnn.ipynb` | QNN inference on IBM Quantum |

### Type B: `REAL_MAX_N` variable (cryptography modules)

A numeric limit instead of a boolean:

```python
REAL_MAX_N = 5    # Grover: real hardware for n <= 5; set 0 to skip all real hardware
REAL_MAX_N = 35   # Shor:   real hardware for N <= 35; set 0 to skip all real hardware
```

- `0`: simulation only.
- Current values: small cases run on IBM Quantum, the rest on the simulator.

| Notebook | Current limit |
|---|---|
| `cryptography/brute_force/real_grover_comparison.ipynb` | 5 (n ≤ 5) |
| `cryptography/factoring/real_shor_comparison.ipynb` | 35 (N ≤ 35) |

## 4. Running each experiment

All notebooks run from top to bottom with **Kernel > Restart & Run All** (or **Run All Cells**). The modules do not depend on each other, but the notebooks inside each AI folder must be run in the order listed below.

### Cryptography

- `cryptography/brute_force/real_grover_comparison.ipynb`: run the whole file. About 2 min in simulation, or 5 to 10 min with real hardware, depending on the queue.
- `cryptography/factoring/real_shor_comparison.ipynb`: run the whole file. About 5 min in simulation, plus 10 to 15 min with real hardware.

### AI: classification (`ai/classification`)

1. `classical/svm.ipynb` writes `svm_results.json` (and `svm_results_4f.json` if `N_FEATURES=4`).
2. `quantum/vqc.ipynb` writes `vqc_results.json`.
3. `comparison/comparison.ipynb` reads both JSON files and generates the plots.

Approximate times: SVM ~1 s, VQC ~5 min (simulator) or ~8 min (real hardware), comparison ~5 s.

### AI: kernel classification (`ai/kernel_classification`)

1. `classical/svm.ipynb` writes `svm_results.json`.
2. `quantum/qksvm.ipynb` writes `qksvm_results.json`.
3. `comparison/comparison.ipynb` reads both and generates the plots.

Approximate times: SVM ~1 s, QKSVM ~15 s (simulator) or 1 to 2 min (real hardware, 10-point demo), comparison ~5 s.

### AI: neural network (`ai/neural_network`)

1. `classical/mlp.ipynb` writes `mlp_results.json` (and `mlp_results_4f.json` if `N_FEATURES=4`).
2. `quantum/qnn.ipynb` writes `qnn_results.json`.
3. `comparison/comparison.ipynb` reads both and generates the plots.

Approximate times: MLP ~1 s, QNN ~30 s (simulator, multi-start x5) or ~5 min (real hardware), comparison ~5 s.

## 5. Four-feature experiment

The classical and quantum AI notebooks have an `N_FEATURES` variable in the configuration cell:

```python
N_FEATURES = 2   # 2 or 4
```

To regenerate the 4-feature results, set `N_FEATURES = 4`, run the notebook, then set it back to `2`. The 4-feature JSON files use the `_4f` suffix (for example, `svm_results_4f.json`). The comparison notebook loads them automatically if they exist.

## 6. IBM Open Plan limits

- The limit is **10 minutes of QPU time per month**.
- The real-hardware runs are already saved in the JSON files.
- Re-running with `RUN_ON_REAL_HW = True` or `REAL_MAX_N > 0` consumes monthly QPU time.
- AI notebooks with `RUN_ON_REAL_HW = False` use no QPU time, even when executed.
- `comparison.ipynb` never uses real hardware; it only reads the JSON files.
