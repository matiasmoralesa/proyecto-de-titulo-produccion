"""
URLs para el bot omnicanal
"""
from django.urls import path
from . import views

app_name = 'omnichannel_bot'

urlpatterns = [
    path('webhook/telegram/', views.telegram_webhook, name='telegram_webhook'),
    path('status/', views.bot_status, name='bot_status'),
    path('link-user/', views.link_user_telegram, name='link_user_telegram'),
    path('get-chat-id/', views.get_my_chat_id, name='get_my_chat_id'),
    path('generate-code/', views.generate_link_code, name='generate_link_code'),
]
