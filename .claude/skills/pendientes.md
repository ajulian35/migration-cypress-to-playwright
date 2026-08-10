# Pendientes del Proyecto

## GitHub
- [ ] Crear una nueva rama en github y guardar el estado actual del proyecto

## Ejecución y Reportes
- [ ] Ejecutar suite Cypress y generar reporte en `reports/cypress/`
- [ ] Ejecutar suite Playwright y generar reporte en `reports/playwright/`
- [ ] Verificar que todos los tests pasen (req-001 al req-007 + precondiciones)

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
