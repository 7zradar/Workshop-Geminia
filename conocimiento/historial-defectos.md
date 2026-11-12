# Historial de defectos del motor

Registro ficticio de defectos anteriores. Sirve para reconocer patrones repetidos.

## DEF-101 Cobro de operaciones gratuitas
Versión 1.2. El motor multiplicaba todas las operaciones por 2.50 e ignoraba que las primeras diez operaciones son gratuitas. Síntoma: diez operaciones cobraban S/ 50 en lugar de S/ 25 y veinte operaciones con cuatro transferencias cobraban S/ 99 en lugar de S/ 74. Corrección aplicada entonces: operacionesCobradas = Math.max(0, operaciones - 10). Severidad S2.

## DEF-087 Redondeo de transferencias
Versión 1.1. El total se redondeaba antes de sumar las transferencias interbancarias y el cliente veía diferencias de un céntimo. Corrección: redondear una sola vez al final. Severidad S3.

## DEF-064 Validación de operaciones negativas
Versión 1.0. El motor aceptaba operaciones negativas y devolvía un costo menor al mantenimiento. Corrección: rechazar con ERROR_VALIDACION cuando las operaciones no están entre 0 y 200. Severidad S2.
