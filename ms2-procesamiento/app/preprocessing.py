"""Preprocesamiento de imagen compartido por entrenamiento e inferencia (tarea 3.1).

`lesion_crop` recorta un cuadrado centrado en la lesión, con la lesión ocupando
una fracción parecida del recorte en todas las imágenes. Así el modelo no puede
aprender atajos como "imagen recortada a mano = melanoma" (ver sesgos en
docs/datasets.md): todas las entradas tienen la misma forma y escala relativa.

Es una heurística clásica (Otsu sobre la luminancia), no una segmentación
precisa; la U-Net de la tarea 3.2 la sustituirá si hace falta. Si no encuentra
una lesión plausible, devuelve el cuadrado central de la imagen.
"""
from dataclasses import dataclass
from math import hypot

import cv2
import numpy as np

DETECT_SIZE = 256        # lado largo de la imagen reducida para detectar
VIGNETTE_LEVEL = 30      # luminancia por debajo = viñeta negra del dermatoscopio
MIN_AREA_FRAC = 0.005    # componentes más pequeños se descartan (ruido, pelos)


@dataclass
class CropInfo:
    found: bool                          # False → se usó el cuadrado central
    bbox: tuple[int, int, int, int] | None  # lesión detectada (x, y, w, h) en píxeles originales
    box: tuple[int, int, int]            # recorte aplicado (x0, y0, lado)


def find_lesion_bbox(rgb: np.ndarray) -> tuple[int, int, int, int] | None:
    """Caja (x, y, w, h) de la lesión más plausible, o None si no hay ninguna."""
    h, w = rgb.shape[:2]
    scale = DETECT_SIZE / max(h, w)
    small = cv2.resize(rgb, (max(1, round(w * scale)), max(1, round(h * scale))),
                       interpolation=cv2.INTER_AREA)
    gray = cv2.GaussianBlur(cv2.cvtColor(small, cv2.COLOR_RGB2GRAY), (5, 5), 0)

    # Píxeles útiles: fuera de la viñeta negra y algo alejados de su borde.
    valid = cv2.erode((gray > VIGNETTE_LEVEL).astype(np.uint8), np.ones((7, 7), np.uint8))
    if valid.sum() < 0.2 * valid.size:
        return None

    # Otsu solo sobre los píxeles útiles: la lesión es la parte oscura.
    threshold, _ = cv2.threshold(gray[valid.astype(bool)].reshape(-1, 1), 0, 255,
                                 cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    mask = ((gray < threshold) & valid.astype(bool)).astype(np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))

    # Entre los componentes, preferir grandes y cercanos al centro.
    n, _, stats, centroids = cv2.connectedComponentsWithStats(mask)
    sh, sw = gray.shape
    half_diag = hypot(sh, sw) / 2
    best, best_score = None, 0.0
    for i in range(1, n):
        area = stats[i, cv2.CC_STAT_AREA]
        if area < MIN_AREA_FRAC * mask.size:
            continue
        dist = hypot(centroids[i][0] - sw / 2, centroids[i][1] - sh / 2) / half_diag
        score = area * (1 - dist) ** 2
        if score > best_score:
            best, best_score = i, score
    if best is None:
        return None

    x, y, bw, bh = stats[best, :4]
    return tuple(int(round(v / scale)) for v in (x, y, bw, bh))


def lesion_crop(rgb: np.ndarray, margin: float = 1.5,
                min_side_frac: float = 0.35) -> tuple[np.ndarray, CropInfo]:
    """Recorte cuadrado centrado en la lesión.

    margin:        lado del recorte = margin × lado mayor de la lesión.
    min_side_frac: lado mínimo, como fracción del lado corto de la imagen
                   (evita ampliar en exceso lesiones diminutas o falsas detecciones).
    """
    h, w = rgb.shape[:2]
    short = min(h, w)
    bbox = find_lesion_bbox(rgb)
    if bbox is None:
        cx, cy, side = w / 2, h / 2, short
    else:
        x, y, bw, bh = bbox
        cx, cy = x + bw / 2, y + bh / 2
        side = min(max(max(bw, bh) * margin, min_side_frac * short), short)

    side = int(round(side))
    x0 = int(round(min(max(cx - side / 2, 0), w - side)))
    y0 = int(round(min(max(cy - side / 2, 0), h - side)))
    crop = rgb[y0:y0 + side, x0:x0 + side]
    return crop, CropInfo(found=bbox is not None, bbox=bbox, box=(x0, y0, side))
