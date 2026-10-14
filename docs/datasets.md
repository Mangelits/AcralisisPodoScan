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
| Melanoma acral (planta) | DERM12345, BCN20000 | ✅ DERM12345 · 🔬 BCN20000 en evaluación |
| Nevus acral benigno | DERM12345, BCN20000 | ✅ DERM12345 · 🔬 BCN20000 en evaluación |
| Melanoma subungueal / lesiones ungueales | BCN20000 (uñas/mucosa, sin itemizar) | 🔬 en evaluación |
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

### 2. BCN20000 — *en evaluación*

- **Origen:** Hospital Clínic de Barcelona (2010–2016). Grupo de procesado de
  imagen de la UPC (imatge-upc). Dataset "dermoscopic lesions in the wild".
- **Referencia:** Hernández-Pérez, C., Combalia, M., Podlipnik, S. et al.
  *BCN20000: Dermoscopic Lesions in the Wild.* **Scientific Data** 11, 641 (2024).
- **Modalidad:** imágenes dermatoscópicas. Enfoque en **casos difíciles** y
  **localizaciones complicadas (uñas y mucosas)**, lesiones grandes e hipopigmentadas.
- **Tamaño total:** 18.946 imágenes (train 12.413 / test 6.533), 8 clases diagnósticas.
- **Licencia:** ⚠️ **a confirmar.** El README de GitHub indica CC BY-NC 4.0 (no
  comercial); el paper/Figshare menciona CC BY 4.0. Además, al formar parte de
  ISIC, cada imagen puede tener licencia propia (CC0 / CC-BY / CC-BY-NC).
  No bloquea el uso académico, pero hay que verificarlo antes de depender de él.
- **Acceso:** descarga desde Figshare (DOI 10.6084/m9.figshare.24140028); también
  presente en el ISIC Archive. Código en GitHub.
- **Enlaces:**
  - Repo: https://github.com/imatge-upc/BCN20000
  - Paper (PMC): https://pmc.ncbi.nlm.nih.gov/articles/PMC11183228/
  - Figshare: https://figshare.com/articles/journal_contribution/BCN20000_Dermoscopic_Lesions_in_the_Wild/24140028/1

#### Clases diagnósticas (conjunto de entrenamiento)

| Clase | Imágenes |
|---|---:|
| Nevus | 4.206 |
| Melanoma | 2.857 |
| Carcinoma basocelular | 2.809 |
| Queratosis benigna | 1.138 |
| Queratosis actínica | 737 |
| Carcinoma escamoso | 431 |
| Dermatofibroma | 124 |
| Vascular | 111 |

#### Localización anatómica (metadatos disponibles)

| Localización | Imágenes (train) |
|---|---:|
| **Palmas / plantas (acral)** | **380 (3%)** |
| Torso anterior | 5.086 (41%) |
| Cabeza / cuello | 3.233 (26%) |
| Extremidad inferior | 2.173 (17%) |
| Extremidad superior | 1.319 (10%) |
| Oral / genital | 59 (1%) |

#### Notas y acciones pendientes

- **Melanomas acrales reales sin desglosar:** los 380 de palmas/plantas son de
  todas las clases (mayoría nevus). **Acción:** cruzar en los metadatos
  `localización = palms/soles` **AND** `diagnóstico = melanoma` para contar los
  melanomas acrales reales (probablemente pocos).
- **Uñas/subungueal:** se abordan explícitamente pero **no vienen itemizadas** →
  inspeccionar los metadatos para localizarlas.
- **Licencia:** resolver la ambigüedad CC BY vs CC BY-NC (ver arriba).
- **Duplicados:** colección de ISIC, igual que DERM12345 → controlar solapamiento
  y duplicados en la limpieza (tarea 2.2).
- **No cubre** la clase traumatismo/hematoma.

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
