// Corrección de referencia. Las primeras diez operaciones están incluidas.
export function calcularCosto(operaciones, interbancarias) {
  if (
    !Number.isInteger(operaciones) ||
    operaciones < 0 ||
    operaciones > 200 ||
    !Number.isInteger(interbancarias) ||
    interbancarias < 0 ||
    interbancarias > 100
  ) {
    const error = new RangeError(
      "Ingrese operaciones de 0 a 200 y transferencias de 0 a 100.",
    );
    error.code = "ERROR_VALIDACION";
    throw error;
  }
  const operacionesCobradas = Math.max(0, operaciones - 10);
  return (
    Math.round((25 + operacionesCobradas * 2.5 + interbancarias * 6) * 100) /
    100
  );
}
