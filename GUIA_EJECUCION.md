# Guía de ejecución — TFG Quantum Computing

## 1. Entorno

Activar el entorno virtual antes de cualquier ejecución:

```bash
source .venv/bin/activate
```

Lanzar JupyterLab:

```bash
jupyter lab
```

---

## 2. Autenticación con IBM Quantum

Las credenciales ya están guardadas localmente. **No es necesario autenticarse en cada sesión.**

Para verificar que las credenciales están disponibles:

```bash
python authentication/verify_credentials.py
```

Si por algún motivo las credenciales se pierden (cambio de máquina, reinstalación), ejecutar:

```bash
python authentication/save_credentials.py
```

En los notebooks, el servicio se carga automáticamente con:

```python
from qiskit_ibm_runtime import QiskitRuntimeService
service = QiskitRuntimeService()
```

El backend se selecciona dinámicamente con `least_busy()`, no hace falta especificarlo a mano.

---

## 3. Tipos de ejecución

Hay dos tipos de notebooks según cómo gestionan el hardware real:

### Tipo A — Flag `RUN_ON_REAL_HW` (módulos de IA)

Los notebooks cuánticos de IA tienen una variable de configuración en la segunda celda:

```python
RUN_ON_REAL_HW = False   # True -> ejecuta en IBM Quantum tras el entrenamiento
```

- **`False`** (por defecto): entrena y evalúa solo en simulador Aer. Rápido, sin cola.
- **`True`**: tras el entrenamiento en simulador, envía el circuito a IBM Quantum para inferencia. Requiere conexión y puede implicar espera en cola.

Afecta a estos notebooks:
| Notebook | Variable | Comportamiento con True |
|----------|----------|------------------------|
| `ai/classification/quantum/vqc.ipynb` | `RUN_ON_REAL_HW` | Inferencia VQC en IBM Quantum |
| `ai/kernel_classification/quantum/qksvm.ipynb` | `RUN_ON_REAL_HW` | Calcula demo del kernel (10 pts) en IBM Quantum |
| `ai/neural_network/quantum/qnn.ipynb` | `RUN_ON_REAL_HW` | Inferencia QNN en IBM Quantum |

### Tipo B — Variable `REAL_MAX_N` (módulos de criptografía)

Los notebooks de criptografía no tienen flag booleano; controlan el hardware real mediante un límite numérico:

```python
REAL_MAX_N = 5    # Grover: ejecuta en HW real para n <= 5; poner 0 para saltar todo HW real
REAL_MAX_N = 35   # Shor:   ejecuta en HW real para N <= 35; poner 0 para saltar todo HW real
```

- **`REAL_MAX_N = 0`**: solo simulación, sin hardware real.
- **Valor actual**: ejecuta los casos pequeños en IBM Quantum y el resto en simulador.

Afecta a:
| Notebook | Variable | Límite actual |
|----------|----------|---------------|
| `cryptography/brute_force/real_grover_comparison.ipynb` | `REAL_MAX_N` | 5 (n ≤ 5) |
| `cryptography/factoring/real_shor_comparison.ipynb` | `REAL_MAX_N` | 35 (N ≤ 35) |

---

## 4. Ejecución de cada módulo

Todos los notebooks están diseñados para ejecutarse de arriba a abajo con **Kernel → Restart & Run All** (o `Run All Cells`). No hay dependencias entre módulos.

### cryptography/brute_force

```
real_grover_comparison.ipynb   <- único archivo, ejecutar completo
```

Tiempo estimado: ~2 min (solo simulación) / ~5-10 min (con HW real, según cola).

### cryptography/factoring

```
real_shor_comparison.ipynb     <- único archivo, ejecutar completo
```

Tiempo estimado: ~5 min (solo simulación) / ~10-15 min adicionales (con HW real).

### ai/classification

Orden de ejecución:

```
1. classical/svm.ipynb          -> genera svm_results.json (y svm_results_4f.json si N_FEATURES=4)
2. quantum/vqc.ipynb            -> genera vqc_results.json
3. comparison/comparison.ipynb  -> lee ambos JSON y genera los plots
```

Tiempo estimado: svm ~1 s / vqc ~5 min (sim) o ~8 min (con HW real) / comparison ~5 s.

### ai/kernel_classification

Orden de ejecución:

```
1. classical/svm.ipynb          -> genera svm_results.json
2. quantum/qksvm.ipynb          -> genera qksvm_results.json
3. comparison/comparison.ipynb  -> lee ambos JSON y genera los plots
```

Tiempo estimado: svm ~1 s / qksvm ~15 s (sim) o ~1-2 min (con HW real, demo 10 pts) / comparison ~5 s.

### ai/neural_network

Orden de ejecución:

```
1. classical/mlp.ipynb          -> genera mlp_results.json (y mlp_results_4f.json si N_FEATURES=4)
2. quantum/qnn.ipynb            -> genera qnn_results.json
3. comparison/comparison.ipynb  -> lee ambos JSON y genera los plots
```

Tiempo estimado: mlp ~1 s / qnn ~30 s (sim, multi-start x5) o ~5 min (con HW real) / comparison ~5 s.

---

## 5. Experimento con 4 características

Los notebooks clásicos y cuánticos de IA tienen una variable `N_FEATURES` en la celda de configuración:

```python
N_FEATURES = 2   # 2 o 4
```

Para regenerar los resultados con 4 características: cambiar a `N_FEATURES = 4`, ejecutar el notebook y volver a `N_FEATURES = 2`. Los archivos JSON de 4 características tienen el sufijo `_4f` (`svm_results_4f.json`, etc.). El notebook de comparación los carga automáticamente si existen.

---

## 6. Consideraciones sobre el Plan Open de IBM

- **Límite**: 10 minutos de QPU al mes.
- El hardware real ya está ejecutado en todos los módulos; los resultados están guardados en los JSON.
- Si se re-ejecuta con `RUN_ON_REAL_HW = True` o `REAL_MAX_N > 0`, se consumirá tiempo del plan mensual.
- Los notebooks de IA con `RUN_ON_REAL_HW = False` no consumen tiempo de QPU aunque estén ejecutados.
- El notebook de comparación (`comparison.ipynb`) nunca usa hardware real, solo lee los JSON.
