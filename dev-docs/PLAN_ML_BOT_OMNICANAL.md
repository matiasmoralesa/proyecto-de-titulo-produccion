# Plan de Implementación: ML + Bot Omnicanal

## 🎯 Objetivo
Integrar un sistema de predicción de fallos basado en ML que automáticamente asigne operadores capacitados y un bot omnicanal para notificaciones y gestión.

## 📊 Estado Actual

### ✅ Ya Implementado
- Modelos de datos para ML (MLModel, FailurePrediction, OperatorSkill, OperatorAvailability)
- Servicio de predicción básico (prediction_service.py)
- Servicio de asignación de operadores (operator_assignment_service.py)
- Feature engineering básico

### ❌ Faltante
- Entrenamiento del modelo con datos reales
- Integración automática: Predicción → Asignación → Notificación
- Bot omnicanal (WhatsApp, Telegram, Email, SMS)
- Dashboard de predicciones
- API endpoints para predicciones
- Scheduler para predicciones periódicas

## 🏗️ Arquitectura Propuesta

```
┌─────────────────────────────────────────────────────────────┐
│                    SISTEMA DE PREDICCIÓN                     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  1. RECOLECCIÓN DE DATOS HISTÓRICOS                         │
│     - Historial de mantenimiento                            │
│     - Órdenes de trabajo completadas                        │
│     - Fallos registrados                                    │
│     - Uso de activos                                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  2. FEATURE ENGINEERING                                      │
│     - Días desde último mantenimiento                       │
│     - Frecuencia de fallos                                  │
│     - Horas de operación                                    │
│     - Tipo de vehículo                                      │
│     - Edad del activo                                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  3. MODELO ML (Random Forest)                               │
│     - Entrenamiento con datos históricos                    │
│     - Predicción de probabilidad de fallo                   │
│     - Clasificación de riesgo (LOW/MEDIUM/HIGH/CRITICAL)    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  4. SISTEMA DE DECISIÓN                                     │
│     - Si riesgo >= MEDIUM: Crear orden de trabajo           │
│     - Si riesgo >= HIGH: Asignar operador automáticamente   │
│     - Si riesgo == CRITICAL: Notificación urgente           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  5. ASIGNACIÓN INTELIGENTE DE OPERADORES                    │
│     Scoring basado en:                                      │
│     - Skills (35%): Certificaciones, experiencia            │
│     - Disponibilidad (25%): Carga de trabajo actual         │
│     - Performance (25%): Historial de éxito                 │
│     - Ubicación (15%): Proximidad al activo                 │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  6. BOT OMNICANAL                                           │
│     - WhatsApp Business API                                 │
│     - Telegram Bot                                          │
│     - Email (SMTP)                                          │
│     - SMS (Twilio)                                          │
│     - Notificaciones In-App                                 │
└─────────────────────────────────────────────────────────────┘
```

## 📋 Tareas de Implementación

### Fase 1: Completar Sistema ML (2-3 días)

#### 1.1 Mejorar Feature Engineering
- [ ] Agregar más features relevantes
- [ ] Normalización de datos
- [ ] Manejo de datos faltantes

#### 1.2 Generar Datos de Entrenamiento
- [ ] Script para generar datos sintéticos realistas
- [ ] Incluir patrones de fallos comunes
- [ ] Balancear clases (fallos vs no-fallos)

#### 1.3 Entrenar Modelo
- [ ] Entrenar Random Forest con datos generados
- [ ] Validación cruzada
- [ ] Guardar modelo entrenado

#### 1.4 API Endpoints
```python
POST   /api/v1/predictions/predict/              # Predecir un activo
POST   /api/v1/predictions/predict-batch/        # Predecir múltiples
GET    /api/v1/predictions/                      # Listar predicciones
GET    /api/v1/predictions/{id}/                 # Detalle predicción
GET    /api/v1/predictions/high-risk/            # Activos de alto riesgo
```

#### 1.5 Scheduler Automático
- [ ] Celery task para predicciones diarias
- [ ] Configurar Celery Beat
- [ ] Logs de ejecución

### Fase 2: Integración Automática (1-2 días)

#### 2.1 Workflow Automático
```python
# Flujo completo
1. Predicción detecta riesgo HIGH/CRITICAL
2. Crear WorkOrder automáticamente
3. Asignar mejor operador disponible
4. Enviar notificación por todos los canales
5. Registrar en timeline del activo
```

#### 2.2 Signals Django
- [ ] Signal post-save en FailurePrediction
- [ ] Trigger automático de asignación
- [ ] Trigger de notificaciones

### Fase 3: Bot Omnicanal (3-4 días)

#### 3.1 Infraestructura Base
```python
apps/
  omnichannel_bot/
    __init__.py
    models.py              # MessageLog, ChannelConfig
    channels/
      __init__.py
      base.py             # BaseChannel interface
      whatsapp.py         # WhatsApp Business API
      telegram.py         # Telegram Bot API
      email.py            # SMTP Email
      sms.py              # Twilio SMS
      in_app.py           # In-app notifications
    message_router.py     # Route messages to channels
    templates.py          # Message templates
    views.py              # Webhooks
    urls.py
```

#### 3.2 Canales de Comunicación

**WhatsApp Business API**
- [ ] Integración con Meta Business API
- [ ] Templates de mensajes aprobados
- [ ] Webhook para respuestas

**Telegram Bot**
- [ ] Crear bot con BotFather
- [ ] Comandos: /status, /workorders, /help
- [ ] Notificaciones push

**Email**
- [ ] Configurar SMTP
- [ ] Templates HTML
- [ ] Adjuntar PDFs de órdenes

**SMS (Twilio)**
- [ ] Integración Twilio API
- [ ] Solo para alertas críticas
- [ ] Rate limiting

**In-App**
- [ ] WebSocket para real-time
- [ ] Toast notifications
- [ ] Badge counters

#### 3.3 Message Router
```python
class MessageRouter:
    def send_notification(self, user, message, priority='normal'):
        """
        Envía mensaje por todos los canales configurados del usuario
        """
        channels = user.notification_preferences.active_channels
        
        for channel in channels:
            if priority == 'critical' or channel.enabled:
                self.send_via_channel(channel, user, message)
```

#### 3.4 Templates de Mensajes
```python
TEMPLATES = {
    'failure_prediction_high': {
        'title': '⚠️ Alerta de Fallo Inminente',
        'body': '''
Activo: {asset_name}
Probabilidad: {probability}%
Riesgo: {risk_level}
Acción: {recommended_action}
        '''
    },
    'work_order_assigned': {
        'title': '📋 Nueva Orden de Trabajo',
        'body': '''
OT: {wo_number}
Activo: {asset_name}
Prioridad: {priority}
Fecha: {scheduled_date}
        '''
    }
}
```

### Fase 4: Frontend Dashboard (2-3 días)

#### 4.1 Página de Predicciones
- [ ] Lista de predicciones activas
- [ ] Filtros por riesgo, activo, fecha
- [ ] Gráficos de tendencias
- [ ] Mapa de calor de riesgos

#### 4.2 Dashboard de Operadores
- [ ] Vista de disponibilidad
- [ ] Carga de trabajo actual
- [ ] Skills y certificaciones
- [ ] Performance metrics

#### 4.3 Configuración de Bot
- [ ] Página de configuración de canales
- [ ] Test de conexión
- [ ] Preferencias de usuario

## 🔧 Dependencias Nuevas

```txt
# ML
scikit-learn==1.3.2
joblib==1.3.2
pandas==2.1.4
numpy==1.26.2

# Scheduler
celery==5.3.4
redis==5.0.1
django-celery-beat==2.5.0

# Bot Channels
python-telegram-bot==20.7
twilio==8.11.0
requests==2.31.0

# WebSocket (real-time)
channels==4.0.0
channels-redis==4.1.0
daphne==4.0.0
```

## 📊 Ejemplo de Flujo Completo

```
1. [SCHEDULER] Ejecuta predicción diaria a las 6:00 AM
   └─> Analiza todos los activos activos

2. [ML MODEL] Detecta: Camión Supersucker 001 - Riesgo HIGH (78%)
   └─> Crea FailurePrediction record

3. [SIGNAL] post_save en FailurePrediction
   └─> Trigger: create_preventive_work_order()

4. [WORK ORDER] Crea OT-2024-001
   └─> Título: "Mantenimiento Preventivo - Predicción de Falla"
   └─> Prioridad: HIGH

5. [ASSIGNMENT SERVICE] Busca mejor operador
   └─> Evalúa: Juan Pérez (Score: 87.5)
       - Skills: 90/100 (Certificado en Supersucker)
       - Disponibilidad: 85/100 (1 OT activa)
       - Performance: 92/100 (95% success rate)
       - Ubicación: 85/100 (Misma planta)
   └─> Asigna: Juan Pérez

6. [BOT OMNICANAL] Envía notificaciones
   ├─> WhatsApp: "⚠️ Nueva OT asignada: OT-2024-001..."
   ├─> Telegram: Mensaje con botones [Ver OT] [Aceptar]
   ├─> Email: PDF adjunto con detalles
   ├─> SMS: "Alerta: OT-2024-001 asignada"
   └─> In-App: Toast notification + Badge

7. [OPERADOR] Juan recibe notificación en todos sus canales
   └─> Responde por Telegram: /accept OT-2024-001
   └─> Bot actualiza estado: "in_progress"

8. [TIMELINE] Registra toda la actividad
   └─> Asset timeline muestra: Predicción → OT → Asignación → Aceptación
```

## 🎯 Métricas de Éxito

### ML Model
- Accuracy > 80%
- Precision > 75%
- Recall > 70%
- F1 Score > 75%

### Asignación de Operadores
- Tiempo promedio de asignación < 5 segundos
- Tasa de aceptación > 90%
- Balance de carga de trabajo (desviación estándar < 20%)

### Bot Omnicanal
- Tasa de entrega > 95%
- Tiempo de entrega < 30 segundos
- Tasa de respuesta de operadores > 80%

## 🚀 Orden de Implementación Recomendado

1. **Día 1-2**: Generar datos sintéticos + Entrenar modelo
2. **Día 3**: API endpoints + Tests
3. **Día 4**: Integración automática (Predicción → Asignación)
4. **Día 5-6**: Bot Telegram + Email (más simples)
5. **Día 7-8**: Bot WhatsApp (requiere aprobación)
6. **Día 9**: SMS + In-App
7. **Día 10-11**: Frontend Dashboard
8. **Día 12**: Testing integral + Documentación

## 📝 Notas Importantes

- **WhatsApp Business API** requiere cuenta de negocio verificada (puede tomar días)
- **Twilio SMS** requiere cuenta de pago
- **Telegram** es el más fácil de implementar (gratis, sin aprobaciones)
- Empezar con Telegram + Email para MVP rápido
- Agregar WhatsApp y SMS después

## ¿Empezamos?

Propongo empezar por:
1. Generar datos sintéticos realistas
2. Entrenar el modelo
3. Crear API endpoints
4. Implementar Telegram Bot (más rápido)
5. Integrar todo el flujo

¿Te parece bien este plan?
