# Acralis AI

**Plataforma Bioinformática y de Visión Artificial para el Triaje y Detección Temprana del Melanoma Acral Lentiginoso.**

> ⚠️ Software de soporte a la decisión clínica (SaMD). **No diagnostica**: realiza un triaje inteligente para agilizar la derivación y la biopsia.

## Descripción

Acralis AI es una aplicación web basada en microservicios diseñada para cerrar la brecha diagnóstica entre la atención podológica y la oncología especializada.

Evalúa lesiones pigmentadas en la planta del pie o el lecho subungueal, diferenciando entre traumatismos comunes y posibles melanomas acrales. Para ello:

1. Ingiere imágenes subidas por el clínico en tiempo real.
2. Las procesa mediante modelos de aprendizaje profundo (CNN).
3. Cruza el análisis morfológico con bases de datos genómicas (**TCGA**) y literatura médica actualizada (**Scopus**).
4. Genera un informe interactivo, accesible y estandarizado que:
   - alerta al podólogo sobre el **nivel de riesgo**;
   - proporciona al oncólogo un **perfil preliminar de mutaciones asociadas** (p. ej. *KIT*, *CCND1*) y guías clínicas.

## Arquitectura

| Microservicio | Responsabilidad | Tecnología |
|---|---|---|
| **MS1 – Ingesta** | Rutinas automatizadas vía REST contra Scopus y repositorios genómicos (TCGA) | Docker |
| **MS2 – Procesamiento** | Filtrado y limpieza de imágenes (eliminación de ruido, segmentación del pie) y modelo de IA | Python, Docker |
| **MS3 – Visor de resultados** | Interfaz clínica accesible (WCAG) | JavaScript, Docker |
| **Datos y despliegue** | Ingesta temporal de fotografías y registro longitudinal de pacientes | Firebase (Cloud Storage, Firestore) |

## Pilares del desarrollo

### 1. Enfoque clínico-técnico
Resolver un problema de flujo de trabajo hospitalario. El algoritmo analiza la imagen (asimetrías, signo de Hutchinson) y, en caso de riesgo, el backend prepara automáticamente un **paquete de derivación** con los marcadores genómicos que la literatura (TCGA) sugiere buscar en la biopsia.

### 2. Arquitectura (backend, APIs y procesamiento)
Separación estricta de responsabilidades mediante contenedores Docker para garantizar escalabilidad.

### 3. Frontend y accesibilidad
Interfaz rápida y clara, utilizable en situaciones de estrés o con mala iluminación:
- Cumplimiento estricto de **WCAG**.
- Modo oscuro estructurado.
- Contraste de color mínimo **4.5:1**.
- Etiquetas semánticas y **ARIA** dinámicas.
- La información crítica no depende solo de mapas de calor: cada gráfico (p. ej. probabilidad de malignidad del 85 %) tiene una estructura de datos subyacente legible sin ambigüedad.

### 4. Datos y despliegue (Firebase)
- **Cloud Storage** para la ingesta temporal de fotografías de lesiones.
- **Firestore** para la evolución de los pacientes.
- Registro longitudinal: comparación de imágenes en el tiempo y cálculo automático de la **tasa de crecimiento** de la lesión.

## Estado

🚧 Proyecto en fase inicial.
