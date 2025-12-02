# Requirements Document

## Introduction

Este documento describe los requisitos para solucionar el problema URGENTE en producción donde la página de predicciones ML aparece en blanco cuando el usuario intenta ejecutar predicciones. El problema está relacionado con la versión del modelo de Machine Learning, errores no manejados en el frontend, y posibles problemas con la carga del modelo en el entorno de producción (Railway).

## Glossary

- **ML System**: Sistema de Machine Learning que genera predicciones de fallos para activos
- **Prediction Service**: Servicio backend que ejecuta el modelo ML y genera predicciones
- **Frontend**: Aplicación React desplegada en Vercel que muestra las predicciones al usuario
- **Backend**: API Django desplegada en Railway que procesa las predicciones
- **API Endpoint**: Punto de acceso REST que permite ejecutar predicciones
- **Error Handler**: Componente que maneja errores y muestra mensajes apropiados al usuario
- **Production Environment**: Entorno de producción en Railway (backend) y Vercel (frontend)

## Requirements

### Requirement 1

**User Story:** Como usuario del sistema en producción, quiero que la página de predicciones ML maneje errores correctamente, para que pueda ver mensajes informativos en lugar de una página en blanco cuando algo falla.

#### Acceptance Criteria

1. WHEN el API retorna un error durante la ejecución de predicciones THEN el Frontend SHALL capturar el error y mostrar un mensaje específico al usuario
2. WHEN ocurre un error de red o timeout THEN el Frontend SHALL mostrar un mensaje indicando el problema de conexión
3. WHEN el modelo ML no está disponible o tiene problemas THEN el Frontend SHALL mostrar un mensaje indicando que el modelo necesita ser reentrenado o verificado
4. WHEN la respuesta del API es exitosa THEN el Frontend SHALL actualizar la lista de predicciones correctamente sin causar errores de renderizado
5. WHEN hay predicciones existentes THEN el Frontend SHALL mostrarlas en la tabla sin errores de JavaScript

### Requirement 2

**User Story:** Como desarrollador, quiero que el backend en Railway maneje errores del modelo ML de forma robusta, para que el sistema retorne respuestas HTTP apropiadas en lugar de fallar silenciosamente.

#### Acceptance Criteria

1. WHEN el modelo ML no puede cargarse en Railway THEN el Backend SHALL retornar un error HTTP 500 con un mensaje JSON descriptivo
2. WHEN el modelo ML genera una excepción durante la predicción THEN el Backend SHALL capturar la excepción y retornar un error HTTP 500 con detalles
3. WHEN no hay activos para predecir THEN el Backend SHALL retornar HTTP 200 con un mensaje indicando que no hay datos
4. WHEN las predicciones se ejecutan exitosamente THEN el Backend SHALL retornar un código HTTP 202 con el ID de la tarea Celery
5. WHEN se consultan las predicciones THEN el Backend SHALL retornar HTTP 200 con la lista completa incluyendo todos los campos requeridos por el Frontend

### Requirement 3

**User Story:** Como administrador del sistema en producción, quiero logs detallados de errores en Railway, para que pueda diagnosticar y solucionar problemas rápidamente usando `railway logs`.

#### Acceptance Criteria

1. WHEN ocurre un error en el servicio de predicciones THEN el Backend SHALL registrar el error completo en los logs de Railway
2. WHEN se ejecutan predicciones THEN el Backend SHALL registrar el inicio y fin de la operación con timestamps
3. WHEN el modelo ML falla al cargar o ejecutar THEN el Backend SHALL registrar el stack trace completo y la ruta del archivo del modelo
4. WHEN hay problemas con los datos de entrada THEN el Backend SHALL registrar los datos que causaron el problema sin exponer información sensible
5. WHEN se consultan los logs con `railway logs` THEN el sistema SHALL mostrar información suficiente para diagnosticar el problema

### Requirement 4

**User Story:** Como usuario, quiero que el sistema valide que el modelo ML está disponible en Railway antes de ejecutar predicciones, para que no pierda tiempo esperando una operación que va a fallar.

#### Acceptance Criteria

1. WHEN el usuario intenta ejecutar predicciones THEN el Backend SHALL verificar que el archivo del modelo ML existe en Railway
2. WHEN el modelo ML no está disponible THEN el Backend SHALL retornar HTTP 503 con un mensaje indicando que debe reentrenarse
3. WHEN el modelo ML está disponible THEN el Backend SHALL permitir ejecutar las predicciones y retornar HTTP 202
4. WHEN se carga la página de predicciones THEN el Frontend SHALL hacer una llamada al Backend para verificar el estado del modelo ML
5. WHEN el modelo ML tiene una versión incompatible THEN el Backend SHALL retornar HTTP 500 con un mensaje indicando que debe actualizarse

### Requirement 5

**User Story:** Como desarrollador, quiero un endpoint de health check para el modelo ML, para que pueda verificar rápidamente si el modelo está disponible y funcionando en producción.

#### Acceptance Criteria

1. WHEN se llama al endpoint de health check THEN el Backend SHALL verificar que el archivo del modelo existe
2. WHEN el modelo está disponible THEN el Backend SHALL retornar HTTP 200 con información de la versión del modelo
3. WHEN el modelo no está disponible THEN el Backend SHALL retornar HTTP 503 con detalles del problema
4. WHEN el modelo está corrupto THEN el Backend SHALL retornar HTTP 500 con detalles del error
5. WHEN se consulta el health check THEN el Backend SHALL retornar el tiempo de respuesta de carga del modelo
