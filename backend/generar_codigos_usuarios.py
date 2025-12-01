"""
Script para generar códigos de vinculación para múltiples usuarios
"""
import os
import django
import sys

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from apps.authentication.models import User
from apps.omnichannel_bot.models import TelegramLinkCode
from django.utils import timezone
from datetime import timedelta
import random
import string


def generar_codigo():
    """Genera un código único de 6 caracteres"""
    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if not TelegramLinkCode.objects.filter(code=code).exists():
            return code


def generar_codigos_para_todos():
    """Genera códigos para todos los usuarios activos"""
    print("\n" + "="*60)
    print("GENERADOR DE CÓDIGOS DE VINCULACIÓN")
    print("="*60)
    
    usuarios = User.objects.filter(is_active=True).order_by('username')
    
    print(f"\n📋 Usuarios encontrados: {usuarios.count()}\n")
    
    codigos_generados = []
    
    for user in usuarios:
        # Generar código con expiración de 24 horas (más tiempo para distribuir)
        code = generar_codigo()
        
        link_code = TelegramLinkCode.objects.create(
            code=code,
            user=user,
            expires_at=timezone.now() + timedelta(hours=24)
        )
        
        codigos_generados.append({
            'username': user.username,
            'nombre': user.get_full_name() or user.username,
            'codigo': code
        })
        
        print(f"✅ {user.username:20s} → {code}")
    
    print("\n" + "="*60)
    print("CÓDIGOS GENERADOS")
    print("="*60)
    print("\nPuedes copiar y enviar estos códigos a cada usuario:\n")
    
    for item in codigos_generados:
        print(f"\n{item['nombre']} (@{item['username']}):")
        print(f"  Código: {item['codigo']}")
        print(f"  Instrucción: /vincular {item['codigo']}")
    
    print("\n" + "="*60)
    print(f"✅ {len(codigos_generados)} códigos generados")
    print("⏰ Expiran en 24 horas")
    print("="*60)
    
    # Guardar en archivo
    with open('codigos_telegram.txt', 'w', encoding='utf-8') as f:
        f.write("CÓDIGOS DE VINCULACIÓN TELEGRAM\n")
        f.write("="*60 + "\n\n")
        
        for item in codigos_generados:
            f.write(f"{item['nombre']} (@{item['username']})\n")
            f.write(f"Código: {item['codigo']}\n")
            f.write(f"Instrucción: /vincular {item['codigo']}\n")
            f.write("-"*60 + "\n\n")
        
        f.write(f"\nTotal: {len(codigos_generados)} códigos\n")
        f.write("Expiran en: 24 horas\n")
    
    print(f"\n💾 Códigos guardados en: codigos_telegram.txt")


def generar_codigo_para_usuario(username):
    """Genera un código para un usuario específico"""
    try:
        user = User.objects.get(username=username)
        
        code = generar_codigo()
        
        link_code = TelegramLinkCode.objects.create(
            code=code,
            user=user,
            expires_at=timezone.now() + timedelta(hours=24)
        )
        
        print("\n" + "="*60)
        print(f"✅ Código generado para {user.get_full_name() or user.username}")
        print("="*60)
        print(f"\nUsuario: {user.username}")
        print(f"Código: {code}")
        print(f"Expira en: 24 horas")
        print(f"\nInstrucción para el usuario:")
        print(f"  /vincular {code}")
        print("="*60)
        
    except User.DoesNotExist:
        print(f"\n❌ Usuario '{username}' no encontrado")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Generar código para usuario específico
        username = sys.argv[1]
        generar_codigo_para_usuario(username)
    else:
        # Generar códigos para todos
        generar_codigos_para_todos()
