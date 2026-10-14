# Inventario de datasets · Acralis AI

> Subtarea 2.1 "Inventario" del plan. Registro de fuentes de datos candidatas
> y confirmadas, con número de imágenes por clase, origen y licencia.
> Documento vivo: se actualiza conforme se localizan y curan nuevas fuentes.

## Esquema de clases objetivo (tarea 2.2)

| Clase | Descripción |
|---|---|
| **Benigno** | Nevus acral y otras lesiones pigmentadas benignas |
| **Traumatismo / hematoma** | Hematoma subungueal, lesiones por fricción/trauma |
| **Sospechoso de melanoma** | Melanoma acral lentiginoso (ALM), nodular (ANM), subungueal |

## Resumen de cobertura

| Necesidad | Fuente(s) | Estado |
|---|---|---|
| Melanoma acral (planta) | DERM12345 | ✅ confirmada |
| Nevus acral benigno | DERM12345 | ✅ confirmada |
| Melanoma subungueal / lesiones ungueales | — | 🔎 por buscar |
| Hematoma / traumatismo | — | 🔎 por buscar |

---

## Fuentes confirmadas

### 1. DERM12345

- **Origen:** ISIC Archive (colección DERM12345). Imágenes recogidas en Turquía.
- **Referencia:** Yilmaz, A., Yasar, S. P., Gencoglan, G. et al. *DERM12345: A Large,
  Multisource Dermatoscopic Skin Lesion Dataset with 40 Subclasses.*
  **Scientific Data** 11, 1302 (2024).
- **Modalidad:** imágenes dermatoscópicas, alta resolución (hasta 4K), JPEG.
- **Tamaño total:** 12.345 imágenes · 5 superclases / 15 clases / 40 subclases.
- **Licencia:** **CC BY 4.0** (requiere atribución; citar el artículo).
- **Acceso:** descarga desde el ISIC Archive (bundle ~1,7 GB) + CSV de metadatos
  y CSV con splits train/test y etiquetas diagnósticas.
- **Enlaces:**
  - Repo: https://github.com/abdurrahimyilmaz/derm12345
  - Colección ISIC: https://api.isic-archive.com/doi/derm12345/
  - Paper (PMC): https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11604664/
  - arXiv: https://arxiv.org/abs/2406.07426

#### Imágenes acrales (relevantes para el proyecto)

| Subclase | Mapeo a nuestra clase | Imágenes |
|---|---|---:|
| Melanoma acral lentiginoso (ALM) | Sospechoso de melanoma | 54 |
| Melanoma acral nodular (ANM) | Sospechoso de melanoma | 78 |
| **Subtotal melanoma acral maligno** | | **132** |
| Nevus acral juncional | Benigno | 351 |
| Nevus acral displásico juncional | Benigno | 212 |
| Nevus acral compuesto | Benigno | 22 |
| Nevus acral displásico compuesto | Benigno | 8 |
| **Subtotal nevus acral benigno** | | **~593** |
| **Total acral** | | **~725** |

#### Notas y riesgos

- **Clase minoritaria crítica:** solo 132 melanomas acrales malignos → apoyarse
  en aumento de datos (tarea 2.4) y pesos por clase; combinar con más fuentes.
- **Huecos:** no incluye hematoma/traumatismo ni lesiones ungueales/subungueales.
- **Duplicados:** es subconjunto de ISIC; si se descarga ISIC por separado,
  controlar duplicados en la limpieza (tarea 2.2).
- **Sesgo:** población de un país/centro → anotar en "sesgos conocidos" (tarea 2.5).

---

## Fuentes candidatas (por evaluar)

| Fuente | Qué aportaría | Licencia | Estado |
|---|---|---|---|
| ISIC Archive (consulta directa, filtro acral/palmoplantar) | Más imágenes acrales | variable por colección | 🔎 por evaluar |
| Datasets/artículos de melanoma subungueal | Lesiones ungueales | por confirmar | 🔎 por buscar |
| Imágenes de hematoma subungueal / traumatismo | Clase traumatismo | por confirmar | 🔎 por buscar |
| Contacto clínico (clínicas/hospitales colaboradores) | Imágenes anonimizadas reales | acuerdo específico | ✉️ pedir pronto (subtarea 2.1) |

---

_Última actualización: 2026-10-14._
