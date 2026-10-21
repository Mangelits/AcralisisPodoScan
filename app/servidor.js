
const express = require("express");
const ort = require("onnxruntime-node");
const path = require("path");
const fs = require("fs");

const app = express();
app.use(express.json());

// Configuración
const PORT = 7000;
const modelPath = path.join(__dirname, "modelo", "modelo.onnx");
const normPath = path.join(__dirname, "modelo", "normalizacion.json");

// Cargar parámetros de normalización
const norm = JSON.parse(fs.readFileSync(normPath, "utf8"));

let session;

// Endpoint de predicción
app.post("/predict", async (req, res) => {
    try {
        const { features } = req.body || {};

        // Comprobar que recibimos los datos esperados
        if (
            !Array.isArray(features) ||
            features.length !== norm.mean.length ||
            !features.every(v => typeof v === "number" && Number.isFinite(v))
        ) {
            return res.status(400).json({
                error: `Se esperan ${norm.mean.length} valores numéricos`,
                orden: norm.features
            });
        }

        // 1. Normalización
        const datos = features.map((valor, i) =>
            (valor - norm.mean[i]) / norm.scale[i]
        );

        // 2. Convertir a tensor float32
        const tensor = new ort.Tensor(
            "float32",
            Float32Array.from(datos),
            [1, datos.length]
        );

        // 3. Ejecutar el modelo ONNX
        const resultado = await session.run({
            [session.inputNames[0]]: tensor
        });

        // 4. Obtener predicción
        const prediccion =
            resultado[session.outputNames[0]].data[0];

        // 5. Responder al cliente
        res.json({
            consumo_predicho: prediccion
        });

    } catch (error) {
        console.error(error);
        res.status(500).json({
            error: "Error al ejecutar la predicción"
        });
    }
});

// Endpoint para consultar las variables de entrada
app.get("/features", (req, res) => {
    res.json({
        features: norm.features
    });
});

// Inicializar modelo y servidor
async function iniciar() {
    session = await ort.InferenceSession.create(modelPath);

    console.log("Modelo ONNX cargado");
    console.log("Entrada:", session.inputNames);
    console.log("Salida:", session.outputNames);

    app.listen(PORT, () => {
        console.log(`Servidor en http://localhost:${PORT}`);
    });
}

iniciar().catch(error => {
    console.error("Error al cargar el modelo:", error);
    process.exit(1);
});
