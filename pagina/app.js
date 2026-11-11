/* Dashboard de reportes. Los resultados provienen del runner, no del navegador. */
const byId = (id) => document.getElementById(id);
let currentReport = null;
let connected = false;
let busy = false;
let imported = false;
let signature = "";
let historySignature = "";
let modeInitialized = false;

function notify(text, success = false) {
  const node = byId("message");
  node.textContent = text;
  node.classList.toggle("success", success);
  node.hidden = !text;
}

function element(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function formatValue(value) {
  return typeof value === "number" ? `S/ ${value.toFixed(2)}` : String(value);
}

function validateReport(report) {
  if (
    !report ||
    report.schema_version !== 1 ||
    !["evidencia", "gemini"].includes(report.mode) ||
    typeof report.id !== "string" ||
    typeof report.source_hash !== "string" ||
    !Array.isArray(report.tests) ||
    !report.tests.length ||
    report.tests.length > 100 ||
    !Array.isArray(report.analysis?.findings) ||
    typeof report.analysis.summary !== "string" ||
    typeof report.analysis.next_action !== "string" ||
    !Array.isArray(report.review?.observations) ||
    !["VALIDADO", "OBSERVADO"].includes(report.review.decision) ||
    !Array.isArray(report.trace) ||
    !Number.isFinite(new Date(report.executed_at).getTime())
  ) {
    throw new Error(
      "El archivo no cumple el formato de reporte QA de este workshop.",
    );
  }
  const ids = new Set();
  for (const test of report.tests) {
    if (
      typeof test.id !== "string" ||
      ids.has(test.id) ||
      typeof test.name !== "string" ||
      typeof test.criterion !== "string" ||
      typeof test.passed !== "boolean" ||
      !["string", "number"].includes(typeof test.expected) ||
      !["string", "number"].includes(typeof test.actual) ||
      test.passed !== (test.expected === test.actual) ||
      !Number.isInteger(test.input?.operaciones) ||
      !Number.isInteger(test.input?.interbancarias)
    ) {
      throw new Error(
        "Uno de los casos contiene datos inválidos o contradictorios.",
      );
    }
    ids.add(test.id);
  }
  const passed = report.tests.filter((test) => test.passed).length;
  if (
    report.summary?.total !== report.tests.length ||
    report.summary.passed !== passed ||
    report.summary.failed !== report.tests.length - passed ||
    report.summary.percentage !==
      Math.round((passed / report.tests.length) * 100)
  ) {
    throw new Error("El resumen no coincide con los casos del reporte.");
  }
  const failedIds = new Set(
    report.tests.filter((test) => !test.passed).map((test) => test.id),
  );
  const findingIds = report.analysis.findings.map((finding) => finding.case_id);
  if (
    findingIds.length !== failedIds.size ||
    new Set(findingIds).size !== failedIds.size ||
    findingIds.some((id) => !failedIds.has(id))
  ) {
    throw new Error("Los hallazgos no coinciden con los casos fallidos.");
  }
  return report;
}

function renderCases() {
  const list = byId("cases-list");
  list.replaceChildren();
  if (!currentReport) return;
  const filter = byId("filter").value;
  const tests = currentReport.tests.filter(
    (test) => filter === "all" || test.passed === (filter === "passed"),
  );
  if (!tests.length)
    list.append(element("p", "empty-state", "No hay casos con este filtro."));
  for (const test of tests) {
    const card = element(
      "article",
      `test-case ${test.passed ? "passed" : "failed"}`,
    );
    const top = element("div", "test-top");
    const title = element("div");
    title.append(
      element("span", "test-id", test.id),
      element("strong", "", test.name),
    );
    top.append(
      title,
      element(
        "span",
        `badge ${test.passed ? "good" : "bad"}`,
        test.passed ? "✓ Aprobada" : "× Fallida",
      ),
    );
    const details = element("details");
    details.open = !test.passed;
    details.append(element("summary", "", "Consultar criterio y evidencia"));
    const evidence = element("div", "evidence-grid");
    for (const [label, value] of [
      ["Esperado", test.expected],
      ["Obtenido", test.actual],
    ]) {
      const cell = element("div");
      cell.append(
        element("span", "", label),
        element("strong", "", formatValue(value)),
      );
      evidence.append(cell);
    }
    details.append(
      evidence,
      element("p", "case-criterion", test.criterion),
      element(
        "p",
        "case-criterion",
        `Entrada · ${test.input.operaciones} operaciones, ${test.input.interbancarias} transferencias`,
      ),
    );
    card.append(top, details);
    list.append(card);
  }
}

function renderReport(report) {
  currentReport = validateReport(report);
  for (const key of ["total", "passed", "failed"])
    byId(key).textContent = report.summary[key];
  byId("percentage").textContent = `${report.summary.percentage}%`;
  byId("progress-fill").style.width = `${report.summary.percentage}%`;
  byId("verdict").textContent = report.summary.failed
    ? "Con fallas"
    : "Sin fallas en los casos ejecutados";
  byId("verdict").className = `badge ${report.summary.failed ? "bad" : "good"}`;
  byId("report-meta").textContent =
    `${new Date(report.executed_at).toLocaleString("es-PE")} · Fuente ${report.source_hash.slice(0, 8)} · Disparador ${report.trigger}`;
  byId("report-mode").textContent =
    report.mode === "gemini"
      ? `Gemini · ${report.model}`
      : "Pruebas reales · análisis local";
  byId("analysis-heading").textContent =
    report.mode === "gemini" ? "Agente QA · Gemini" : "Diagnóstico local";
  byId("analysis-summary").textContent = report.analysis.summary;
  byId("next-action").textContent = report.analysis.next_action;
  const findings = byId("findings");
  findings.replaceChildren();
  for (const finding of report.analysis.findings) {
    const node = element("article", "finding");
    node.append(
      element("strong", "", finding.case_id),
      element("p", "", finding.description),
      element("small", "", finding.recommendation),
    );
    findings.append(node);
  }
  byId("review-heading").textContent =
    report.mode === "gemini"
      ? "Agente revisor · Gemini"
      : "Revisión local de consistencia";
  byId("review-decision").textContent =
    report.review.decision === "VALIDADO"
      ? "Reporte validado"
      : "Reporte observado";
  byId("review-decision").className =
    `badge ${report.review.decision === "VALIDADO" ? "good" : "bad"}`;
  byId("observations").replaceChildren(
    ...report.review.observations.map((text) => element("li", "", text)),
  );
  byId("trace").replaceChildren(
    ...report.trace.map((event) =>
      element("li", "", `${event.actor} → ${event.name} · ${event.event}`),
    ),
  );
  byId("download").disabled = false;
  renderCases();
}

async function api(path, body) {
  const response = await fetch(
    path,
    body === undefined
      ? { cache: "no-store" }
      : {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(body),
        },
  );
  const data = await response.json();
  if (!response.ok)
    throw new Error(data.error || "No se pudo completar la operación.");
  return data;
}

function setControls(status) {
  if (connected && !modeInitialized) {
    byId("mode").value = status.mode;
    modeInitialized = true;
  }
  busy = status.running || status.queued > 0;
  for (const id of ["run", "fix", "bug"])
    byId(id).disabled = !connected || busy;
  byId("run").textContent = busy ? "◌ Ejecutando QA…" : "▶ Ejecutar QA";
  byId("watch").disabled = !connected;
  byId("watch").checked = status.watch;
  byId("mode").disabled = !connected || busy;
  byId("mode").querySelector('option[value="gemini"]').disabled =
    !status.gemini_ready;
  byId("watch-description").textContent = status.watch
    ? "Activo. Guardar el código dispara una revisión."
    : "Pausado. Puedes ejecutar QA manualmente.";
}

function renderHistory(history) {
  const signature = JSON.stringify(history);
  if (historySignature === signature) return;
  historySignature = signature;
  byId("history").replaceChildren();
  if (!history.length)
    byId("history").append(
      element(
        "p",
        "muted",
        "Las versiones aparecerán después de la primera ejecución.",
      ),
    );
  for (const report of history.slice(0, 6)) {
    const button = element("button", "history-row");
    const label = element("div");
    label.append(
      element(
        "strong",
        "",
        `${report.summary.passed}/${report.summary.total} aprobadas · ${report.source_hash.slice(0, 8)}`,
      ),
      element(
        "small",
        "",
        `${new Date(report.executed_at).toLocaleString("es-PE")} · ${report.mode} · ${report.trigger}`,
      ),
    );
    button.append(
      label,
      element(
        "span",
        `badge ${report.summary.failed ? "bad" : "good"}`,
        `${report.summary.percentage}% ↗`,
      ),
    );
    button.addEventListener("click", async () => {
      try {
        renderReport(await api(`/api/report/${report.id}`));
        imported = true;
        notify(
          "Mostrando una ejecución del historial. Ejecuta QA para volver al reporte actual.",
          true,
        );
      } catch (error) {
        notify(error.message);
      }
    });
    byId("history").append(button);
  }
}

async function refresh() {
  if (location.protocol === "file:") return;
  try {
    const [status, report, history] = await Promise.all([
      api("/api/status"),
      api("/api/report"),
      api("/api/history"),
    ]);
    connected = true;
    byId("connection").textContent = busy
      ? "Ejecución en curso"
      : "Servidor local conectado";
    byId("connection").classList.add("online");
    byId("presentation-link").href = "/presentacion";
    setControls(status);
    byId("connection").textContent = busy
      ? "Ejecución en curso"
      : "Servidor local conectado";
    if (status.error) notify(status.error);
    const next = report ? `${report.id}:${report.executed_at}` : "";
    if (report && signature !== next && !imported) {
      renderReport(report);
      signature = next;
      if (!status.error) notify("");
    }
    renderHistory(history);
  } catch (error) {
    connected = false;
    byId("connection").textContent = "Servidor desconectado";
    byId("connection").classList.remove("online");
    setControls({
      watch: false,
      running: false,
      queued: 0,
      gemini_ready: false,
    });
  }
}

byId("filter").addEventListener("change", renderCases);
byId("run").addEventListener("click", async () => {
  try {
    imported = false;
    signature = "";
    await api("/api/run", { mode: byId("mode").value });
    notify(
      "Ejecución iniciada. Las herramientas comprobarán la versión actual.",
      true,
    );
    await refresh();
  } catch (error) {
    notify(error.message);
  }
});
byId("watch").addEventListener("change", async (event) => {
  try {
    await api("/api/watch", { enabled: event.target.checked });
    await refresh();
  } catch (error) {
    notify(error.message);
  }
});
async function applyScenario(name) {
  try {
    imported = false;
    const status = await api("/api/scenario", { name });
    if (!status.changed) {
      notify(
        "Esa versión ya está aplicada. Puedes ejecutar QA para revisarla de nuevo.",
        true,
      );
      return;
    }
    notify(
      "El archivo cambió. Esperando el reporte de la nueva versión…",
      true,
    );
    byId("calculation").textContent =
      "La versión cambió. Puedes repetir el cálculo.";
    await refresh();
  } catch (error) {
    notify(error.message);
  }
}
byId("fix").addEventListener("click", () => applyScenario("corregida"));
byId("bug").addEventListener("click", () => applyScenario("defectuosa"));
byId("import").addEventListener("change", async (event) => {
  const file = event.target.files[0];
  if (!file) return;
  try {
    if (file.size > 1000000)
      throw new Error("El reporte debe ocupar menos de 1 MB.");
    const report = validateReport(JSON.parse(await file.text()));
    renderReport(report);
    imported = true;
    notify(`Mostrando el reporte importado ${report.id}.`, true);
  } catch (error) {
    notify(`No se importó el archivo. ${error.message}`);
  }
  event.target.value = "";
});
byId("download").addEventListener("click", () => {
  if (!currentReport) return;
  const url = URL.createObjectURL(
    new Blob([JSON.stringify(currentReport, null, 2)], {
      type: "application/json",
    }),
  );
  const link = element("a");
  link.href = url;
  link.download = `reporte-qa-${currentReport.id}.json`;
  link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
});
byId("calculator-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  try {
    if (!connected)
      throw new Error(
        "Inicia el servidor con iniciar.ps1 para ejecutar el motor actual.",
      );
    const { calcularCosto } = await import(
      `../app/calculadora.mjs?v=${Date.now()}`
    );
    const value = calcularCosto(
      Number(byId("operations").value),
      Number(byId("transfers").value),
    );
    byId("calculation").textContent =
      `Resultado de la implementación actual · ${formatValue(value)}`;
  } catch (error) {
    byId("calculation").textContent = error.message;
  }
});

if (window.QA_EXAMPLE) {
  renderReport(window.QA_EXAMPLE);
  byId("report-meta").textContent +=
    " · Ejemplo guardado de una ejecución real";
}
if (location.protocol === "file:") {
  byId("connection").textContent = "Archivo local · ejemplo guardado";
  setControls({ watch: false, running: false, queued: 0, gemini_ready: false });
  byId("watch-description").textContent =
    "Inicia iniciar.ps1 para ejecutar el agente y vigilar cambios.";
} else {
  refresh();
  setInterval(refresh, 1500);
}
