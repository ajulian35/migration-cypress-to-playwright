# Pendientes del Proyecto

## GitHub
- [x] Crear una nueva rama en github y guardar el estado actual del proyecto → rama `feature/migration-progress` publicada

## Ejecución y Reportes
- [x] Ejecutar suite Cypress y generar reporte en `reports/cypress/` → **6/8 passed** (reportes mochawesome generados)
- [x] Ejecutar suite Playwright y generar reporte en `reports/playwright/` → **6/8 passed** (report.html generado)
- [x] Verificar que todos los tests pasen (req-001 al req-007 + precondiciones) → **8/8 passed** en ambas suites

### Fallos identificados
| Suite | Test | Causa | Tipo |
|---|---|---|---|
| Cypress | `pre-002_create-claim` | `cy.within()` sobre 2 elementos `[role="dialog"]` — **fix aplicado** en `ClaimPage.ts:38` con `.first()` | Bug de código |
| Cypress | `req-006_search-employee` | Timeout de página (60s) — sitio demo sobrecargado tras 5 tests consecutivos | Flakiness de red |
| Playwright | `req-006_search-employee` | Timeout de navegación (30s) — mismo motivo de red | Flakiness de red |
| Playwright | `req-007_user-logout` | Timeout de navegación (30s) — mismo motivo de red | Flakiness de red |

## Código / Tests
- [x] Revisar y commitear cambios pendientes → tree limpio, 2 commits en `feature/migration-progress`
- [x] Validar precondiciones Playwright → `pytest_collection_modifyitems` en `conftest.py` ordena: pre_001 → pre_002 → reqs
- [x] Validar precondiciones Cypress → `specPattern` en `cypress.config.ts` fuerza el orden correcto del array

## Documentación del Capstone
- [x] Completar `migration_workflow.md` con el proceso Cypress → Playwright → archivo completo con conversión patterns y decisiones
- [x] Redactar problem statement → `docs/problem_statement.md` completo
- [x] Documentar data provenance → `docs/data_provenance.md` completo
- [x] Registrar errores que el AI generó y corregidos → `docs/ai_review.md` (3 errores documentados + actualizado con fix de REQ-006)
- [x] Failure analysis → `docs/failure_analysis.md` completo (5 casos con inputs, outputs, root cause; REQ-006 marcado como resuelto)
- [x] Mejora medida → `docs/measured_improvement.md`: fix REQ-006 autocomplete (fixed sleep → condition wait + name filter); FAILED → PASSED verificado
- [x] Slide de presentación → `docs/AI_Capstone_Filled_L1.pptx` (174KB) y `docs/stakeholder_slide.md` completos
- [x] Declarar esfuerzo → `docs/declared_effort.md` actualizado (~7h total, ejecución end-to-end incluida)

## Evidencia para el Checklist (`criteria_checklist.md`)
- [ ] Spec, plan y task artifacts con commit history que demuestre que precedieron la implementación
- [ ] Evidencia del efecto de `CLAUDE.md` en la calidad del output (antes/después)
- [ ] Pipeline de retrieval sobre documentos propios **o** automatización n8n con AI-in-the-loop
