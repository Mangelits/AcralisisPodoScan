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
| Preentreno general de melanoma | HAM10000 | 🟡 opcional, baja prioridad |

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

Cifras verificadas en `derm12345_supplemental.csv` (columna `label`) el 2026-10-21.

| Subclase | `label` | Mapeo a nuestra clase | Imágenes (train / test) |
|---|---|---|---:|
| Melanoma acral lentiginoso (ALM) | `alm` | Sospechoso de melanoma | 60 |
| Melanoma acral nodular (ANM) | `anm` | Sospechoso de melanoma | 76 |
| **Subtotal melanoma acral maligno** | | | **136** |
| Nevus acral juncional | `ajb` | Benigno | 426 (340 / 86) |
| Nevus acral displásico juncional | `ajd` | Benigno | 288 (230 / 58) |
| Nevus acral compuesto | `acb` | Benigno | 37 (30 / 7) |
| Nevus acral displásico compuesto | `acd` | Benigno | 9 (7 / 2) |
| **Subtotal nevus acral benigno** | | | **760** |
| **Total acral** | | | **896** |

El total coincide con `anatom_site_general = palms/soles` en `derm12345.csv`.
Los nevus acrales pertenecen a 330 pacientes distintos.

**Descarga:** `python3 scripts/datasets/download_derm12345.py` baja solo estas
896 imágenes (en vez del bundle de 1,9 GB) a `data/raw/derm12345/` y genera
`acral.csv` con `patient_id` y el split original del paper.

#### Notas y riesgos

- **Clase minoritaria crítica:** solo 136 melanomas acrales malignos → apoyarse
  en aumento de datos (tarea 2.4) y pesos por clase; combinar con más fuentes.
- **Los 136 melanomas son solo 24 pacientes** (16 en el train del paper, 8 en el
  test; un paciente aporta 22 imágenes). En la práctica hay ~24 casos
  independientes de melanoma → un único split train/test es muy ruidoso. Se
  evalúa con validación cruzada repetida por paciente
  (`notebooks/03_repeated_cv_derm12345.ipynb`). Conseguir más **pacientes** con
  melanoma acral es la prioridad de datos.
- **Posible atajo de cámara:** 8 de los 28 melanomas del test son de 3264×2448,
  una resolución que en train es casi siempre nevus. Se vigila con métricas por
  cámara en el notebook 03.
- **Huecos:** no incluye hematoma/traumatismo ni lesiones ungueales/subungueales.
- **Duplicados:** es subconjunto de ISIC; si se descarga ISIC por separado,
  controlar duplicados en la limpieza (tarea 2.2).
- **Sesgo:** población de un país/centro → anotar en "sesgos conocidos" (tarea 2.5).
- **Sesgo de recorte (atajo), detectado 2026-10-21:** las imágenes con tamaño de
  cámara habitual (768×576, 3264×2448, 4032×3024, 1920×1080, 2048×1536) son casi
  todas nevus; las de tamaño irregular (recortadas a mano) son mayoritariamente
  melanomas. Un modelo puede aprender "recortada = melanoma" en vez de la lesión.
  Además el reparto cambia entre splits:

  | Split | Melanomas recortados | Nevus recortados |
  |---|---:|---:|
  | train | 75 / 108 (69 %) | 40 / 607 (7 %) |
  | test | 3 / 28 (11 %) | 12 / 153 (8 %) |

  **Mitigación:** todas las imágenes pasan por el mismo recorte cuadrado centrado
  en la lesión (`ms2-procesamiento/app/preprocessing.py`) y se reportan métricas
  por subgrupo estándar/recortada (`notebooks/02_baseline_v2_derm12345.ipynb`).

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

### 3. HAM10000 — *opcional, baja prioridad*

- **Origen:** Tschandl, Rosendahl & Kittler. Benchmark clásico de lesiones
  pigmentadas comunes, multi-fuente. Base de muchas colecciones de ISIC.
- **Referencia:** Tschandl, P., Rosendahl, C. & Kittler, H. *The HAM10000 dataset…*
  **Scientific Data** 5, 180161 (2018).
- **Modalidad:** imágenes dermatoscópicas (PNG). ~**10.015 imágenes**.
- **Clases y conteos:** nv 6.705 · **mel 1.113** · bkl 1.099 · bcc 514 ·
  akiec 327 · vasc 142 · df 115.
- **Localización:** el CSV de metadatos incluye el campo `localization` con el
  valor `acral` (y `foot`, `hand`) → filtrable, pero con **muy pocos casos acrales**
  (cifra exacta **a verificar en el CSV**).
- **Licencia:** ⚠️ **verificar en origen.** El HAM10000 **oficial**
  (Harvard Dataverse / ISIC) es **CC BY-NC 4.0 (no comercial)**. El registro de
  Zenodo indicado es un **re-archivo de un tercero** que declara CC BY 4.0 →
  usar la fuente oficial y asumir CC BY-NC salvo confirmación.
- **Enlaces:**
  - Zenodo (re-archivo): https://zenodo.org/records/17702692
  - Fuente oficial (Harvard Dataverse): https://doi.org/10.7910/DVN/DBW86T
  - Paper: https://doi.org/10.1038/sdata.2018.161

#### Por qué baja prioridad

- **No es acral-específico:** subconjunto acral mínimo; aporta poco al cuello de
  botella de melanoma acral.
- **Solapamiento/duplicados:** es una de las bases de ISIC; DERM12345 y BCN20000
  ya son derivados de ISIC → alto riesgo de imágenes repetidas entre los tres.
  Dedup obligatorio y control de que una lesión no caiga en train y test (tareas 2.2, 2.3).
- **No cubre** trauma/hematoma ni lesiones ungueales como tales.
- **Uso razonable:** solo como bolsa de **preentreno general** de melanoma, desde
  la fuente oficial y con dedup estricto.

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
