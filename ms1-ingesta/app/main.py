"""MS1 · Ingesta genómica y bibliográfica.

Expone, según el contrato (tarea 1.4):
  - GET /markers      -> marcadores genómicos (TCGA/GDC) por gen y subtipo
  - GET /literature   -> referencias bibliográficas (Scopus)

Por ahora son stubs con datos de ejemplo. La implementación real de los
conectores llega en el bloque 4 (tareas 4.1-4.3).
"""
from fastapi import FastAPI

app = FastAPI(
    title="Acralis AI · MS1 Ingesta",
    description="Ingesta genómica (TCGA/GDC) y bibliográfica (Scopus).",
    version="0.0.1",
)


@app.get("/health")
def health() -> dict:
    """Healthcheck del servicio."""
    return {"status": "ok", "service": "ms1-ingesta"}


@app.get("/markers")
def markers() -> dict:
    """Marcadores genómicos asociados al melanoma acral (stub)."""
    return {
        "subtype": "acral-lentiginous-melanoma",
        "markers": [
            {"gene": "KIT", "frequency": None, "references": []},
            {"gene": "NRAS", "frequency": None, "references": []},
            {"gene": "BRAF", "frequency": None, "references": []},
            {"gene": "CCND1", "frequency": None, "references": []},
            {"gene": "NF1", "frequency": None, "references": []},
        ],
        "source": "stub",
        "version": "0.0.1",
    }


@app.get("/literature")
def literature(query: str = "acral lentiginous melanoma") -> dict:
    """Referencias bibliográficas sobre el melanoma acral (stub)."""
    return {
        "query": query,
        "results": [],
        "source": "stub",
        "version": "0.0.1",
    }
