# ADR 0001 · Microservicios con Docker y Firebase

- **Estado:** aceptado
- **Fecha:** 2026-10-14

## Contexto

Acralis AI combina procesamiento de imagen/IA, ingesta de datos externos
(genómica y bibliografía) y una interfaz clínica. Son responsabilidades muy
distintas en lenguaje, dependencias y ritmo de cambio.

## Decisión

- **Arquitectura de microservicios** (MS1 ingesta, MS2 procesamiento/IA, MS3
  frontend) con separación estricta de responsabilidades.
- **Docker + docker-compose** para empaquetar y orquestar en local con un solo
  comando.
- **Firebase** (Auth, Firestore, Storage, Hosting) como backend de datos y
  despliegue del frontend, priorizando el **plan gratuito (Spark)**.

## Consecuencias

- Cada servicio evoluciona y se prueba de forma aislada.
- Los contratos entre servicios (OpenAPI, tarea 1.4) son críticos.
- **Limitación del plan gratuito:** Cloud Run/Functions requieren el plan
  Blaze. La estrategia de despliegue de los microservicios en gratuito se
  decide en el Sprint 10 (tarea 10.1); en desarrollo todo corre en local con
  emuladores.
