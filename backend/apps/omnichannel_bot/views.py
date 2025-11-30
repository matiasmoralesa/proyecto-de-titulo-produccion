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
    
    # Buscar usuario del sistema asociado a este chat_id
    try:
        preference = UserChannelPreference.objects.get(
            channel_type='TELEGRAM',
            channel_user_id=chat_id
        )
        user = preference.user
    except UserChannelPreference.DoesNotExist:
        user = None
        logger.warning(f"No user found for chat_id {chat_id}")
    
    # Procesar comando
    if text.startswith('/'):
        handler = BotCommandHandler()
        response = handler.handle_command(text, user)
        
        # Enviar respuesta
        telegram.send_message(
            chat_id=chat_id,
            title='',
            message=response['text'],
            reply_markup={'inline_keyboard': response.get('buttons', [])} if response.get('buttons') else None
        )
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


def handle_callback(callback_query: dict, telegram: TelegramChannel):
    """
    Procesa un callback de botón presionado
    """
    callback_id = callback_query['id']
    chat_id = str(callback_query['message']['chat']['id'])
    message_id = callback_query['message']['message_id']
    callback_data = callback_query['data']
    
    logger.info(f"Callback from {chat_id}: {callback_data}")
    
    # Buscar usuario
    try:
        preference = UserChannelPreference.objects.get(
            channel_type='TELEGRAM',
            channel_user_id=chat_id
        )
        user = preference.user
    except UserChannelPreference.DoesNotExist:
        user = None
    
    # Procesar callback
    handler = BotCommandHandler()
    response = handler.handle_callback(callback_data, user)
    
    # Responder al callback (para quitar el "loading" del botón)
    import requests
    bot_token = telegram.bot_token
    requests.post(
        f"https://api.telegram.org/bot{bot_token}/answerCallbackQuery",
        json={'callback_query_id': callback_id}
    )
    
    # Editar el mensaje con la nueva respuesta
    requests.post(
        f"https://api.telegram.org/bot{bot_token}/editMessageText",
        json={
            'chat_id': chat_id,
            'message_id': message_id,
            'text': response['text'],
            'parse_mode': 'Markdown',
            'reply_markup': {'inline_keyboard': response.get('buttons', [])} if response.get('buttons') else None
        }
    )


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
