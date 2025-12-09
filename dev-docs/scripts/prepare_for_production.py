#!/usr/bin/env python3
"""
Script para preparar el proyecto para deployment en producción.
Verifica configuraciones, optimiza archivos y genera documentación.
"""

import os
import sys
from pathlib import Path

def print_header(text):
    """Imprime un encabezado formateado."""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")

def print_success(text):
    """Imprime mensaje de éxito."""
    print(f"✅ {text}")

def print_warning(text):
    """Imprime mensaje de advertencia."""
    print(f"⚠️  {text}")

def print_error(text):
    """Imprime mensaje de error."""
    print(f"❌ {text}")

def check_file_exists(filepath):
    """Verifica si un archivo existe."""
    return Path(filepath).exists()

def check_security_settings():
    """Verifica configuraciones de seguridad."""
    print_header("Verificando Configuraciones de Seguridad")
    
    issues = []
    
    # Verificar .gitignore
    if check_file_exists(".gitignore"):
        with open(".gitignore", "r") as f:
            gitignore_content = f.read()
            
        required_entries = [".env", "db.sqlite3", "*.log", "__pycache__"]
        for entry in required_entries:
            if entry in gitignore_content:
                print_success(f"'{entry}' está en .gitignore")
            else:
                print_warning(f"'{entry}' NO está en .gitignore")
                issues.append(f"Agregar '{entry}' a .gitignore")
    else:
        print_error(".gitignore no encontrado")
        issues.append("Crear archivo .gitignore")
    
    # Verificar que archivos sensibles no estén trackeados
    sensitive_files = [".env", "db.sqlite3", "*.log"]
    for pattern in sensitive_files:
        if check_file_exists(pattern.replace("*", "test")):
            print_warning(f"Archivos sensibles encontrados: {pattern}")
            issues.append(f"Asegurar que {pattern} no se suba a Git")
    
    return issues

def check_dependencies():
    """Verifica dependencias del proyecto."""
    print_header("Verificando Dependencias")
    
    issues = []
    
    # Backend
    if check_file_exists("backend/requirements.txt"):
        print_success("requirements.txt encontrado")
    else:
        print_error("requirements.txt no encontrado")
        issues.append("Crear backend/requirements.txt")
    
    # Frontend
    if check_file_exists("frontend/package.json"):
        print_success("package.json encontrado")
    else:
        print_error("package.json no encontrado")
        issues.append("Crear frontend/package.json")
    
    return issues

def check_documentation():
    """Verifica documentación del proyecto."""
    print_header("Verificando Documentación")
    
    issues = []
    
    docs = {
        "README.md": "Documentación principal",
        "DEPLOYMENT_GUIDE.md": "Guía de deployment",
        "docs/SETUP_LOCAL.md": "Guía de setup local",
    }
    
    for doc, description in docs.items():
        if check_file_exists(doc):
            print_success(f"{description} encontrado")
        else:
            print_warning(f"{description} no encontrado")
            issues.append(f"Crear {doc}")
    
    return issues

def generate_production_requirements():
    """Genera requirements.txt optimizado para producción."""
    print_header("Generando requirements-production.txt")
    
    if not check_file_exists("backend/requirements.txt"):
        print_error("No se puede generar requirements-production.txt sin requirements.txt")
        return
    
    with open("backend/requirements.txt", "r") as f:
        requirements = f.readlines()
    
    # Agregar dependencias de producción
    production_deps = [
        "\n# Production dependencies\n",
        "gunicorn==21.2.0\n",
        "psycopg2-binary==2.9.9\n",
        "whitenoise==6.6.0\n",
        "sentry-sdk==1.39.1\n",
    ]
    
    with open("backend/requirements-production.txt", "w") as f:
        f.writelines(requirements)
        f.writelines(production_deps)
    
    print_success("requirements-production.txt generado")

def create_production_env_template():
    """Crea template de .env para producción."""
    print_header("Creando .env.production.template")
    
    env_template = """# Django Settings
DEBUG=False
SECRET_KEY=change-this-to-a-random-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/cmms_prod

# Redis
REDIS_URL=redis://localhost:6379/0

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/1

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Telegram
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_ENABLED=True

# AWS S3 (Optional)
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=cmms-media
AWS_S3_REGION_NAME=us-east-1

# Sentry (Optional)
SENTRY_DSN=your-sentry-dsn
"""
    
    with open(".env.production.template", "w") as f:
        f.write(env_template)
    
    print_success(".env.production.template creado")

def create_deployment_checklist():
    """Crea checklist de deployment."""
    print_header("Creando DEPLOYMENT_CHECKLIST.md")
    
    checklist = """# Deployment Checklist

## Pre-Deployment

- [ ] Código revisado y testeado
- [ ] Tests pasando (backend y frontend)
- [ ] Documentación actualizada
- [ ] Variables de entorno configuradas
- [ ] Archivos sensibles en .gitignore
- [ ] Backup de datos actual

## Servidor

- [ ] Servidor configurado (VPS/Cloud)
- [ ] PostgreSQL instalado
- [ ] Redis instalado
- [ ] Nginx instalado
- [ ] Certificado SSL configurado
- [ ] Firewall configurado

## Aplicación

- [ ] Código clonado en servidor
- [ ] Dependencias instaladas
- [ ] Migraciones ejecutadas
- [ ] Archivos estáticos recolectados
- [ ] Gunicorn configurado
- [ ] Celery Worker corriendo
- [ ] Celery Beat corriendo

## Frontend

- [ ] Build de producción generado
- [ ] Archivos deployados
- [ ] Variables de entorno configuradas
- [ ] DNS configurado

## Post-Deployment

- [ ] Health checks pasando
- [ ] Logs monitoreados
- [ ] Backups automáticos configurados
- [ ] Monitoreo configurado
- [ ] Documentación de deployment actualizada

## Testing en Producción

- [ ] Login funciona
- [ ] APIs responden correctamente
- [ ] Notificaciones funcionan
- [ ] Celery tasks ejecutándose
- [ ] Bot de Telegram funciona
- [ ] Predicciones ML funcionan

---

**Fecha de Deployment:** _______________
**Deployado por:** _______________
**Versión:** _______________
"""
    
    # Solo crear si no existe para no sobrescribir
    if not check_file_exists("docs/DEPLOYMENT_CHECKLIST.md"):
        os.makedirs("docs", exist_ok=True)
        with open("docs/DEPLOYMENT_CHECKLIST.md", "w") as f:
            f.write(checklist)
        print_success("DEPLOYMENT_CHECKLIST.md creado")
    else:
        print_warning("DEPLOYMENT_CHECKLIST.md ya existe, no se sobrescribió")

def main():
    """Función principal."""
    print("\n" + "=" * 60)
    print("  PREPARACIÓN PARA PRODUCCIÓN - Sistema CMMS")
    print("=" * 60)
    
    all_issues = []
    
    # Ejecutar verificaciones
    all_issues.extend(check_security_settings())
    all_issues.extend(check_dependencies())
    all_issues.extend(check_documentation())
    
    # Generar archivos
    generate_production_requirements()
    create_production_env_template()
    create_deployment_checklist()
    
    # Resumen
    print_header("Resumen")
    
    if all_issues:
        print_warning(f"Se encontraron {len(all_issues)} problemas:")
        for i, issue in enumerate(all_issues, 1):
            print(f"  {i}. {issue}")
    else:
        print_success("¡Todo listo para producción!")
    
    print("\n" + "=" * 60)
    print("  Próximos pasos:")
    print("=" * 60)
    print("1. Revisar y resolver los problemas listados arriba")
    print("2. Configurar .env.production con valores reales")
    print("3. Ejecutar: setup_git_repos.bat")
    print("4. Seguir DEPLOYMENT_GUIDE.md para deployment")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()
