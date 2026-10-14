# MS2 · Procesamiento de imagen e IA

Microservicio de visión artificial y aprendizaje profundo.

- **Preprocesamiento:** normalización, reducción de ruido, CLAHE, control de calidad (tarea 3.1).
- **Segmentación:** pie/fondo y máscara de la lesión, U-Net ligera si hace falta (tarea 3.2).
- **Modelo CNN:** EfficientNet-B0 por transfer learning, calibrado (tarea 3.4).
- **API:** FastAPI con `/analyze` (tarea 3.7).

## Endpoints (contrato · tarea 1.4)

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/health` | Healthcheck (incluye versión del modelo) |
| POST | `/analyze` | Recibe imagen; devuelve riesgo, probabilidad, rasgos y máscara |

## Desarrollo

Se levanta junto al resto con `docker compose up` desde la raíz. En local:

```bash
pip install -r requirements.txt
# PyTorch CPU (evita descargar CUDA):
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
uvicorn app.main:app --reload --port 8002
```

> Estado: **stub**. Preprocesamiento, segmentación y modelo se implementan en el bloque 3 del plan.
