"""
Script para probar el webhook de Telegram directamente
"""
import requests
import json

# Reemplaza con tu URL de Railway
RAILWAY_URL = "https://tu-app.up.railway.app"

def test_webhook():
    """Prueba el webhook enviando un mensaje de prueba"""
    
    print("🧪 Probando webhook de Telegram...\n")
    
    # Simular un mensaje de Telegram
    test_message = {
        "update_id": 123456789,
        "message": {
            "message_id": 1,
            "from": {
                "id": 123456789,
                "is_bot": False,
                "first_name": "Test",
                "username": "testuser"
            },
            "chat": {
                "id": 123456789,
                "first_name": "Test",
                "username": "testuser",
                "type": "private"
            },
            "date": 1234567890,
            "text": "/help"
        }
    }
    
    print("📤 Enviando mensaje de prueba: /help")
    print(f"URL: {RAILWAY_URL}/api/omnichannel/webhook/telegram/\n")
    
    try:
        response = requests.post(
            f"{RAILWAY_URL}/api/omnichannel/webhook/telegram/",
            json=test_message,
            timeout=10
        )
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📝 Response: {response.text}\n")
        
        if response.status_code == 200:
            print("✅ Webhook respondió correctamente")
            result = response.json()
            if result.get('ok'):
                print("✅ Mensaje procesado exitosamente")
            else:
                print("❌ Error en el procesamiento")
                print(f"Error: {result}")
        else:
            print(f"❌ Error HTTP {response.status_code}")
            print(f"Respuesta: {response.text}")
    
    except requests.exceptions.Timeout:
        print("❌ Timeout - El servidor no respondió a tiempo")
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión - No se pudo conectar al servidor")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_bot_status():
    """Verifica el estado del bot"""
    print("\n" + "="*60)
    print("📊 Verificando estado del bot...\n")
    
    try:
        response = requests.get(
            f"{RAILWAY_URL}/api/omnichannel/status/",
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ Estado del bot:")
            print(f"   Status: {data.get('status')}")
            print(f"   Channel: {data.get('channel')}")
            print(f"   Mensajes enviados: {data.get('messages_sent')}")
            print(f"   Mensajes fallidos: {data.get('messages_failed')}")
        else:
            print(f"❌ Error: {response.text}")
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_get_chat_ids():
    """Obtiene los chat IDs recientes"""
    print("\n" + "="*60)
    print("💬 Obteniendo chat IDs recientes...\n")
    
    try:
        response = requests.get(
            f"{RAILWAY_URL}/api/omnichannel/get-chat-id/",
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                chat_ids = data.get('chat_ids', [])
                print(f"\n✅ {len(chat_ids)} chat IDs encontrados:")
                for chat in chat_ids:
                    print(f"\n   Chat ID: {chat.get('chat_id')}")
                    print(f"   Nombre: {chat.get('first_name')} {chat.get('last_name')}")
                    print(f"   Username: @{chat.get('username')}")
                    print(f"   Último mensaje: {chat.get('last_message')}")
            else:
                print(f"❌ Error: {data.get('error')}")
        else:
            print(f"❌ Error: {response.text}")
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == '__main__':
    print("="*60)
    print("🤖 TEST DE TELEGRAM BOT")
    print("="*60)
    print("\n⚠️  IMPORTANTE: Actualiza RAILWAY_URL en el script")
    print(f"    URL actual: {RAILWAY_URL}\n")
    
    input("Presiona Enter para continuar...")
    
    test_bot_status()
    test_get_chat_ids()
    test_webhook()
    
    print("\n" + "="*60)
    print("✅ Tests completados")
    print("="*60)
