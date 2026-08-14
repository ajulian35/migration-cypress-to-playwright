# Pendientes — L2 Capstone Plan
**Proyecto:** Cypress → Playwright Test Migration Agent  
**Rama activa:** L2  
**Fecha:** 2026-08-14

---

## FUENTE 1 — L1 Capstone Review (Feedback pendiente de la primer parte)

> Solo se listan los ítems que el evaluador identificó como **gap, incompleto, o requieren acción en L2**.

### P1. Spec-Driven Development — Brecha crítica (3/15)
- [x] La secuencia **spec → plan → tasks → implement** debe ser verificable desde el historial de git. El proyecto L1 no tenía repositorio al inicio. Para L2: crear commits en ese orden desde el primer día en la rama `L2`.
- [x] El commit inicial de L2 debe contener únicamente el spec/problem-statement. No código aún.

### P2. Evidencia de ejecución del suite
- [x] La ejecución L1 que reclamó "8/8 passing" fue **inconclusa** para el evaluador (3/4 tests se quedaron en login page en su run independiente). Para L2 se debe incluir en el repositorio el **output real de consola / reporte HTML** de una ejecución exitosa documentada.

### P3. Documento de requerimientos desactualizado
- [x] Actualizar `requirements/functional_requirements_Cypress.md` líneas 26–28 para que los valores (Nationality, Marital Status, Date of Birth) reflejen los valores actuales del demo live, en lugar de los valores stale del spec original.

### P4. Bugs conocidos no corregidos en L1 (del ai_review.md)
- [x] **REQ-007** — username `"mandaa user"` hardcodeado en `playwright/tests/step_defs/req_007_steps.py:8`. Cambiar a `.oxd-userdropdown-tab` o leer desde fixture/env. _(ya resuelto en código — usa `.oxd-userdropdown-tab`)_
- [x] **REQ-002** — re-localización redundante de la misma fila usando referencia hardcodeada `"202307180000002"` en 6 `@then` steps. Refactorizar para usar `ref_id` del parámetro o fixture compartido. _(ya resuelto — código usa matching dinámico sin hardcode)_
- [x] **REQ-005** — no hay teardown del empleado creado. Cada ejecución acumula registros en el demo. Agregar fixture con cleanup post-escenario. _(resuelto: `cleanup_test_employee` session autouse en `conftest.py`)_

---

## FUENTE 2 — L2_Case05_Open_Choice_Agent_Brief.docx (Nuevos requerimientos)

> El L2 es un nivel diferente: ya no es solo migrar tests, es **construir y documentar un agente** que opere el workflow de migración de forma confiable.

### P5. Definición del problema agentic
- [ ] Escribir un **problem statement** claro: dominio, usuario nombrado, y la decisión que el agente toma en su nombre. Debe justificar por qué un agente (decisión en runtime) es mejor que un script determinista.
- [ ] Confirmar que el agente actual (`playwright-migration` en `.claude/agents/playwright-migration.md`) cumple con la definición: "el modelo decide qué hacer en runtime, no sigue una secuencia hardcodeada".

### P6. Arquitectura del agente — componentes requeridos
- [ ] **Al menos 2 herramientas** que el agente invoca documentadas explícitamente (ej. MCP Playwright browser, file-write tools, Read/Grep tools).
- [ ] **Componente de memoria** con justificación del tier elegido (short-term / session / long-term). Documentar qué se almacena y por qué.
- [ ] **Human validation gate** explícito antes de cualquier acción irreversible (ej. antes de sobrescribir tests, antes de hacer commit). Demostrar que existe en el flujo.

### P7. Manejo de fallos (obligatorio)
- [ ] El agente debe **validar el output de las herramientas** en lugar de asumirlo correcto.
- [ ] Cuando falla, debe **incluir la razón específica del fallo en el retry** (no reintentar a ciegas).
- [ ] Después de N fallos repetidos, **escalar con contexto completo** en lugar de entrar en loop.
- [ ] **Inyectar un fallo deliberado** (ej. tool output malformado, timeout, input inesperado) y demostrar que el agente lo maneja o escala correctamente.

### P8. Evaluación objetiva del agente
- [ ] Definir criterios de evaluación propios (no por inspección). Ej. "el test generado corre sin modificación manual", "el selector corresponde al elemento correcto", etc.
- [ ] Reportar los **casos donde el agente falla**, con al menos **2 explicados mecánicamente** (input específico → output incorrecto → causa raíz).

### P9. Stack tecnológico
- [ ] Documentar el stack elegido y justificar contra **al menos una alternativa rechazada** (ej. LangGraph vs n8n vs Claude Code Agent SDK).
- [ ] Si se usa Portkey o LangSmith, documentar la configuración. Si no se usan, justificar el equivalente de observabilidad.

---

## FUENTE 3 — criteria_checklist.md (Criterios de evaluación — todos unchecked)

### P10. DEFINE — Obligatorios
- [ ] Problem statement: dominio, usuario, decisión que el agente delega.
- [ ] Justificación de que el agente es necesario (vs script determinista).
- [ ] Data provenance note: fuente, qué representa, si incluye casos difíciles que exponen fallos del agente, cómo se maneja información sensible.

### P11. BUILD — Obligatorios
- [ ] Agente funcionando end-to-end, demostrable.
- [ ] Mínimo 2 tools invocadas por el agente.
- [ ] Componente de memoria con razón declarada del tier elegido.
- [ ] Human validation gate antes de cualquier acción irreversible.
- [ ] Failure handling: output validado, razón de fallo incluida en retry, escalación con contexto completo después de fallo repetido.

### P12. PROVE — Obligatorios
- [ ] Evaluación contra criterios definidos y defendibles (no por inspección).
- [ ] Casos donde falla, con mínimo 2 explicados mecánicamente.
- [ ] Inyección deliberada de fallo + demostración de recovery o escalación.
- [ ] **Suite `pytest-asyncio`** cubriendo: agent loop, tool mocking, recovery path — con output de ejecución pasando incluido.
- [ ] **Evidencia de observabilidad**: Portkey traces, LangSmith step traces, o equivalente.

### P13. COMMUNICATE — Obligatorios
- [ ] `REFLECTION.md` 600–1000 palabras: qué se construyó, por qué, qué falló, cómo se corrigió, qué se haría diferente, impacto de negocio. Las secciones de fallo tienen mayor peso.
- [ ] **Un slide** presentando la solución a stakeholders del cliente.
- [ ] **Demo** mostrando: (a) run normal y (b) fallo siendo manejado/escalado.
- [ ] Declared-effort statement: horas aproximadas y qué se decidió cortar.

---

## FUENTE 4 — Presentación L2 (AI_Capstone_L2_Julian Largo.pptx)

> La presentación es un **template en blanco** — ningún slide de contenido está completado. Todo lo siguiente está pendiente.

### P14. Completar slides de contenido
- [ ] **Slide 1**: Agregar nombre (Julian Largo Ramirez) y fecha. Seleccionar Option 4 (AI Case Study).
- [ ] **Slide 3 — Project Overview**: Completar con dominio del proyecto, problema, solución AI, y outcomes cuantificados.
- [ ] **Slide 4 — AI Approach**: Documentar el flujo paso a paso del agente (ej. requirements → MCP exploration → code generation → validation → report).
- [ ] **Slide 5 — Before/After**: Proceso manual vs proceso asistido por AI. Incluir screenshot de output del agente. Tiempos comparados.
- [ ] **Slide 6 — AI Impact Scorecard**: Llenar métricas reales (tiempo antes/después, calidad, frecuencia, beneficio de equipo). Incluir números específicos.
- [ ] **Slide 7 — Reusability & Scale**: Qué es reutilizable (el agente, los prompts, el CLAUDE.md), quién puede adoptarlo, qué se empaquetó.
- [ ] **Slide 8 — What AI Got Right & Wrong**: Ejemplos reales del proyecto (ej. selector generation, import shadowing bug, demo data drift). Ser específico.
- [ ] **Slide 9 — Evidence & Artifacts**: Links a commits, demo recording, prompt log/transcript, screenshots. Completar datos del Validator.
- [ ] **Slide 11 — Self-Rating**: Completar scores por cada uno de los 5 competency topics.
- [ ] **Slide 12 — Reflection & Key Takeaway**: Completar frases de reflexión y nivel de confianza before/after.

---

## PLAN CONSOLIDADO

Todas las tareas agrupadas por categoría, ordenadas por prioridad.

### A. GIT / SPEC-DRIVEN (crítico para puntuación)
1. ~~El historial de commits en `L2` debe seguir la secuencia: spec → plan → tasks → implement. Asegurarse de hacer commits granulares desde ahora.~~ ✅ Commits `c168a01` (spec), `ed438f4` (plan), `6a379e1` (fix), `449adf0` (docs) verificables en L2.
2. ~~Actualizar `requirements/functional_requirements_Cypress.md` con valores live de REQ-001 (Nationality, Marital Status, Date of Birth).~~ ✅ Actualizado a test user qauser_001 (Julian/Test/QAUser); campos opcionales no verificados documentados.

### B. CÓDIGO — BUGS PENDIENTES
3. ~~Corregir `req_007_steps.py:8` — reemplazar `"mandaa user"` hardcodeado por `.oxd-userdropdown-tab` o fixture de env.~~ ✅ Ya resuelto.
4. ~~Refactorizar `req_002_steps.py` — eliminar re-localización redundante con referencia hardcodeada, usar `ref_id` del parámetro.~~ ✅ Ya resuelto.
5. ~~Agregar teardown en `req_005_steps.py` para eliminar el empleado creado (cleanup post-escenario).~~ ✅ `cleanup_test_employee` en `conftest.py`.

### C. TESTS — EJECUCIÓN Y EVIDENCIA
6. ~~Ejecutar los 8 tests de Cypress (suite completa) y capturar el output/reporte HTML como evidencia oficial para L2.~~ ✅ 8/8 passing, reportes mochawesome en `reports/cypress/`.
7. ~~Ejecutar los 8 tests de Playwright (suite completa) y capturar el output/reporte HTML como evidencia oficial para L2.~~ ✅ 8/8 passing, reporte en `reports/playwright/report.html`.
8. Idealmente repetir contra entorno estable (si no se puede containerizar, documentar la inestabilidad del demo compartido como limitación conocida con detalle técnico).

### D. AGENTE — ARQUITECTURA Y DOCUMENTACIÓN
9. Documentar el agente de migración como sistema agentic: tools usadas, memory tier, human gate, failure handling.
10. Definir y escribir el **problem statement** del agente: dominio, usuario, decisión delegada, justificación vs script.
11. Escribir la **data provenance note** para L2 (OrangeHRM demo: qué representa, limitaciones, casos difíciles incluidos).
12. Implementar o documentar el **human validation gate** explícito en el flujo del agente.
13. Documentar/implementar **failure handling**: validación de tool output, retry con razón de fallo, escalación.
14. **Inyectar fallo deliberado** y capturar la respuesta del agente como evidencia.

### E. EVALUACIÓN DEL AGENTE
15. Definir criterios de evaluación del agente (no por inspección).
16. Documentar al menos 2 casos donde el agente falla, con explicación mecánica (input → output incorrecto → causa raíz).
17. Crear suite **`pytest-asyncio`** cubriendo agent loop, tool mocking y recovery path, con output pasando.

### F. OBSERVABILIDAD
18. Integrar y capturar trazas de observabilidad (Portkey, LangSmith, o equivalente de Claude Code) como evidencia del comportamiento del agente.

### G. DOCUMENTACIÓN NUEVA
19. Crear `REFLECTION.md` (600–1000 palabras): qué se construyó, por qué, qué falló, cómo se corrigió, qué se haría diferente, impacto de negocio.
20. Actualizar `declared_effort.md` con las horas del L2 y qué se decidió cortar.

### H. PRESENTACIÓN
21. Completar todos los slides de la presentación `AI_Capstone_L2_Julian Largo.pptx` (Slides 1, 3–9, 11–12) con contenido real del proyecto L2.
22. El Slide 9 debe incluir links reales a commits, demo recording, prompt logs.
23. El Slide 11 debe contener un self-rating honesto de los 5 competency topics.
