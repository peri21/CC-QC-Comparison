# Explicación: gráfico Accuracy/Tiempo (plot5_ratio.png)

El gráfico `plot5_ratio.png` muestra el cociente **accuracy de test / tiempo de entrenamiento**
para el SVM clásico y el VQC cuántico (simulador Aer), en escala logarítmica.

## Valores obtenidos (2 features)

| Modelo | Accuracy | Tiempo entrenamiento | Ratio |
|--------|----------|----------------------|-------|
| SVM (clásico) | 85% | 0.003 s | ~284 |
| VQC (simulador) | 68% | 323 s | ~0.002 |

La diferencia es de aproximadamente **95.000×**, lo que en escala logarítmica produce
una barra prácticamente invisible para el VQC frente a la del SVM.

## Por qué no hay que interpretar este dato como "el SVM es 95.000× mejor"

1. **El tiempo del VQC es tiempo de simulación clásica**, no tiempo de ejecución en
   hardware cuántico real. Simular un circuito cuántico de 2 qubits con 300 iteraciones
   SPSA en un ordenador convencional es inherentemente costoso porque requiere mantener
   el vector de estado completo. En hardware cuántico real, cada medición es casi
   instantánea.

2. **La métrica accuracy/tiempo no es relevante para comparar paradigmas cuántico vs
   clásico en NISQ.** Lo que importa es la tendencia de escalado: el SVM escala como
   O(n²) o O(n³) con el número de muestras, mientras que los algoritmos cuánticos
   apuntan a ventajas asintóticas en problemas específicos (no necesariamente
   clasificación Iris).

3. **El problema es demasiado pequeño** (100 muestras, 2 features) para que el VQC
   pueda mostrar ninguna ventaja. El overhead de simulación domina completamente.

## Cómo presentarlo en el TFG

Incluir este gráfico acompañado de la aclaración de que la diferencia refleja el coste
de *simular* un computador cuántico, no el coste de *ejecutar* uno. La comparación
relevante para el tribunal es la de accuracy (SVM 85% vs VQC 70%) y la discusión
sobre por qué el VQC no converge mejor (barren plateaus, expresividad limitada con
2 qubits, ruido NISQ).
