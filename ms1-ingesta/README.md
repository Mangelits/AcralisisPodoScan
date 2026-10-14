# MS1 · Ingesta

Microservicio de ingesta de datos genómicos y bibliográficos.

- **Genómica:** conector contra el Genomic Data Commons (TCGA/GDC) — mutaciones en *KIT*, *NRAS*, *BRAF*, *CCND1*, *NF1* (tarea 4.1).
- **Bibliografía:** conector contra Scopus — literatura sobre melanoma acral lentiginoso (tarea 4.2).

## Endpoints (contrato · tarea 1.4)

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/health` | Healthcheck |
| GET | `/markers` | Marcadores genómicos por gen y subtipo |
| GET | `/literature` | Referencias bibliográficas |

## Desarrollo

Se levanta junto al resto con `docker compose up` desde la raíz. En local:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

> Estado: **stub**. Los conectores reales se implementan en el bloque 4 del plan.
