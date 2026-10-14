"""MS2 · Procesamiento de imagen e IA.

Expone, según el contrato (tarea 1.4):
  - POST /analyze  -> recibe una imagen y devuelve riesgo, probabilidad,
                      rasgos clínicos y máscara de segmentación.

Por ahora es un stub: valida la imagen y devuelve una respuesta con la
estructura del contrato. El preprocesamiento, la segmentación y el modelo
CNN llegan en el bloque 3 (tareas 3.1-3.7).
"""
import os

from fastapi import FastAPI, File, HTTPException, UploadFile

app = FastAPI(
    title="Acralis AI · MS2 Procesamiento",
    description="Preprocesamiento de imagen, segmentación y modelo de IA.",
    version="0.0.1",
)

MODEL_VERSION = os.getenv("MODEL_VERSION", "0.0.0-dev")
ALLOWED_TYPES = {"image/jpeg", "image/png"}


@app.get("/health")
def health() -> dict:
    """Healthcheck del servicio."""
    return {"status": "ok", "service": "ms2-procesamiento", "model_version": MODEL_VERSION}


@app.post("/analyze")
async def analyze(image: UploadFile = File(...)) -> dict:
    """Analiza una imagen de lesión acral (stub).

    Devuelve la estructura del contrato con la versión del modelo que la generó.
    """
    if image.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=415,
            detail=f"Formato no soportado: {image.content_type}. Usa JPEG o PNG.",
        )

    # TODO (bloque 3): preprocesar -> segmentar -> inferir con el modelo CNN.
    return {
        "risk": None,              # "low" | "medium" | "high"
        "probability": None,       # 0.0 - 1.0 (melanoma)
        "features": {
            "asymmetry": None,
            "border": None,
            "color_variety": None,
            "parallel_ridges": None,
            "hutchinson_sign": None,
        },
        "mask": None,              # máscara de segmentación (base64 / ref)
        "model_version": MODEL_VERSION,
        "source": "stub",
    }
