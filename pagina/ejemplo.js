window.QA_EXAMPLE = {
  "schema_version": 1,
  "id": "46eea48df326386578c3",
  "executed_at": "2026-11-11T17:14:43+00:00",
  "mode": "evidencia",
  "model": null,
  "trigger": "ejemplo",
  "source_hash": "3fb3e70d99abf257f8d66f0f33d9b15f1e589b6c2788cb5c1e67ea1c621887ca",
  "contract_hash": "56624697fc9bbce8d61f96f696639be5b7936eeb8b78df27ad84878818b381dd",
  "verdict": "CON_FALLAS",
  "summary": {
    "total": 4,
    "passed": 2,
    "failed": 2,
    "percentage": 50
  },
  "tests": [
    {
      "id": "QA-01",
      "name": "Sin operaciones se cobra solo mantenimiento",
      "criterion": "El mantenimiento mensual es S/ 25",
      "input": {
        "operaciones": 0,
        "interbancarias": 0
      },
      "expected": 25,
      "actual": 25,
      "passed": true,
      "error": null
    },
    {
      "id": "QA-02",
      "name": "Las primeras diez operaciones son gratuitas",
      "criterion": "Hasta diez operaciones no generan comisión adicional",
      "input": {
        "operaciones": 10,
        "interbancarias": 0
      },
      "expected": 25,
      "actual": 50,
      "passed": false,
      "error": null
    },
    {
      "id": "QA-03",
      "name": "Se cobra solo el exceso y las transferencias",
      "criterion": "25 + (20 - 10) × 2.50 + 4 × 6 = 74",
      "input": {
        "operaciones": 20,
        "interbancarias": 4
      },
      "expected": 74,
      "actual": 99,
      "passed": false,
      "error": null
    },
    {
      "id": "QA-04",
      "name": "Se rechazan operaciones negativas",
      "criterion": "Las operaciones deben ser enteros entre 0 y 200",
      "input": {
        "operaciones": -1,
        "interbancarias": 0
      },
      "expected": "ERROR_VALIDACION",
      "actual": "ERROR_VALIDACION",
      "passed": true,
      "error": "Ingrese operaciones de 0 a 200 y transferencias de 0 a 100."
    }
  ],
  "analysis": {
    "summary": "2 de 4 pruebas aprobadas. 2 diferencias frente a la especificación.",
    "findings": [
      {
        "case_id": "QA-02",
        "description": "Las primeras diez operaciones son gratuitas. Se esperaba 25 y se obtuvo 50.",
        "recommendation": "Revisar la implementación frente al criterio de este caso y repetir la prueba."
      },
      {
        "case_id": "QA-03",
        "description": "Se cobra solo el exceso y las transferencias. Se esperaba 74 y se obtuvo 99.",
        "recommendation": "Revisar la implementación frente al criterio de este caso y repetir la prueba."
      }
    ],
    "next_action": "Corregir los casos fallidos y volver a ejecutar QA."
  },
  "review": {
    "decision": "VALIDADO",
    "observations": [
      "Comprobación local de correspondencia entre casos fallidos y hallazgos.",
      "El modo evidencia usa pruebas reales y un diagnóstico determinista."
    ]
  },
  "trace": [
    {
      "actor": "qa",
      "event": "tool",
      "name": "leer_criterios"
    },
    {
      "actor": "qa",
      "event": "tool",
      "name": "ejecutar_pruebas"
    },
    {
      "actor": "revision_local",
      "event": "completed",
      "name": "consistencia"
    }
  ]
};
