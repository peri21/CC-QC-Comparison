# Estado del proyecto — TFG Quantum Computing

**Entorno**: `.venv` en `/home/david/Desktop/TFG/Qiskit/`, activar con `source .venv/bin/activate`.  
**Hardware IBM**: credenciales guardadas, cargar con `QiskitRuntimeService()`. Plan Open (10 min/mes).

---

## cryptography/brute_force — COMPLETADO ✓

Archivo único: `real_grover_comparison.ipynb`.

Compara búsqueda lineal y binaria (clásicas) vs algoritmo de Grover (cuántico) en simulación y hardware IBM real.

**Resultados** (n=2..11, real HW solo n≤5):

| n | N | Linear | Binary | Grover | Sim OK | Depth sim | Depth real | Prob real | Umbral | Real OK |
|---|---|--------|--------|--------|--------|-----------|------------|-----------|--------|---------|
| 2 | 4 | 2.8 | 2.0 | 1 | Yes | 6 | 12 | 97.4% | 50.0% | Yes |
| 3 | 8 | 4.0 | 2.0 | 2 | Yes | 10 | 169 | 80.1% | 35.4% | Yes |
| 4 | 16 | 8.8 | 5.0 | 3 | Yes | 14 | 595 | 37.0% | 25.0% | Yes |
| 5 | 32 | 8.4 | 1.0 | 4 | Yes | 18 | 1770 | 4.1% | 17.7% | **No** |
| 6 | 64 | 39.5 | 6.0 | 6 | Yes | 26 | N/A | N/A | 12.5% | N/A |
| 7 | 128 | 56.9 | 6.0 | 8 | Yes | 34 | N/A | N/A | 8.8% | N/A |
| 8 | 256 | 93.9 | 7.0 | 12 | Yes | 50 | N/A | N/A | 6.2% | N/A |
| 9 | 512 | 232.6 | 7.0 | 17 | Yes | 70 | N/A | N/A | 4.4% | N/A |
| 10 | 1024 | 408.1 | 10.0 | 25 | Yes | 102 | N/A | N/A | 3.1% | N/A |
| 11 | 2048 | 883.6 | 11.0 | 35 | Yes | 142 | N/A | N/A | 2.2% | N/A |

Nota: `linear_queries` para n=5 (8.4) es anómalamente bajo respecto al valor esperado (~16.5); es varianza muestral con RUNS=10 y no afecta a los resultados.

**Plots generados** (5): `plot1_queries.png`, `plot2_speedup.png`, `plot3_breakeven.png`, `plot4_success_prob.png`, `plot5_circuit_depth.png`

**Resumen exportado**: `grover_summary.json`

**Decisiones técnicas**:
- Umbral de éxito: `prob > 1/√N` (√N veces más probable que uniforme), no mayoría simple
- Real HW limitado a n≤5: para n=5 el circuito alcanza profundidad 1770 en hardware real (×98 sobre simulación) por descomposición MCX→CNOT + SWAPs de enrutamiento
- Backend usado: `ibm_marrakesh` (n=2..5, seleccionado por `least_busy()`)
- `SamplerV2` + `generate_preset_pass_manager(optimization_level=1)`

---

## ai/classification — COMPLETADO ✓

Tres notebooks: `classical/svm.ipynb`, `quantum/vqc.ipynb`, `comparison/comparison.ipynb`.

Compara clasificación binaria (Versicolor vs Virginica, dataset Iris) entre SVM clásico con kernel RBF y un Clasificador Cuántico Variacional (VQC) en simulación y hardware IBM real.

**Resultados** (2 features: longitud y anchura del pétalo, 80 train / 20 test):

| Modelo | Accuracy test | CV / multi-seed | Tiempo entrenamiento |
|---|---|---|---|
| SVM (clásico) | **85%** | 94.0% ± 3.7% | 0.003 s |
| VQC simulador (media 3 runs) | 63.3% ± 9.4% | — | 271 s |
| VQC simulador (run ref, seed=42) | 70% | — | — |
| VQC hardware real (ibm_marrakesh) | **70%** | — | 164 s (inferencia) |

**Experimento 4 features** (sepal + petal, todas):

| Modelo | Accuracy test | Parámetros |
|---|---|---|
| SVM 4f | 80% | — |
| VQC 4f (sim) | **50%** (azar) | 16 |

**Plots generados** (6): `plot1_accuracy.png`, `plot2_training_time.png`, `plot3_vqc_loss.png`, `plot4_confusion_matrices.png`, `plot5_ratio.png`, `plot6_2f_vs_4f.png`

**Resumen exportado**: `comparison_summary.json`

**Decisiones técnicas**:
- Dataset: solo clases 1 y 2 del Iris (Versicolor vs Virginica); clase 0 (Setosa) descartada por ser trivialmente separable
- Escalado: SVM en [0,1] (MinMaxScaler); VQC en [0,π] (× π adicional para aprovechar el rango de las puertas de rotación)
- Arquitectura VQC: `ZZFeatureMap(reps=2)` + `RealAmplitudes(reps=3)` = 8 parámetros entrenables (2 qubits)
- Optimizador SPSA (300 iter): loss estanca en ~0.73 tras ~60 iteraciones → barren plateau, comportamiento esperado en NISQ
- Multi-seed (semillas 42, 123, 7): alta varianza (±9.4%) → el modelo es sensible a la inicialización
- VQC 4f = 50% (azar): el modelo con 4 qubits y 16 parámetros no aprende nada en este dataset con SPSA
- Real HW = 70% (igual que sim): circuito de 2 qubits suficientemente superficial para sobrevivir el ruido de ibm_marrakesh
- Entrenamiento solo en simulador; inferencia en real HW para evitar colas de cientos de iteraciones
- `SamplerV2` + `generate_preset_pass_manager(optimization_level=1)`

---

## ai/kernel_classification — COMPLETADO ✓

Tres notebooks: `classical/svm.ipynb`, `quantum/qksvm.ipynb`, `comparison/comparison.ipynb`.

Compara clasificación binaria (Versicolor vs Virginica, dataset Iris) entre SVM clásico con kernel RBF y un Kernel SVM Cuántico (QKSVM) en simulación y hardware IBM real (solo análisis de ruido del kernel, no clasificación completa).

**Resultados** (2 features: longitud y anchura del pétalo, 80 train / 20 test):

| Modelo | Accuracy test | CV / notas | Tiempo total | Vectores de soporte |
|---|---|---|---|---|
| SVM (clásico) | **85%** | 94.0% ± 3.7% | 0.0016 s | 17 |
| QKSVM simulador (2 qubits) | 70% | — | 14.35 s | 48 |
| QKSVM hardware real | — | demo kernel 10 pts, Pearson r=0.9738 | 61.5 s (kernel) | — |

**Experimento 4 features** (sépalos + pétalos, todas):

| Modelo | Accuracy test |
|---|---|
| SVM 4f | 80% |
| QKSVM 4f (sim) | 65% |

Nota: la precisión del QKSVM varía entre ejecuciones (~60-70% en 2f) porque `BackendSamplerV2` con `AerSimulator` usa shots finitos sin semilla fija → varianza de ruido de muestreo en los valores del kernel.

**Plots generados** (5): `plot1_accuracy.png`, `plot2_time_breakdown.png`, `plot3_confusion_matrices.png`, `plot4_2f_vs_4f.png`, `plot5_kernel_noise.png`

**Resumen exportado**: `comparison_summary.json`

**Decisiones técnicas**:
- Dataset: solo clases 1 y 2 del Iris (Versicolor vs Virginica); clase 0 (Setosa) descartada por ser trivialmente separable
- Escalado: SVM en [0,1] (MinMaxScaler); QKSVM en [0,π] (× π adicional para aprovechar el rango de las puertas de rotación)
- Arquitectura QKSVM: `ZZFeatureMap(reps=2)`, sin parámetros entrenables; kernel = fidelidad cuántica |⟨φ(x_i)|φ(x_j)⟩|²
- Backend kernel: `FidelityQuantumKernel` + `ComputeUncompute`, `AerSimulator` para simulación
- QKSVM acumula 47 vectores de soporte vs 17 del SVM clásico → el margen en el espacio cuántico es más difícil de separar
- Tiempo dominado por kernel cuántico (99.99% del total): 20.47 s vs 0.0016 s del SVM
- Hardware real: subconjunto demo de 10 puntos (5 por clase) para análisis de ruido del kernel; kernel completo (20×80=1600 pares) requeriría ~29 min de presupuesto QPU
- `max_circuits_per_job=50` para evitar el límite por trabajo del IBM Open Plan (error 1305)
- Backend hardware usado: `ibm_fez` (seleccionado por `least_busy()`)
- `SamplerV2` + `generate_preset_pass_manager(optimization_level=1)`

---

## ai/neural_network — COMPLETADO ✓

Tres notebooks: `classical/mlp.ipynb`, `quantum/qnn.ipynb`, `comparison/comparison.ipynb`.

Compara clasificación binaria (Versicolor vs Virginica, dataset Iris) entre un Perceptrón Multicapa (MLP) clásico y una Red Neuronal Cuántica (QNN) basada en `EstimatorQNN` + `NeuralNetworkClassifier`, en simulación y hardware IBM real.

**Resultados** (2 features: longitud y anchura del pétalo, 80 train / 20 test):

| Modelo | Accuracy test | Accuracy train | Tiempo | Parámetros | HW real |
|---|---|---|---|---|---|
| MLP (clásico) | **80%** | 97.5% | 0.12 s | 37 | — |
| QNN simulador (2 qubits) | **80%** | 78.75% | ~5 s | **6** | — |
| QNN hardware real (ibm_kingston) | **75%** | — | — | 6 | ✓ |

**Experimento 4 features** (sépalos + pétalos, todas):

| Modelo | Accuracy test | Accuracy train | Parámetros |
|---|---|---|---|
| MLP 4f | **80%** | 98.75% | 81 |
| QNN 4f (sim) | **80%** | 58.75% | **8** |
| QNN 4f (ibm_kingston) | **80%** | — | 8 |

**Plots generados** (6): `plot1_accuracy.png`, `plot2_training_time.png`, `plot3_loss_curves.png`, `plot4_params_vs_accuracy.png`, `plot5_confusion_matrices.png`, `plot6_2f_vs_4f.png`

**Resumen exportado**: `comparison_summary.json`

**Decisiones técnicas**:
- Dataset: solo clases 1 y 2 del Iris (Versicolor vs Virginica); clase 0 (Setosa) descartada por ser trivialmente separable
- Escalado: MLP en [0,1] (MinMaxScaler); QNN en [0,π] (× π adicional para puertas de rotación)
- Arquitectura MLP: capas ocultas (4,4) para 2f y (8,4) para 4f, activación ReLU, optimizador Adam, 500 iteraciones
- Arquitectura QNN: `ZZFeatureMap(reps=3)` + `RealAmplitudes(reps=2)` + observable `Z⊗n` = 6 parámetros (2f), 8 parámetros (4f)
- Diferencia clave respecto al VQC: `NeuralNetworkClassifier` + `EstimatorQNN` en lugar del `VQC` de alto nivel → control explícito sobre el observable, el gradiente (regla de desplazamiento de parámetros) y el optimizador
- Multi-start COBYLA (N_STARTS=5, MAX_ITER=500): 5 arranques desde puntos aleatorios, se conserva el mejor → compensa la sensibilidad a la inicialización en paisajes no convexos
- Observable `Z⊗n` (todos los qubits): captura correlaciones en todo el registro; eigenvalores ±1 → salida en [-1,1], compatible con codificación de etiquetas {-1,+1}
- `StatevectorEstimator`: valores de expectación exactos (sin shots), usado en entrenamiento en simulador
- QNN logra paridad con el MLP (80%) usando 6× menos parámetros en 2f y 10× menos en 4f
- Degradación HW real mínima: 80%→75% en 2f; 80%=80% en 4f (circuito suficientemente superficial)
- Entrenamiento solo en simulador; inferencia en real HW para evitar colas largas
- Backend hardware usado: `ibm_kingston` (seleccionado por `least_busy()`)
- `EstimatorV2` + `generate_preset_pass_manager(optimization_level=1)`

---

## cryptography/factoring — COMPLETADO ✓

Archivo único: `real_shor_comparison.ipynb`.

Compara factorización clásica (división por tentativa, Pollard's rho) vs algoritmo de Shor (cuántico) en simulación y hardware IBM real.

**Resultados** — benchmark principal (n_count = 2·bits, RUNS=5, SHOTS=2000):

| N | bits | n_count | Trial Q | Pollard Q | QPE depth | Sim OK | Real OK | top_prob | Tiempo real |
|---|------|---------|---------|-----------|-----------|--------|---------|----------|-------------|
| 15 | 4 | 8 | 2.0 | 1.2 | 11 | Yes (r=2) | Yes (r=2) | 18.2% | 33.5 s |
| 21 | 5 | 10 | 2.0 | 1.2 | 13 | Yes (r=6) | Yes (r=2)† | 0.9% | 25.2 s |
| 33 | 6 | 12 | 2.0 | 1.2 | 15 | Yes (r=2) | Yes ★ (r=18) | 1.9% | 65.2 s |
| 35 | 6 | 12 | 3.0 | 1.4 | 15 | Yes (r=6) | Yes ★ (r=32) | 13.0% | 65.1 s |
| 77 | 7 | 14 | 4.0 | 1.4 | 17 | Yes (r=6) | N/A | — | — |
| 91 | 7 | 14 | 4.0 | 1.6 | 17 | Yes (r=6) | N/A | — | — |
| 143 | 8 | 16 | 6.0 | 2.0 | Skip | N/A | N/A | — | — |
| 221 | 8 | 16 | 7.0 | 4.0 | Skip | N/A | N/A | — | — |

† **Sub-periodo en N=21 real**: el QPE midió la fase 1/2 (pico k=3 de r=6), CF→r=2. gcd(2¹+1, 21)=3 ✓. Resultado legítimo, muy ruidoso (top_prob=0.9%).  
★ **Periodos espurios en N=33 y N=35**: ord₃₃(2)=10 pero hardware devolvió r=18; ord₃₅(2)=12 pero hardware devolvió r=32. El ruido QPE produjo medidas que, via CF y GCD, dieron factores correctos por casualidad. Factorización asistida por ruido.

**Resultados** — sweep de tasa de éxito (N=33, a=2, ord=10, 10 trials cada punto):

| n_count | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
|---------|---|---|---|---|---|---|----|----|----|----|-----|
| Éxito | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% |

100% de éxito en todo el rango n_count=4..14. El algoritmo es robusto incluso por debajo del mínimo recomendado (2·⌈log₂N⌉=12) porque k=5 (fase 1/2 → r=2) siempre aparece como pico dominante.

**Plots generados** (4): `plot1_complexity.png`, `plot2_success_rate.png`, `plot3_qpe_histogram.png`, `plot4_sim_vs_real.png`

**Resumen exportado**: `shor_summary.json`

**Decisiones técnicas**:
- `SIM_MAX_N = 100`: para N > 100 la matriz unitaria 2^n_target × 2^n_target es intratable (>256×256 → transpilación impracticable)
- `REAL_MAX_N = 35`: limita hardware real a circuitos de profundidad manejable (≤18 qubits total)
- Unitario de permutación exacto U|y⟩ = |a·y mod N⟩: kickback de fase genuino, pero construirlo es exponencial en n_bits (solo viable para N pequeños)
- Caché de puertas en el sweep: `pow(a, 2^j, N)` toma solo 5 valores distintos para N=33 → se descomponen 5 unitarios controlados una sola vez en lugar de O(Σ n_count)≈99 descomposiciones
- Extracción de sub-periodos por fracciones continuas: puede devolver un divisor de r (no r mismo) y aun así factorizar si a^(r/2) ≢ ±1 (mod N)
- Backend hardware usado: `ibm_kingston` (seleccionado por `least_busy()`)
- `SamplerV2` + `generate_preset_pass_manager(optimization_level=1)`
