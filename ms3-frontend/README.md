# MS3 · Frontend

Interfaz clínica accesible (WCAG 2.2 AA) construida con **Vite + JavaScript**.

Se despliega en **Firebase Hosting** (gratuito, plan Spark) y usa Firebase
Authentication, Firestore y Cloud Storage.

## Funcionalidad (bloque 6 del plan)

- Autenticación con roles podólogo/oncólogo (6.1).
- Gestión de pacientes seudonimizados (6.2).
- Subida de imagen con guía de captura (6.3).
- Visor de resultados: riesgo, probabilidad, rasgos y mapa de calor (6.4).
- Accesibilidad WCAG 2.2 AA y modo oscuro (6.5, 6.6).

## Desarrollo

Se levanta junto al resto con `docker compose up` desde la raíz. En local:

```bash
npm install
npm run dev
```

Abre http://localhost:5173

> Estado: **esqueleto**. Las vistas se implementan en el bloque 6 del plan.
