"""
Script para probar los botones del bot de Telegram
"""
import os
import django
import sys

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from apps.omnichannel_bot.channels.telegram import TelegramChannel
from apps.omnichannel_bot.models import ChannelConfig
from apps.omnichannel_bot.bot_commands import BotCommandHandler


def test_telegram_buttons():
    """
    Prueba los botones del bot de Telegram
    """
    print("🔍 Verificando configuración del bot de Telegram...")
    
    try:
        # Obtener configuración
        config = ChannelConfig.objects.get(channel_type='TELEGRAM', is_enabled=True)
        print(f"✅ Configuración encontrada: {config.channel_name}")
        
        # Crear instancia del canal
        telegram = TelegramChannel(config.config)
        
        # Verificar conexión
        if telegram.validate_config():
            print("✅ Bot de Telegram conectado correctamente")
        else:
            print("❌ Error al conectar con el bot de Telegram")
            return
        
        # Probar comandos con botones
        print("\n📋 Probando comandos con botones...")
        handler = BotCommandHandler()
        
        # Test /start
        print("\n1. Comando /start:")
        response = handler.cmd_start()
        print(f"   Texto: {response['text'][:50]}...")
        print(f"   Botones: {len(response.get('buttons', []))} botones")
        for btn_row in response.get('buttons', []):
            for btn in btn_row:
                print(f"      - {btn['text']} → {btn['callback_data']}")
        
        # Test /status
        print("\n2. Comando /status:")
        response = handler.cmd_status()
        print(f"   Texto: {response['text'][:50]}...")
        print(f"   Botones: {len(response.get('buttons', []))} botones")
        for btn_row in response.get('buttons', []):
            for btn in btn_row:
                print(f"      - {btn['text']} → {btn['callback_data']}")
        
        # Test /workorders
        print("\n3. Comando /workorders:")
        response = handler.cmd_workorders()
        print(f"   Texto: {response['text'][:50]}...")
        if 'buttons' in response:
            print(f"   Botones: {len(response.get('buttons', []))} botones")
            for btn_row in response.get('buttons', []):
                for btn in btn_row:
                    print(f"      - {btn['text']} → {btn['callback_data']}")
        else:
            print("   Sin botones (sin órdenes de trabajo)")
        
        # Test /predictions
        print("\n4. Comando /predictions:")
        response = handler.cmd_predictions()
        print(f"   Texto: {response['text'][:50]}...")
        
        # Test /help
        print("\n5. Comando /help:")
        response = handler.cmd_help()
        print(f"   Texto: {response['text'][:50]}...")
        
        print("\n✅ Todos los comandos funcionan correctamente")
        print("\n📝 Estructura de botones:")
        print("   - Los botones usan 'inline_keyboard' de Telegram")
        print("   - Cada botón tiene 'text' y 'callback_data'")
        print("   - Los callbacks se procesan en handle_callback()")
        
        print("\n🔗 Para probar en producción:")
        print("   1. Envía /start al bot en Telegram")
        print("   2. Presiona los botones interactivos")
        print("   3. Verifica que naveguen correctamente")
        
        # Verificar webhook
        print("\n🌐 Verificando webhook...")
        bot_token = config.config.get('bot_token', '')
        if bot_token:
            import requests
            response = requests.get(f"https://api.telegram.org/bot{bot_token}/getWebhookInfo")
            if response.status_code == 200:
                webhook_info = response.json()['result']
                webhook_url = webhook_info.get('url', 'No configurado')
                print(f"   URL del webhook: {webhook_url}")
                print(f"   Actualizaciones pendientes: {webhook_info.get('pending_update_count', 0)}")
                
                if webhook_url:
                    print("   ✅ Webhook configurado")
                else:
                    print("   ⚠️ Webhook no configurado")
                    print("   Configúralo con: /api/data-loader/setup-telegram/")
            else:
                print("   ❌ Error al obtener info del webhook")
        
    except ChannelConfig.DoesNotExist:
        print("❌ No se encontró configuración de Telegram")
        print("   Configura el bot primero con /api/data-loader/setup-telegram/")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    test_telegram_buttons()
