# Aplicación bajo prueba

Calculadora ficticia de costo mensual. El motor recibe operaciones e interbancarias enteras. Operaciones válidas de 0 a 200 e interbancarias de 0 a 100. Los valores negativos, fraccionarios, cadenas, infinitos o ausentes son inválidos.

Costo = 25 + max(0, operaciones - 10) * 2.50 + interbancarias * 6.

| ID | Operaciones | Interbancarias | Esperado |
|---|---|---|---|
| QA-01 | 0 | 0 | 25 |
| QA-02 | 10 | 0 | 25 |
| QA-03 | 20 | 4 | 74 |
| QA-04 | -1 | 0 | Error de validación |

La versión defectuosa cobra todas las operaciones. La corrección respeta las primeras diez operaciones libres. La spec y casos son comunes a ambas versiones. Los archivos demo/version-*.mjs son referencias pedagógicas. El agente prueba app/calculadora.mjs, cuya huella se incorpora al reporte.
