"""Descarga el subconjunto acral de DERM12345 desde el ISIC Archive (tarea 2.1).

En vez del bundle completo (~1,9 GB), baja solo las imágenes acrales
(palmas/plantas) imagen a imagen, en paralelo y de forma reanudable:
si se corta, volver a lanzarlo continúa donde se quedó.

Uso (desde la raíz del repo):
    python3 scripts/datasets/download_derm12345.py
    # Si ya tienes el bundle completo (derm12345.zip), extrae de él sin red:
    python3 scripts/datasets/download_derm12345.py --zip data/raw/derm12345/derm12345.zip

Resultado en data/raw/derm12345/ (ignorado por git):
    derm12345.csv               metadatos ISIC (incluye patient_id)
    derm12345_supplemental.csv  etiquetas del paper (label, split, sub_class)
    acral.csv                   subconjunto acral con ruta local de cada imagen
    images/ISIC_xxxxxxx.jpg

Licencia: CC BY 4.0 — citar Yilmaz et al., Sci Data 11, 1302 (2024).
Solo usa la librería estándar.
"""
import argparse
import csv
import json
import sys
import time
import urllib.request
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

DOI_BASE = "https://isic-archive.s3.amazonaws.com/dois/10.34970-705541"
CSV_FILES = {
    "derm12345.csv": f"{DOI_BASE}/derm12345.csv",
    "derm12345_supplemental.csv": f"{DOI_BASE}/supplements/derm12345_supplemental.csv",
}
IMAGE_API = "https://api.isic-archive.com/api/v2/images/{}/"

# Etiquetas acrales del CSV suplementario.
ACRAL_LABELS = {
    "acb": "nevus acral compuesto",
    "acd": "nevus acral displásico compuesto",
    "ajb": "nevus acral juncional",
    "ajd": "nevus acral displásico juncional",
    "alm": "melanoma acral lentiginoso",
    "anm": "melanoma acral nodular",
}

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = ROOT / "data" / "raw" / "derm12345"


def fetch(url: str, timeout: int = 60) -> bytes:
    """GET con reintentos y espera exponencial."""
    for attempt in range(5):
        try:
            with urllib.request.urlopen(url, timeout=timeout) as resp:
                return resp.read()
        except Exception:
            if attempt == 4:
                raise
            time.sleep(2 ** attempt)
    raise RuntimeError("inalcanzable")


def download_csvs(out: Path) -> None:
    for name, url in CSV_FILES.items():
        path = out / name
        if path.exists() and path.stat().st_size > 0:
            continue
        print(f"Descargando {name}…")
        tmp = path.with_suffix(".part")
        tmp.write_bytes(fetch(url))
        tmp.rename(path)


def extract_csvs(zf: zipfile.ZipFile, out: Path) -> None:
    """Copia los CSV del bundle con los mismos nombres que la descarga directa."""
    for member, name in (("metadata.csv", "derm12345.csv"),
                         ("supplements/derm12345_supplemental.csv", "derm12345_supplemental.csv")):
        (out / name).write_bytes(zf.read(member))


def extract_image(zf: zipfile.ZipFile, isic_id: str, images_dir: Path) -> Path:
    member = f"images/{isic_id}.jpg"
    path = images_dir / f"{isic_id}.jpg"
    if not (path.exists() and path.stat().st_size == zf.getinfo(member).file_size):
        path.write_bytes(zf.read(member))
    return path


def download_image(isic_id: str, images_dir: Path) -> tuple[str, Path]:
    """Descarga una imagen; la salta si ya existe con el tamaño esperado."""
    meta = json.loads(fetch(IMAGE_API.format(isic_id)))
    full = meta["files"]["full"]
    path = images_dir / f"{isic_id}{Path(full['url']).suffix}"
    if path.exists() and path.stat().st_size == full["size"]:
        return isic_id, path
    data = fetch(full["url"], timeout=300)
    if len(data) != full["size"]:
        raise IOError(f"{isic_id}: tamaño {len(data)} != {full['size']}")
    tmp = path.with_suffix(".part")
    tmp.write_bytes(data)
    tmp.rename(path)
    return isic_id, path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--zip", type=Path, help="bundle derm12345.zip local; evita la red")
    args = parser.parse_args()

    out: Path = args.out
    images_dir = out / "images"
    images_dir.mkdir(parents=True, exist_ok=True)
    zf = zipfile.ZipFile(args.zip) if args.zip else None
    if zf:
        extract_csvs(zf, out)
    else:
        download_csvs(out)

    with open(out / "derm12345_supplemental.csv", newline="") as f:
        supp = {r["isic_id"]: r for r in csv.DictReader(f) if r["label"] in ACRAL_LABELS}
    with open(out / "derm12345.csv", newline="") as f:
        isic = {r["isic_id"]: r for r in csv.DictReader(f) if r["isic_id"] in supp}
    print(f"{len(supp)} imágenes acrales a obtener en {images_dir}")

    paths: dict[str, Path] = {}
    failed: list[str] = []
    if zf:
        for isic_id in supp:
            try:
                paths[isic_id] = extract_image(zf, isic_id, images_dir)
            except KeyError:
                failed.append(isic_id)
                print(f"  ✗ {isic_id}: no está en el ZIP", file=sys.stderr)
    else:
        download_all(supp, images_dir, args.workers, paths, failed)

    write_acral_csv(out, supp, isic, paths)
    print(f"Hecho: {len(paths)} OK, {len(failed)} fallidas → {out / 'acral.csv'}")
    if failed:
        print("Vuelve a ejecutar el script para reintentar las fallidas.")
    return 1 if failed else 0


def download_all(supp: dict, images_dir: Path, workers: int,
                 paths: dict[str, Path], failed: list[str]) -> None:
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(download_image, i, images_dir): i for i in supp}
        for n, fut in enumerate(as_completed(futures), 1):
            isic_id = futures[fut]
            try:
                paths[isic_id] = fut.result()[1]
            except Exception as exc:
                failed.append(isic_id)
                print(f"  ✗ {isic_id}: {exc}", file=sys.stderr)
            if n % 25 == 0 or n == len(futures):
                print(f"  {n}/{len(futures)}", flush=True)


def write_acral_csv(out: Path, supp: dict, isic: dict, paths: dict[str, Path]) -> None:
    fields = ["isic_id", "file", "label", "label_desc", "malignancy",
              "patient_id", "study_patient_id", "split", "copyright_license"]
    with open(out / "acral.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for isic_id in sorted(paths):
            s, m = supp[isic_id], isic.get(isic_id, {})
            writer.writerow({
                "isic_id": isic_id,
                "file": paths[isic_id].relative_to(out).as_posix(),
                "label": s["label"],
                "label_desc": ACRAL_LABELS[s["label"]],
                "malignancy": s["malignancy"],
                "patient_id": m.get("patient_id", ""),
                "study_patient_id": s["study_patient_id"],
                "split": s["split"],
                "copyright_license": m.get("copyright_license", ""),
            })


if __name__ == "__main__":
    sys.exit(main())
