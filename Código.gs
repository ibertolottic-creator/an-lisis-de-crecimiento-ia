function doGet(e) {
  return HtmlService.createHtmlOutputFromFile("Index")
    .setTitle("Análisis de Crecimiento USMP Virtual")
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL)
    .addMetaTag("viewport", "width=device-width, initial-scale=1");
}

function getDatos() {
  try {
    // Intenta usar la hoja activa si el script está vinculado, sino usa el ID
    let ss;
    try {
      ss = SpreadsheetApp.getActiveSpreadsheet();
    } catch (e) {}

    if (!ss) {
      // CONEXIÓN ABSOLUTA con tu ID de Google Sheets
      ss = SpreadsheetApp.openById(
        "1rOv812dEhB0uT4DGwNnVEqJLWfhFfTmpWohLYcaZB28",
      );
    }

    let sheetPregrado = null;
    let sheetPosgrado = null;

    // Búsqueda inteligente de pestañas (ignora mayúsculas y espacios)
    const sheets = ss.getSheets();
    for (let s of sheets) {
      let name = s.getName().toLowerCase().trim();
      if (name.includes("pregrado")) sheetPregrado = s;
      if (name.includes("posgrado")) sheetPosgrado = s;
    }

    if (!sheetPregrado && !sheetPosgrado) {
      let nombresActuales = sheets.map((s) => s.getName()).join(" | ");
      throw new Error(
        "No encontré las pestañas. Nombres actuales: [ " +
          nombresActuales +
          " ].",
      );
    }

    const dataPregrado = sheetPregrado ? sheetToObjects(sheetPregrado) : [];
    const dataPosgrado = sheetPosgrado ? sheetToObjects(sheetPosgrado) : [];

    return {
      pregrado: dataPregrado,
      posgrado: dataPosgrado,
    };
  } catch (error) {
    throw new Error("Fallo en Base de Datos: " + error.message);
  }
}

function sheetToObjects(sheet) {
  if (!sheet) return [];

  const data = sheet.getDataRange().getValues();
  if (data.length < 2) return [];

  const headers = data[0].map((h) => h.toString().toLowerCase().trim());
  const rows = data.slice(1);

  // Buscador de columnas a prueba de fallos
  const getIdx = (possibleNames) => {
    // 1. Coincidencia exacta
    for (let name of possibleNames) {
      let idx = headers.findIndex((h) => h === name);
      if (idx !== -1) return idx;
    }
    // 2. Coincidencia parcial
    for (let name of possibleNames) {
      let idx = headers.findIndex((h) => h.includes(name));
      if (idx !== -1) return idx;
    }
    return -1;
  };

  const idxMes = getIdx(["mes"]);
  const idxPrograma = getIdx(["programa"]);
  const idxEgresados = getIdx(["egresado"]);
  const idxNoMatri = getIdx(["no matrí", "no matri", "deserción", "abandono"]);
  const idxAdmitidosMatri = getIdx([
    "admitidos matriculados",
    "adm. mat",
    "admitidos matri",
  ]);
  // Asegurarse de que 'admitidos' no coincida con 'admitidos matriculados' si es posible, 
  // pero findIndex en exact match lo previene. Para contains, hay riesgo.
  const idxAdmitidos = getIdx(["admitidos"]);
  
  const idxRecuperados = getIdx(["recuperado"]);
  const idxDistancia = getIdx(["distancia"]);
  const idxPresencial = getIdx(["presencial"]);
  const idxTotal = getIdx([
    "total",
    "matrí. total",
    "matri. total",
    "estudiantes",
  ]);
  const idxDosMeses = getIdx(["2 meses", "dos meses", "tránsito", "transito"]);

  return rows
    .map((row) => {
      if (
        idxMes === -1 ||
        idxPrograma === -1 ||
        !row[idxMes] ||
        !row[idxPrograma]
      )
        return null;

      return {
        mes: String(row[idxMes]),
        programa: String(row[idxPrograma]),
        egresados: parseInt(row[idxEgresados]) || 0,
        noMatri: parseInt(row[idxNoMatri]) || 0,
        // Evitar que admitidos sea igual a admitidos matriculados si las columnas se confundieron
        admitidos: parseInt(row[idxAdmitidos]) || 0,
        admitidosMatri: parseInt(row[idxAdmitidosMatri]) || 0,
        recuperados: parseInt(row[idxRecuperados]) || 0,
        matDistancia: parseInt(row[idxDistancia]) || 0,
        matPresencial:
          idxPresencial !== -1 ? parseInt(row[idxPresencial]) || 0 : 0,
        total: parseInt(row[idxTotal]) || 0,
        dosMeses: idxDosMeses !== -1 ? parseInt(row[idxDosMeses]) || 0 : 0,
      };
    })
    .filter((r) => r !== null);
}

function analizarConGemini(datos, nivel, mes) {
  const API_KEY = "AIzaSyDzVb8Y6ZWxH3Rs67Ai-sO4AFjESbjQpcU";
  const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${API_KEY}`;
  
const prompt = `Eres un Director Estratégico Universitario experto en análisis de datos.
Analiza los siguientes resultados del nivel académico "${nivel}" en el mes de "${mes}".
Datos:
- Total Matriculados: ${datos.total}
- Alumnos en Asignaturas de 2 Meses (En Tránsito): ${datos.dosMeses}
- Crecimiento Neto: ${datos.crecimientoNeto}
- Tasa Efectividad Comercial: ${datos.tasaEfComercial}% (Admitidos que pagaron: ${datos.admitidosMatri} de ${datos.admitidos})
- Tasa de Deserción: ${datos.tasaDesercion}% (Fuga: ${datos.noMatri})
- Balance de Retención: ${datos.balanceRetencion} (Recuperados: ${datos.recuperados} vs Fuga: ${datos.noMatri})

Proporciona un diagnóstico ejecutivo breve (máximo 2 párrafos) y 3 viñetas con recomendaciones de acción directa para mejorar estos KPIs. Usa un tono gerencial, directo y orientado a resultados.
No uses formato markdown excesivo, solo negritas para resaltar.`;

  const payload = {
    contents: [{ parts: [{ text: prompt }] }]
  };

  const options = {
    method: "post",
    contentType: "application/json",
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  };

  try {
    const response = UrlFetchApp.fetch(url, options);
    const result = JSON.parse(response.getContentText());
    if (result.error) {
      return "Error de la IA: " + result.error.message;
    }
    return result.candidates[0].content.parts[0].text;
  } catch (e) {
    return "Ocurrió un error al contactar a la IA: " + e.message;
  }
}

