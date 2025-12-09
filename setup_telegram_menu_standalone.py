"""
Script standalone para configurar el menú de comandos del bot de Telegram
No requiere conexión a base de datos
"""
import os
import requests
import sys

def setup_telegram_menu():
    """Configura el menú de comandos del bot de Telegram"""
    
    # Obtener token del bot desde variable de entorno
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    
    if not bot_token:
        print('❌ Error: TELEGRAM_BOT_TOKEN no está configurado en las variables de entorno')
        return False
    
    # Definir comandos del menú
    commands = [
        {"command": "start", "description": "🏠 Iniciar el bot"},
        {"command": "workorders", "description": "📋 Ver mis órdenes de trabajo"},
        {"command": "predictions", "description": "⚠️ Ver predicciones de alto riesgo"},
        {"command": "assets", "description": "🔧 Ver estado de activos"},
        {"command": "status", "description": "📊 Estado general del sistema"},
        {"command": "myinfo", "description": "👤 Ver mi información"},
        {"command": "help", "description": "❓ Ver ayuda y comandos"},
    ]
    
    print('\n📋 Configurando menú de comandos del bot...\n')
    
    try:
        # Enviar comandos a Telegram
        response = requests.post(
            f"https://api.telegram.org/bot{bot_token}/setMyCommands",
            json={"commands": commands},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('ok'):
                print('✅ Menú de comandos configurado exitosamente!\n')
                print('📱 Comandos disponibles:\n')
                for cmd in commands:
                    print(f"   /{cmd['command']} - {cmd['description']}")
                
                print('\n💡 Los usuarios ahora verán estos comandos al escribir "/" en el chat.\n')
                return True
            else:
                print(f"❌ Error: {result.get('description', 'Unknown error')}\n")
                return False
        else:
            print(f'❌ Error HTTP {response.status_code}: {response.text}\n')
            return False
    
    except Exception as e:
        print(f'❌ Error: {str(e)}\n')
        return False

if __name__ == '__main__':
    success = setup_telegram_menu()
    sys.exit(0 if success else 1)
