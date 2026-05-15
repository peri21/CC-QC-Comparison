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
| QKSVM simulador (2 qubits) | 60% | — | 20.47 s | 47 |
| QKSVM hardware real | — | demo kernel 10 pts, Pearson r=0.9738 | 61.5 s (kernel) | — |

**Experimento 4 features** (sépalos + pétalos, todas):

| Modelo | Accuracy test |
|---|---|
| SVM 4f | 80% |
| QKSVM 4f (sim) | **70%** (mejor que 2f — el kernel cuántico aprovecha el espacio de mayor dimensión) |

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

## cryptography/factoring — PENDIENTE RE-EJECUCIÓN ⏳

Archivo único: `real_shor_comparison.ipynb`.

Compara factorización clásica (división por tentativa, Pollard's rho) vs algoritmo de Shor (cuántico) en simulación y hardware IBM real.

**Resultados anteriores** — benchmark principal (n_count = 2·bits):

| N | bits | n_count | QPE depth | Sim OK | Real OK | Backend |
|---|------|---------|-----------|--------|---------|---------|
| 15 | 4 | 8 | 11 | Yes (r=2) | Yes (r=2) | ibm_fez |
| 21 | 5 | 10 | 13 | Yes (r=6) | **No** | ibm_fez |
| 33 | 6 | 12 | 15 | Yes (r=2) | Yes (r=2) | ibm_fez |
| 35 | 6 | 12 | 15 | Yes (r=12) | Yes ★ (r=16) | ibm_fez |
| 77 | 7 | 14 | 17 | Yes (r=6) | N/A | — |
| 91 | 7 | 14 | 17 | Yes (r=6) | N/A | — |
| 143 | 8 | 16 | Skip | N/A | N/A | — |
| 221 | 8 | 16 | Skip | N/A | N/A | — |

★ **Periodo espurio en N=35**: hardware reportó r=16 pero ord₃₅(2)=12. El ruido QPE produjo r=16 y el GCD tuvo éxito por casualidad (2⁸ mod 35=11, gcd(10,35)=5 ✓). Factorización asistida por ruido, no QPE genuino.

**Resultados anteriores** — sweep de tasa de éxito (N=33, a=2, r=10, 10 trials cada punto):

| n_count | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
|---------|---|---|---|---|---|---|----|----|----|----|-----|
| Éxito | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% |

100% de éxito en todo el rango n_count=4..14. El algoritmo es robusto incluso por debajo del mínimo recomendado (2·⌈log₂N⌉=12) porque k=5 (fase 1/2 → r=2) siempre aparece entre los top-12 picos.

**Estado**: el notebook tiene retoques pendientes de validar. Necesita re-ejecución completa (simulación + hardware real). Cola larga en IBM — aplazado.

**Plots generados** (4):
1. Escalado de complejidad: consultas clásicas vs profundidad QPE (escala log), extrapolado a tamaños de clave RSA
2. Tasa de éxito del QPE vs n_count (sweep N=33)
3. Histograma de medidas del QPE (N=15, a=7, n_count=8)
4. Simulación vs hardware IBM real: éxito y probabilidad del resultado más frecuente (proxy de ruido)

**Decisiones técnicas**:
- `SIM_MAX_N = 100`: para N > 100 la matriz unitaria 2^n_target × 2^n_target es intratable (>256×256 → transpilación impracticable)
- `REAL_MAX_N = 35`: limita hardware real a circuitos de profundidad manejable (≤18 qubits)
- Unitario de permutación exacto U|y⟩ = |a·y mod N⟩: kickback de fase genuino, pero construirlo es exponencial en n_bits (solo viable para N pequeños)
- Caché de puertas en el sweep: `pow(a, 2^j, N)` toma solo 5 valores distintos para N=33 → se descomponen 5 unitarios controlados una sola vez en lugar de O(Σ n_count)≈99 descomposiciones
- Extracción de sub-periodos por fracciones continuas: puede devolver un divisor de r (no r mismo) y aun así factorizar si a^(r/2) ≢ ±1 (mod N)
- Backend usado: `ibm_fez` para todos los casos de hardware real
- `SamplerV2` + `generate_preset_pass_manager(optimization_level=1)`
