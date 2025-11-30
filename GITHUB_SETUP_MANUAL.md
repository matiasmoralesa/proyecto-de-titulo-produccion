# Guía Manual para Crear Repositorios en GitHub

Si prefieres crear los repositorios manualmente o si el script automático falla, sigue estos pasos:

## Opción 1: Usando la Interfaz Web de GitHub

### Paso 1: Crear Repositorio "proyecto-de-titulo-local"

1. Ve a: https://github.com/new
2. Configura:
   - **Repository name:** `proyecto-de-titulo-local`
   - **Description:** Sistema CMMS - Gestión de Mantenimiento con ML y Bot Telegram
   - **Visibility:** Private (recomendado)
   - **NO** marques "Initialize this repository with a README"
3. Haz clic en "Create repository"

### Paso 2: Crear Repositorio "proyecto-de-titulo-produccion"

1. Ve a: https://github.com/new
2. Configura:
   - **Repository name:** `proyecto-de-titulo-produccion`
   - **Description:** Sistema CMMS - Versión de Producción
   - **Visibility:** Private (recomendado)
   - **NO** marques "Initialize this repository with a README"
3. Haz clic en "Create repository"

### Paso 3: Conectar tu Proyecto Local

Abre PowerShell o CMD en la carpeta del proyecto y ejecuta:

```bash
# Inicializar Git
git init
git branch -M main

# Agregar todos los archivos
git add .

# Crear commit inicial
git commit -m "Initial commit: Sistema CMMS completo"

# Conectar con el repositorio remoto (reemplaza TU_USUARIO)
git remote add origin https://github.com/TU_USUARIO/proyecto-de-titulo-local.git

# Subir el código
git push -u origin main
```

**IMPORTANTE:** Reemplaza `TU_USUARIO` con tu nombre de usuario de GitHub.

---

## Opción 2: Usando GitHub CLI (Recomendado)

### Requisitos Previos

1. Instalar GitHub CLI: https://cli.github.com/
2. Autenticarse:
   ```bash
   gh auth login
   ```

### Ejecutar el Script Automático

Simplemente ejecuta:
```bash
setup_git_repos.bat
```

El script hará todo automáticamente.

---

## Verificación

Después de crear los repositorios, verifica:

1. **Repositorio Local:**
   - URL: https://github.com/TU_USUARIO/proyecto-de-titulo-local
   - Debe contener todo el código del proyecto

2. **Repositorio Producción:**
   - URL: https://github.com/TU_USUARIO/proyecto-de-titulo-produccion
   - Debe estar vacío (se usará para deployment)

---

## Próximos Pasos

1. ✅ Repositorios creados
2. 📝 Configurar deployment (ver `DEPLOYMENT_GUIDE.md`)
3. 🚀 Hacer deploy a producción

---

## Troubleshooting

### Error: "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/TU_USUARIO/proyecto-de-titulo-local.git
```

### Error: "Authentication failed"
```bash
# Usar GitHub CLI
gh auth login

# O configurar token manualmente
git config --global credential.helper store
```

### Error: "Permission denied"
- Verifica que el repositorio sea tuyo
- Verifica que tengas permisos de escritura
- Revoca y crea un nuevo token si es necesario

---

## Seguridad

⚠️ **NUNCA** compartas:
- Tokens de acceso personal
- Archivos `.env`
- Credenciales de base de datos
- Claves SSH privadas

Estos archivos ya están en `.gitignore` y no se subirán al repositorio.
