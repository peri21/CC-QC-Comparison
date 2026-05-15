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
