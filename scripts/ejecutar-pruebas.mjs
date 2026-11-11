import { readFile } from "node:fs/promises";
import { resolve } from "node:path";
import { pathToFileURL, fileURLToPath } from "node:url";

const root = fileURLToPath(new URL("../", import.meta.url));
const args = process.argv.slice(2);
function option(name, fallback) {
  const index = args.indexOf(name);
  if (index === -1) return resolve(root, fallback);
  if (!args[index + 1]) throw new Error(`Falta valor de ${name}`);
  return resolve(args[index + 1]);
}

try {
  const motor = option("--motor", "app/calculadora.mjs");
  const casesPath = option("--casos", "contratos/casos.json");
  const cases = JSON.parse(await readFile(casesPath, "utf8"));
  const { calcularCosto } = await import(pathToFileURL(motor).href);
  if (typeof calcularCosto !== "function")
    throw new Error("El motor debe exportar calcularCosto.");
  const tests = cases.map((test) => {
    let actual;
    let error = null;
    try {
      actual = calcularCosto(test.input.operaciones, test.input.interbancarias);
      if (!Number.isFinite(actual))
        throw new Error("El resultado no es un número finito.");
    } catch (exception) {
      actual =
        exception.code === "ERROR_VALIDACION"
          ? "ERROR_VALIDACION"
          : "ERROR_EJECUCION";
      error = exception.message;
    }
    return { ...test, actual, passed: actual === test.expected, error };
  });
  const passed = tests.filter((test) => test.passed).length;
  console.log(
    JSON.stringify({
      tests,
      summary: {
        total: tests.length,
        passed,
        failed: tests.length - passed,
        percentage: Math.round((passed / tests.length) * 100),
      },
    }),
  );
  process.exitCode = passed === tests.length ? 0 : 1;
} catch (error) {
  console.log(JSON.stringify({ error: error.message }));
  process.exitCode = 2;
}
