"""
Views para el bot omnicanal
"""
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import logging
from .models import ChannelConfig, UserChannelPreference
from .channels.telegram import TelegramChannel
from .bot_commands import BotCommandHandler

logger = logging.getLogger(__name__)


@csrf_exempt
@require_http_methods(["POST", "GET"])
def telegram_webhook(request):
    """
    Webhook para recibir actualizaciones de Telegram
    """
    if request.method == 'GET':
        return HttpResponse("Telegram Webhook is active", status=200)
    
    try:
        # Obtener configuración del bot
        config = ChannelConfig.objects.get(channel_type='TELEGRAM', is_enabled=True)
        telegram = TelegramChannel(config.config)
        
        # Parsear el update de Telegram
        update = json.loads(request.body.decode('utf-8'))
        logger.info(f"Telegram update received: {update}")
        
        # Extraer información del mensaje
        message = update.get('message')
        callback_query = update.get('callback_query')
        
        if message:
            handle_message(message, telegram)
        elif callback_query:
            handle_callback(callback_query, telegram)
        
        return JsonResponse({'ok': True})
    
    except ChannelConfig.DoesNotExist:
        logger.error("Telegram channel not configured")
        return JsonResponse({'error': 'Channel not configured'}, status=500)
    except Exception as e:
        logger.error(f"Error processing telegram webhook: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)


def handle_message(message: dict, telegram: TelegramChannel):
    """
    Procesa un mensaje recibido del usuario
    """
    chat_id = str(message['chat']['id'])
    text = message.get('text', '')
    from_user = message.get('from', {})
    
    logger.info(f"Message from {chat_id}: {text}")
    
    try:
        # Buscar usuario del sistema asociado a este chat_id
        try:
            preference = UserChannelPreference.objects.get(
                channel_type='TELEGRAM',
                channel_user_id=chat_id
            )
            user = preference.user
            logger.info(f"User found: {user.username}")
        except UserChannelPreference.DoesNotExist:
            user = None
            logger.warning(f"No user found for chat_id {chat_id}")
        
        # Procesar comando
        if text.startswith('/'):
            handler = BotCommandHandler()
            response = handler.handle_command(text, user)
            
            logger.info(f"Command response: {response['text'][:50]}...")
            
            # Enviar respuesta
            result = telegram.send_message(
                chat_id=chat_id,
                title='',
                message=response['text'],
                reply_markup={'inline_keyboard': response.get('buttons', [])} if response.get('buttons') else None
            )
            
            if result.get('success'):
                logger.info(f"Message sent successfully to {chat_id}")
            else:
                logger.error(f"Failed to send message: {result.get('error')}")
        else:
            # Mensaje no es comando
            if not user:
                telegram.send_message(
                    chat_id=chat_id,
                    title='',
                    message=(
                        '👋 ¡Hola!\n\n'
                        'Para usar este bot, necesitas que un administrador configure tu cuenta.\n\n'
                        f'Tu Chat ID es: `{chat_id}`\n\n'
                        'Proporciona este ID al administrador para que te configure.'
                    )
                )
            else:
                telegram.send_message(
                    chat_id=chat_id,
                    title='',
                    message=(
                        'Usa /help para ver los comandos disponibles.\n\n'
                        'O usa los botones del menú para navegar.'
                    )
                )
    
    except Exception as e:
        logger.error(f"Error in handle_message: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        # Intentar enviar mensaje de error al usuario
        try:
            telegram.send_message(
                chat_id=chat_id,
                title='',
                message='❌ Error procesando tu mensaje. Por favor intenta de nuevo.'
            )
        except:
            pass


def handle_callback(callback_query: dict, telegram: TelegramChannel):
    """
    Procesa un callback de botón presionado
    """
    import requests
    
    callback_id = callback_query['id']
    chat_id = str(callback_query['message']['chat']['id'])
    message_id = callback_query['message']['message_id']
    callback_data = callback_query['data']
    bot_token = telegram.bot_token
    
    logger.info(f"Callback from {chat_id}: {callback_data}")
    
    try:
        # Buscar usuario
        try:
            preference = UserChannelPreference.objects.get(
                channel_type='TELEGRAM',
                channel_user_id=chat_id
            )
            user = preference.user
            logger.info(f"User found: {user.username}")
        except UserChannelPreference.DoesNotExist:
            user = None
            logger.warning(f"No user found for chat_id {chat_id}")
        
        # Procesar callback
        handler = BotCommandHandler()
        response = handler.handle_callback(callback_data, user)
        
        # Responder al callback (para quitar el "loading" del botón)
        answer_response = requests.post(
            f"https://api.telegram.org/bot{bot_token}/answerCallbackQuery",
            json={'callback_query_id': callback_id},
            timeout=5
        )
        logger.info(f"Answer callback response: {answer_response.status_code}")
        
        # Editar el mensaje con la nueva respuesta
        edit_response = requests.post(
            f"https://api.telegram.org/bot{bot_token}/editMessageText",
            json={
                'chat_id': chat_id,
                'message_id': message_id,
                'text': response['text'],
                'parse_mode': 'Markdown',
                'reply_markup': {'inline_keyboard': response.get('buttons', [])} if response.get('buttons') else None
            },
            timeout=10
        )
        
        if edit_response.status_code == 200:
            logger.info(f"Message edited successfully")
        else:
            logger.error(f"Error editing message: {edit_response.text}")
            # Si falla la edición, enviar nuevo mensaje
            telegram.send_message(
                chat_id=chat_id,
                title='',
                message=response['text'],
                reply_markup={'inline_keyboard': response.get('buttons', [])} if response.get('buttons') else None
            )
    
    except Exception as e:
        logger.error(f"Error in handle_callback: {str(e)}")
        # Responder al callback aunque haya error
        try:
            requests.post(
                f"https://api.telegram.org/bot{bot_token}/answerCallbackQuery",
                json={
                    'callback_query_id': callback_id,
                    'text': '❌ Error procesando acción',
                    'show_alert': True
                },
                timeout=5
            )
        except:
            pass


@require_http_methods(["GET"])
def bot_status(request):
    """
    Endpoint para verificar el estado del bot
    """
    try:
        telegram_config = ChannelConfig.objects.get(channel_type='TELEGRAM')
        
        return JsonResponse({
            'status': 'active' if telegram_config.is_enabled else 'inactive',
            'channel': 'TELEGRAM',
            'messages_sent': telegram_config.messages_sent,
            'messages_failed': telegram_config.messages_failed,
            'last_used': telegram_config.last_used.isoformat() if telegram_config.last_used else None
        })
    except ChannelConfig.DoesNotExist:
        return JsonResponse({
            'status': 'not_configured',
            'error': 'Telegram channel not configured'
        }, status=404)


@csrf_exempt
@require_http_methods(["POST", "GET"])
def link_user_telegram(request):
    """
    Endpoint para vincular un usuario con su chat_id de Telegram
    """
    if request.method == 'GET':
        # Listar usuarios vinculados
        preferences = UserChannelPreference.objects.filter(channel_type='TELEGRAM')
        users_list = []
        for pref in preferences:
            users_list.append({
                'user_id': pref.user.id,
                'username': pref.user.username,
                'full_name': pref.user.get_full_name(),
                'chat_id': pref.channel_user_id,
                'is_enabled': pref.is_enabled
            })
        
        return JsonResponse({
            'success': True,
            'users': users_list,
            'total': len(users_list)
        })
    
    # POST - Vincular usuario
    try:
        data = json.loads(request.body.decode('utf-8'))
        user_id = data.get('user_id')
        chat_id = str(data.get('chat_id'))
        
        if not user_id or not chat_id:
            return JsonResponse({
                'success': False,
                'error': 'user_id y chat_id son requeridos'
            }, status=400)
        
        from apps.authentication.models import User
        
        # Buscar usuario
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': f'Usuario con id {user_id} no encontrado'
            }, status=404)
        
        # Crear o actualizar preferencia
        preference, created = UserChannelPreference.objects.update_or_create(
            user=user,
            channel_type='TELEGRAM',
            defaults={
                'channel_user_id': chat_id,
                'is_enabled': True,
                'preferences': {}
            }
        )
        
        action = 'creado' if created else 'actualizado'
        
        return JsonResponse({
            'success': True,
            'message': f'Usuario {user.username} {action} con chat_id {chat_id}',
            'user': {
                'id': user.id,
                'username': user.username,
                'full_name': user.get_full_name(),
                'chat_id': chat_id
            }
        })
    
    except Exception as e:
        logger.error(f"Error linking user: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def get_my_chat_id(request):
    """
    Endpoint para que un usuario obtenga su chat_id
    Instrucciones: Envía cualquier mensaje al bot y luego visita esta URL
    """
    try:
        # Obtener configuración del bot
        config = ChannelConfig.objects.get(channel_type='TELEGRAM', is_enabled=True)
        bot_token = config.config.get('bot_token', '')
        
        if not bot_token:
            return JsonResponse({
                'success': False,
                'error': 'Bot token no configurado'
            }, status=500)
        
        # Obtener actualizaciones recientes
        import requests
        response = requests.get(
            f"https://api.telegram.org/bot{bot_token}/getUpdates",
            params={'limit': 10},
            timeout=10
        )
        
        if response.status_code != 200:
            return JsonResponse({
                'success': False,
                'error': 'Error al obtener actualizaciones del bot'
            }, status=500)
        
        updates = response.json().get('result', [])
        
        # Extraer chat_ids únicos
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
                        'last_message': update['message'].get('text', '')
                    }
        
        return JsonResponse({
            'success': True,
            'message': 'Chat IDs de usuarios que han enviado mensajes recientemente',
            'chat_ids': list(chat_ids.values()),
            'instructions': (
                '1. Envía un mensaje al bot en Telegram\n'
                '2. Recarga esta página\n'
                '3. Busca tu chat_id en la lista\n'
                '4. Usa /api/omnichannel/link-user/ para vincular tu usuario'
            )
        })
    
    except ChannelConfig.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Bot de Telegram no configurado'
        }, status=404)
    except Exception as e:
        logger.error(f"Error getting chat IDs: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
