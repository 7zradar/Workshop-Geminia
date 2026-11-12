# Guía de severidad

Guía ficticia para clasificar los defectos que reporta el agente QA.

## S1 Crítica
El sistema no calcula o cobra de forma masiva un monto incorrecto a todos los clientes. Requiere corrección inmediata.

## S2 Alta
El cálculo del costo es incorrecto para un grupo de clientes o para un tramo de la tarifa, por ejemplo operaciones gratuitas cobradas o validaciones ausentes. Se corrige antes del próximo despliegue.

## S3 Media
Diferencias menores de redondeo o de presentación sin impacto relevante en el monto cobrado. Se programa en el siguiente ciclo.
