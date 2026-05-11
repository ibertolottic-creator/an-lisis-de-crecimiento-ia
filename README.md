# 📊 Sistema de Análisis de Crecimiento y Deserción — USMP Virtual 2026

> **Gestión Estratégica y Control de Matrícula** basado en métricas de conversión, retención y crecimiento neto para la Universidad de San Martín de Porres — Sede Virtual (UVA).

---

## 🎯 Descripción General

Sistema de inteligencia de negocios (BI) que transforma datos operativos de matrícula universitaria en un cuadro de mando estratégico interactivo. Procesa información mensual de **Carreras Profesionales (Pregrado)** y **Maestrías (Posgrado)**, calcula 8 indicadores estratégicos clave (KPIs), y presenta visualizaciones dinámicas con diagnósticos automatizados potenciados por **Gemini AI**.

### Características principales

- 📈 **15+ visualizaciones interactivas** (gráficos de barras, líneas, burbujas, doughnut)
- 🤖 **Diagnóstico con IA** (Gemini 2.5 Flash) integrado directamente en el dashboard
- 🔍 **Filtros multinivel**: Institucional → Pregrado/Posgrado → Programa individual
- 📊 **Matriz Estratégica BCG** para clasificación de programas (Estrellas, Dormidos, Fugas, Críticos)
- 📋 **Modales educativos** con fórmulas, interpretación y recomendaciones para cada métrica
- 🔄 **Doble modo de operación**: Conexión en vivo a Google Sheets + Modo Offline con CSV
- 📱 **Responsive** y optimizado para presentaciones ejecutivas

---

## 📂 Estructura del Proyecto

```
📁 Análisis de crecimiento y deserción/
├── 📄 index.html                    → Dashboard principal (Frontend completo)
├── 📄 Código.gs                     → Backend en Google Apps Script
├── 📄 Prompt Maestro_...txt         → Instrucciones para IA (generación de tablas)
├── 📄 Cuadro_Mando_Pregrado_Actualizado.csv   → Datos procesados Pregrado
├── 📄 Cuadro_Mando_Posgrado_Actualizado.csv   → Datos procesados Posgrado
├── 📄 Resultados Generales Carreras...docx    → Fuente original Pregrado
├── 📄 Resultados Generales Maestrías...docx   → Fuente original Posgrado
├── 📄 respaldoGestión Estratégica...xlsx       → Respaldo de la hoja de cálculo
├── 📄 DOCUMENTACION.md              → Documentación técnica completa
├── 📄 .gitignore
└── 📄 README.md                     → Este archivo
```

---

## 🚀 Estado del Proyecto

| Aspecto | Estado |
|---|---|
| Dashboard Frontend | ✅ Operativo |
| Backend Google Apps Script | ✅ Operativo |
| Integración Gemini AI | ✅ Operativo |
| Datos Pregrado (Ene–May 2026) | ✅ Cargados |
| Datos Posgrado (Ene–May 2026) | ✅ Cargados |
| Nuevo campo: Alumnos en Asignaturas de 2 Meses | ✅ Integrado |
| Modo Offline (CSV / Demo) | ✅ Operativo |
| Documentación técnica | ✅ Completa |

---

## 📖 Documentación

Consulta **[DOCUMENTACION.md](DOCUMENTACION.md)** para la guía completa que incluye:

- Proceso de actualización mensual (2 fases)
- Arquitectura técnica del sistema
- Diccionario completo de métricas y fórmulas
- Catálogo de todas las visualizaciones y análisis

---

## 🛠️ Tecnologías

- **Frontend**: HTML5, JavaScript vanilla, TailwindCSS (CDN), Chart.js
- **Backend**: Google Apps Script (GAS)
- **Base de datos**: Google Sheets
- **IA**: Gemini 2.5 Flash API
- **Parsing CSV**: PapaParse.js
- **Tipografía**: Google Fonts (Inter)

---

## 👤 Autor

Desarrollado para la **USMP Virtual (UVA)** — Ciclo Académico 2026-I.

---

*Última actualización: Mayo 2026*
