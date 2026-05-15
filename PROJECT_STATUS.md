# Estado del proyecto — TFG Quantum Computing

**Entorno**: `.venv` en `/home/david/Desktop/TFG/Qiskit/`, activar con `source .venv/bin/activate`.  
**Hardware IBM**: credenciales guardadas, cargar con `QiskitRuntimeService()`. Plan Open (10 min/mes).

---

## cryptography/brute_force — PENDIENTE RE-EJECUCIÓN ⏳

Archivo único: `real_grover_comparison.ipynb`.

Compara búsqueda lineal y binaria (clásicas) vs algoritmo de Grover (cuántico) en simulación y hardware IBM real.

**Resultados anteriores** (n=2..11, real HW solo n≤5):

| n | N | Linear | Binary | Grover | Sim OK | Depth sim | Depth real | Prob real | Umbral | Real OK |
|---|---|--------|--------|--------|--------|-----------|------------|-----------|--------|---------|
| 2 | 4 | 2.7 | 2.0 | 1 | Yes | 6 | 12 | 93.0% | 50.0% | Yes |
| 3 | 8 | 4.2 | 3.0 | 2 | Yes | 10 | 170 | 76.5% | 35.4% | Yes |
| 4 | 16 | 4.7 | 3.0 | 3 | Yes | 14 | 596 | 41.4% | 25.0% | Yes |
| 5 | 32 | 14.5 | 5.0 | 4 | Yes | 18 | 1777 | 5.8% | 17.7% | **No** |
| 6–11 | 64–2048 | — | — | 6–35 | Yes | 26–142 | N/A | N/A | — | N/A |

**Estado**: el notebook tiene retoques pendientes de validar. Necesita re-ejecución completa (simulación + hardware real). Cola larga en IBM en este momento — aplazado.

**Plots generados** (5):
1. Consultas/iteraciones vs n (escala log)
2. Speedup relativo vs lineal, vs binaria, vs binaria+sort, y efectivo en HW real
3. Break-even: búsquedas mínimas para que binaria+Timsort supere a cada alternativa
4. Probabilidad de éxito en hardware real vs n
5. Profundidad del circuito transpilado (simulación vs hardware real)

**Decisiones técnicas**:
- Umbral de éxito: `prob > 1/√N` (√N veces más probable que uniforme), no mayoría simple
- Real HW limitado a n≤5: para n=5 el circuito ya alcanza profundidad 1777 en hardware real (×98 sobre simulación) por descomposición MCX→CNOT + SWAPs de enrutamiento
- Backends usados en ejecución anterior: `ibm_fez` (n=2,4,5), `ibm_kingston` (n=3)
- `SamplerV2` + `generate_preset_pass_manager(optimization_level=1)`
