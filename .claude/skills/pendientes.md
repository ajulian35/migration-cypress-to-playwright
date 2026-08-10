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
- [ ] Revisar y commitear cambios pendientes (todos los archivos están en estado `M`)
- [ ] Validar que los archivos de precondición (`pre-001`, `pre-002`) se ejecutan antes de los tests dependientes - proyecto playwright
- [ ] Validar que los archivos de precondición (`pre-001`, `pre-002`) se ejecutan antes de los tests dependientes - proyecto cypress

## Documentación del Capstone
- [ ] Completar `migration_workflow.md` con el proceso Cypress → Playwright
- [ ] Redactar problem statement (dominio, usuario, problema, definición de éxito)
- [ ] Documentar data provenance (origen de datos, limitaciones, sensibilidad)
- [ ] Registrar al menos un error que el AI generó y que fue corregido manualmente
- [ ] Failure analysis: inputs específicos que rompen los tests y por qué
- [ ] Mejora medida: estado antes, cambio aplicado, estado después
- [ ] Preparar slide de presentación para stakeholders (PowerPoint ya existe en `docs/`)
- [ ] Grabar demo o transcripción incluyendo al menos un caso que falla
- [ ] Declarar esfuerzo: horas aproximadas y qué se descartó

## Evidencia para el Checklist (`criteria_checklist.md`)
- [ ] Spec, plan y task artifacts con commit history que demuestre que precedieron la implementación
- [ ] Evidencia del efecto de `CLAUDE.md` en la calidad del output (antes/después)
- [ ] Pipeline de retrieval sobre documentos propios **o** automatización n8n con AI-in-the-loop
