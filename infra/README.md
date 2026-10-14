# infra · Infraestructura

Configuración de infraestructura del proyecto.

## `firebase/`

Emuladores de Firebase para desarrollo local (tarea 1.3) y reglas de
seguridad (tarea 8.1).

- `firebase.json` — configuración de emuladores (Auth, Firestore, Storage, UI).
- `firestore.rules` / `storage.rules` — reglas de seguridad.
- `firestore.indexes.json` — índices de Firestore.
- `.firebaserc` — proyecto por defecto (`acralis-dev`).
- `emulator-data/` — datos importados/exportados por los emuladores (no se versionan).

Los emuladores se levantan con el resto del stack desde la raíz:

```bash
docker compose up --build
```

- Emulator UI: http://localhost:4000
- Firestore: `localhost:8080` · Auth: `localhost:9099` · Storage: `localhost:9199`

## Nota sobre despliegue (plan gratuito)

El plan contempla **Cloud Run** para MS1/MS2/orquestador (tarea 10.1), que
requiere el plan **Blaze** de Firebase/GCP (con facturación activada). El plan
**Spark gratuito** cubre Firestore, Storage, Authentication y **Hosting** (para
el frontend). La estrategia de despliegue "solo gratuito" se decide en el
Sprint 10; durante el desarrollo todo corre en local con Docker + emuladores.
