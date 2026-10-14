# Convenciones de contribución · Acralis AI

Este documento recoge las convenciones del proyecto (tarea 1.1 del plan).

## Ramas

- `main`: rama protegida. Nunca se hace push directo; solo entra código mediante **pull request** revisada.
- `feature/<descripcion-corta>`: nueva funcionalidad. Ej.: `feature/ms2-endpoint-analyze`.
- `fix/<descripcion-corta>`: corrección de errores. Ej.: `fix/cors-frontend`.

## Commits — Conventional Commits

Formato: `<tipo>(<ámbito opcional>): <descripción en minúscula>`

Tipos habituales:

| Tipo | Uso |
|---|---|
| `feat` | nueva funcionalidad |
| `fix` | corrección de error |
| `docs` | documentación |
| `chore` | tareas de mantenimiento, config, dependencias |
| `refactor` | cambio de código sin alterar comportamiento |
| `test` | añadir o corregir tests |
| `ci` | integración continua |

Ejemplos:

```
feat(ms2): endpoint /analyze que devuelve riesgo y probabilidad
fix(ms3): contraste insuficiente en la tarjeta de riesgo
docs(infra): instrucciones de los emuladores de Firebase
```

## Pull requests

- Una PR por tarea o subtarea del plan siempre que sea posible.
- Enlaza el *issue* correspondiente del tablero (GitHub Projects).
- Rellena la plantilla de PR.
- La PR debe pasar lint y tests (cuando exista CI, tarea 9.4).

## Issues y tablero

Las tareas del plan se crean como *issues* etiquetadas por **prioridad** (`P0`–`P3`) y **sprint** (`S1`–`S12`), gestionadas en GitHub Projects (tarea 1.1).
