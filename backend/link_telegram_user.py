"""
Script para vincular usuarios con sus chat_ids de Telegram
"""
import os
import django
import sys

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from apps.authentication.models import User
from apps.omnichannel_bot.models import UserChannelPreference


def list_users():
    """Lista todos los usuarios del sistema"""
    print("\n📋 Usuarios del sistema:")
    print("=" * 60)
    users = User.objects.all().order_by('id')
    for user in users:
        print(f"ID: {user.id:3d} | Username: {user.username:20s} | Nombre: {user.get_full_name()}")
    print("=" * 60)


def list_linked_users():
    """Lista usuarios ya vinculados con Telegram"""
    print("\n🔗 Usuarios vinculados con Telegram:")
    print("=" * 60)
    preferences = UserChannelPreference.objects.filter(channel_type='TELEGRAM')
    
    if not preferences.exists():
        print("No hay usuarios vinculados aún")
    else:
        for pref in preferences:
            status = "✅ Activo" if pref.is_enabled else "❌ Inactivo"
            print(f"User: {pref.user.username:20s} | Chat ID: {pref.channel_user_id:15s} | {status}")
    print("=" * 60)


def get_recent_chat_ids():
    """Obtiene los chat_ids de mensajes recientes"""
    from apps.omnichannel_bot.models import ChannelConfig
    import requests
    
    try:
        config = ChannelConfig.objects.get(channel_type='TELEGRAM', is_enabled=True)
        bot_token = config.config.get('bot_token', '')
        
        if not bot_token:
            print("❌ Bot token no configurado")
            return []
        
        response = requests.get(
            f"https://api.telegram.org/bot{bot_token}/getUpdates",
            params={'limit': 20},
            timeout=10
        )
        
        if response.status_code != 200:
            print("❌ Error al obtener actualizaciones del bot")
            return []
        
        updates = response.json().get('result', [])
        
        chat_ids = {}
        for update in updates:
            if 'message' in update:
                chat = update['message']['chat']
                from_user = update['message']['from']
                chat_id = str(chat['id'])
                
                if chat_id not in chat_ids:
                    chat_ids[chat_id] = {
                        'chat_id': chat_id,
                        'first_name': from_user.get('first_name', ''),
                        'last_name': from_user.get('last_name', ''),
                        'username': from_user.get('username', ''),
                        'last_message': update['message'].get('text', '')[:30]
                    }
        
        return list(chat_ids.values())
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return []


def show_recent_chat_ids():
    """Muestra los chat_ids recientes"""
    print("\n💬 Chat IDs de mensajes recientes:")
    print("=" * 80)
    print("(Envía un mensaje al bot en Telegram si no ves tu chat_id)")
    print("=" * 80)
    
    chat_ids = get_recent_chat_ids()
    
    if not chat_ids:
        print("No hay mensajes recientes. Envía /start al bot en Telegram.")
    else:
        for chat in chat_ids:
            username = f"@{chat['username']}" if chat['username'] else "Sin username"
            name = f"{chat['first_name']} {chat['last_name']}".strip()
            print(f"Chat ID: {chat['chat_id']:15s} | {name:25s} | {username:20s}")
            print(f"  Último mensaje: {chat['last_message']}")
    
    print("=" * 80)


def link_user(user_id, chat_id):
    """Vincula un usuario con su chat_id"""
    try:
        user = User.objects.get(id=user_id)
        
        preference, created = UserChannelPreference.objects.update_or_create(
            user=user,
            channel_type='TELEGRAM',
            defaults={
                'channel_user_id': str(chat_id),
                'is_enabled': True,
                'preferences': {}
            }
        )
        
        action = "vinculado" if created else "actualizado"
        print(f"\n✅ Usuario {user.username} {action} con chat_id {chat_id}")
        
        return True
    
    except User.DoesNotExist:
        print(f"\n❌ Usuario con ID {user_id} no encontrado")
        return False
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False


def interactive_mode():
    """Modo interactivo para vincular usuarios"""
    print("\n" + "=" * 60)
    print("🤖 VINCULACIÓN DE USUARIOS CON TELEGRAM")
    print("=" * 60)
    
    while True:
        print("\n¿Qué deseas hacer?")
        print("1. Ver usuarios del sistema")
        print("2. Ver usuarios ya vinculados")
        print("3. Ver chat IDs recientes")
        print("4. Vincular usuario")
        print("5. Salir")
        
        choice = input("\nOpción: ").strip()
        
        if choice == '1':
            list_users()
        
        elif choice == '2':
            list_linked_users()
        
        elif choice == '3':
            show_recent_chat_ids()
        
        elif choice == '4':
            list_users()
            user_id = input("\nIngresa el ID del usuario: ").strip()
            
            show_recent_chat_ids()
            chat_id = input("\nIngresa el Chat ID de Telegram: ").strip()
            
            if user_id and chat_id:
                link_user(user_id, chat_id)
            else:
                print("❌ Debes ingresar ambos valores")
        
        elif choice == '5':
            print("\n👋 ¡Hasta luego!")
            break
        
        else:
            print("❌ Opción no válida")


def quick_link():
    """Vinculación rápida desde argumentos de línea de comandos"""
    if len(sys.argv) >= 3:
        user_id = sys.argv[1]
        chat_id = sys.argv[2]
        
        print(f"\n🔗 Vinculando usuario {user_id} con chat_id {chat_id}...")
        link_user(user_id, chat_id)
    else:
        print("\n📝 Uso: python link_telegram_user.py <user_id> <chat_id>")
        print("   O ejecuta sin argumentos para modo interactivo")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        quick_link()
    else:
        interactive_mode()
