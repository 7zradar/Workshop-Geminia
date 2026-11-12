# Reglas de negocio de la calculadora

Documento ficticio del workshop. Describe cómo se calcula el costo mensual de una cuenta PYME.

## Tarifa mensual
El mantenimiento mensual es S/ 25. Las primeras diez operaciones del mes son gratuitas y no generan comisión adicional. Desde la operación once se cobra S/ 2.50 por operación excedente. Cada transferencia interbancaria cuesta S/ 6. Fórmula: 25 + max(0, operaciones - 10) × 2.50 + interbancarias × 6.

## Límites de entrada
Las operaciones son enteros de 0 a 200 y las transferencias interbancarias son enteros de 0 a 100. Los valores negativos, fraccionarios, cadenas, infinitos o ausentes se rechazan con ERROR_VALIDACION y un mensaje claro para el usuario.

## Redondeo
El costo final se redondea a dos decimales antes de mostrarse al cliente.
