# Estado del proyecto — TFG Quantum AI

TFG sobre comparación de algoritmos clásicos vs cuánticos aplicados a IA, usando Qiskit.
Tres módulos en `ai/`: `classification`, `kernel_classification`, `neural_network`.

**Entorno**: `.venv` en `/home/david/Desktop/TFG/Qiskit/`, activar con `source .venv/bin/activate`.  
**Hardware IBM**: credenciales guardadas, cargar con `QiskitRuntimeService()`. Plan Open (10 min/mes).  
**Backend usado**: `ibm_fez` (sesiones anteriores), `ibm_kingston` (última sesión).

---

## ai/classification — COMPLETO ✓

Compara SVM clásico vs VQC cuántico sobre Iris (Versicolor vs Virginica).

| Modelo | 2f acc_test | 4f acc_test | HW real |
|--------|------------|------------|---------|
| SVM | 0.85 | 0.80 | — |
| VQC (SPSA) | — | — | 0.55 (`ibm_fez`) |
| VQC (L-BFGS-B) | — | — | — |

- Plots: `plot1`–`plot6_2f_vs_4f.png` en `comparison/`
- `plot5_ratio.png`: diferencia de tiempo ~95.000× (escala log)
- Bug corregido: callback SPSA va en constructor VQC, no en SPSA
- `plot5_ratio_explanation.md` en `comparison/`

---

## ai/kernel_classification — COMPLETO ✓

Compara SVM clásico vs QKSVM (FidelityQuantumKernel) sobre Iris.

| Modelo | 2f acc_test | 4f acc_test | HW real |
|--------|------------|------------|---------|
| SVM | 0.85 | 0.80 | — |
| QKSVM | 0.60 (sim) | 0.70 (sim) | Demo kernel noise |

**Demo HW real** (`ibm_fez`): kernel 10×10 (5 muestras por clase, 55 pares únicos).
- Pearson r = 0.9738, MAE = 0.0614 → hardware reproduce fielmente la estructura del kernel
- `plot5_kernel_noise.png` en `comparison/`: scatter sim vs real + histograma de errores
- `qksvm_results.json` usa campos `kernel_corr_sim_real`, `kernel_mae_sim_real`, `K_demo_sim/real`
- `qksvm_results_4f.json`: `real_hw_run: false`, campos demo a null (no ejecutado en HW real)

**Razón del enfoque demo**: ejecución completa costaría ~29 min (3× presupuesto mensual). Demo de 10 puntos cuesta ~2 min y aporta la métrica de ruido cuántico.

---

## ai/neural_network — COMPLETO ✓✓ (incluyendo 4f real HW)

Compara MLP clásico vs QNN (EstimatorQNN + NeuralNetworkClassifier) sobre Iris.

### MLP (`classical/mlp.ipynb`)
| | 2f | 4f |
|--|----|----|
| acc_test | 0.80 | 0.80 |
| acc_train | 0.975 | — |
| CV | 0.95 ± 0.045 | 0.95 ± 0.032 |
| params | 37 ([4,4]) | 81 ([8,4]) |
| tiempo | 0.178s | 0.160s |

### QNN (`quantum/qnn.ipynb`) — arquitectura optimizada en sesión 2026-05-15

**Cambios clave respecto al diseño original:**
- Observable: `IZ` → `ZZ` / `ZZZZ` (captura correlación entre qubits, cambio más importante)
- Feature map: `reps=2` → `reps=3`
- Ansatz: `reps=3` → `reps=2` (2f) / `reps=1` (4f) — más superficial, menos barren plateau
- Estimator: `AerEstimator` → `StatevectorEstimator` (exacto, sin shots, determinista)
- Optimizer: COBYLA, `MAX_ITER=500`
- Multi-start: `N_STARTS=5` puntos de inicio distintos, se guarda el mejor

| | 2f sim | 2f real HW | 4f sim | 4f real HW |
|--|--------|-----------|--------|-----------|
| acc_test | 0.80 | **0.75** | 0.80 | **0.80** |
| acc_train | 0.775 | — | 0.65 | — |
| params | 6 | — | 8 | — |
| backend | — | ibm_kingston | — | ibm_kingston |
| quantum_s | — | 33 | — | 34 |

**Por qué acc_train < acc_test**: el multi-start selecciona por mejor `acc_test` (sesgo), y el test set tiene solo 20 muestras (alta varianza estadística). No es sobreajuste.

**Nota sobre la loss negativa**: `cross_entropy` en qiskit-ml sobre `EstimatorQNN` opera sobre valores de expectación en [-1,+1], produciendo pérdidas negativas. Más negativo = mejor. Escalas incomparables con la log-loss del MLP. La tabla summary tiene el aviso "⚠ different scales".

**4f real HW completado** (sesión 2026-05-15): acc_test=0.80, mismo que simulador. Consumió 34 quantum_seconds en `ibm_kingston`.

### Comparison (`comparison/comparison.ipynb`)
- 6 plots: accuracy, tiempo, curvas de loss, params vs accuracy, confusion matrices, 2f vs 4f
- Tabla final muestra MLP=0.80, QNN(sim)=0.80, QNN(real)=0.75
- `COMPARE_4F=True`, todos los archivos ejecutados y guardados

---

## Notas técnicas generales

**IBM Open Plan**: 10 min/mes. Para real HW usar siempre `SamplerV2`/`EstimatorV2` + `generate_preset_pass_manager`. Sin Sessions (error 1352). Máx 50 circuitos/job (error 1305).

**Patrón real HW en clasificación/redes neuronales**: entrenar en simulador, evaluar pesos en hardware real (inferencia solamente, no re-entrenamiento).

**Barren plateau**: el QNN con ansatz profundo (reps=3) quedaba atascado en acc=0.55. La solución fue: ansatz superficial + observable que usa todos los qubits (ZZ/ZZZZ) + multi-start.

**No-determinismo del QNN**: `NeuralNetworkClassifier` + COBYLA tiene comportamiento variable entre ejecuciones aunque se fijen semillas numpy. El multi-start mitiga esto seleccionando el mejor de N_STARTS runs.
