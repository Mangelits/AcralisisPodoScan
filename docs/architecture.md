# Arquitectura · Acralis AI

> Documento vivo. Se completa en la tarea 1.5 del plan (diagrama C4, flujo de
> datos y ADRs).

## Microservicios

| Servicio | Responsabilidad | Tecnología | Puerto (dev) |
|---|---|---|---|
| **MS1 · Ingesta** | Conectores Scopus (bibliografía) y TCGA/GDC (genómica) | Python · FastAPI | 8001 |
| **MS2 · Procesamiento** | Preprocesamiento, segmentación y modelo CNN | Python · FastAPI · OpenCV · PyTorch | 8002 |
| **MS3 · Frontend** | Interfaz clínica accesible (WCAG 2.2 AA) | Vite · JavaScript | 5173 |
| **Firebase** | Auth, Firestore, Storage, Hosting | Firebase (emuladores en local) | 4000/8080/9099/9199 |

El **orquestador / API Gateway** (tarea 5.1) coordina la subida de imagen, la
llamada a MS2 y el guardado del resultado en Firestore. Se incorpora en el
bloque 5.

## Flujo de datos (resumen)

1. El podólogo sube una foto de la lesión desde MS3.
2. La imagen se guarda en Cloud Storage.
3. El orquestador detecta la subida y llama a `MS2 /analyze`.
4. MS2 preprocesa, segmenta e infiere → devuelve riesgo + probabilidad + rasgos.
5. El resultado se guarda en Firestore y se muestra en el visor (MS3).
6. En caso de riesgo, se genera el paquete de derivación con marcadores de MS1.

## Contratos

Ver `docs/contracts/` (OpenAPI de MS1 y MS2, tarea 1.4).

## Modelo de datos (Firestore)

Colecciones previstas: `patients`, `lesions`, `captures`, `referrals`
(tarea 1.4).
