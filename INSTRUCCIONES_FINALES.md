# 🚀 Instrucciones Finales - Setup de Repositorios GitHub

## ✅ Archivos Creados

He preparado todo lo necesario para crear y desplegar tus repositorios:

### Scripts
- ✅ `setup_git_repos.bat` - Script automático para crear repositorios
- ✅ `prepare_for_production.py` - Script de preparación para producción

### Documentación
- ✅ `GITHUB_SETUP_MANUAL.md` - Guía manual si prefieres hacerlo paso a paso
- ✅ `DEPLOYMENT_GUIDE.md` - Guía completa de deployment
- ✅ `README_PRODUCCION.md` - README para el repo de producción
- ✅ `.env.production.template` - Template de variables de entorno

---

## 🎯 Pasos para Ejecutar

### Paso 1: Preparar el Proyecto

Abre PowerShell o CMD en la carpeta del proyecto y ejecuta:

```bash
python prepare_for_production.py
```

Este script verificará:
- ✅ Configuraciones de seguridad
- ✅ Dependencias
- ✅ Documentación
- ✅ Generará archivos necesarios

### Paso 2: Crear Repositorios en GitHub

**Opción A: Automático (Recomendado)**

```bash
setup_git_repos.bat
```

El script te pedirá autenticarte en GitHub (si no lo estás) y luego:
1. Inicializará Git en tu proyecto
2. Creará el commit inicial
3. Creará el repositorio `proyecto-de-titulo-local` en GitHub
4. Subirá todo el código
5. Creará el repositorio `proyecto-de-titulo-produccion` (vacío)

**Opción B: Manual**

Si prefieres hacerlo manualmente, sigue la guía en:
```
GITHUB_SETUP_MANUAL.md
```

---

## 📋 Requisitos Previos

### Para Opción Automática:

1. **GitHub CLI instalado**
   - Descargar de: https://cli.github.com/
   - O instalar con: `winget install GitHub.cli`

2. **Git instalado**
   - Descargar de: https://git-scm.com/
   - O instalar con: `winget install Git.Git`

3. **Cuenta de GitHub**
   - Tener una cuenta activa en https://github.com

### Para Opción Manual:

Solo necesitas:
- Cuenta de GitHub
- Git instalado

---

## 🔍 Verificación

Después de ejecutar el script, verifica:

### 1. Repositorio Local Creado
```bash
# Verificar que Git está inicializado
git status

# Deberías ver: "On branch main"
```

### 2. Repositorios en GitHub

Ve a tu perfil de GitHub y verifica que existen:

1. **proyecto-de-titulo-local**
   - URL: `https://github.com/TU_USUARIO/proyecto-de-titulo-local`
   - Debe contener todo el código
   - Debe tener el commit inicial

2. **proyecto-de-titulo-produccion**
   - URL: `https://github.com/TU_USUARIO/proyecto-de-titulo-produccion`
   - Debe estar vacío (se usará para deployment)

### 3. Verificar Archivos Subidos

```bash
# Ver commits
git log

# Ver archivos trackeados
git ls-files
```

---

## 🎉 ¿Qué Sigue?

Una vez que los repositorios estén creados:

### 1. Configurar Deployment

Sigue la guía completa en:
```
DEPLOYMENT_GUIDE.md
```

### 2. Preparar para Producción

- Configurar variables de entorno (`.env.production`)
- Configurar servidor (VPS, AWS, DigitalOcean, etc.)
- Configurar PostgreSQL
- Configurar Redis
- Configurar Nginx

### 3. Deploy a Producción

```bash
# En el servidor de producción
git clone https://github.com/TU_USUARIO/proyecto-de-titulo-produccion.git
cd proyecto-de-titulo-produccion

# Seguir pasos en DEPLOYMENT_GUIDE.md
```

---

## 🔐 Seguridad - MUY IMPORTANTE

### ⚠️ NUNCA subas a Git:

- ❌ Archivos `.env` (con credenciales reales)
- ❌ `db.sqlite3` (base de datos con datos reales)
- ❌ Tokens de acceso
- ❌ Claves privadas
- ❌ Passwords

### ✅ Estos archivos YA están en .gitignore:

- `.env`
- `db.sqlite3`
- `*.log`
- `__pycache__/`
- `node_modules/`
- `venv/`
- `/media` (archivos subidos)

---

## 🆘 Troubleshooting

### Error: "gh: command not found"

**Solución:** Instalar GitHub CLI
```bash
winget install GitHub.cli
```

Luego reinicia la terminal y vuelve a ejecutar el script.

### Error: "git: command not found"

**Solución:** Instalar Git
```bash
winget install Git.Git
```

Luego reinicia la terminal y vuelve a ejecutar el script.

### Error: "Authentication failed"

**Solución:** Autenticarse en GitHub CLI
```bash
gh auth login
```

Sigue las instrucciones en pantalla.

### Error: "Repository already exists"

**Solución:** 
1. Ve a GitHub y elimina el repositorio existente
2. O usa un nombre diferente editando `setup_git_repos.bat`

### Error: "Permission denied"

**Solución:** Ejecuta PowerShell o CMD como Administrador

---

## 📞 Comandos Útiles

```bash
# Ver estado de Git
git status

# Ver repositorios remotos
git remote -v

# Ver commits
git log --oneline

# Ver archivos ignorados
git status --ignored

# Ver repositorios en GitHub
gh repo list

# Ver detalles de un repo
gh repo view proyecto-de-titulo-local

# Abrir repo en navegador
gh repo view proyecto-de-titulo-local --web
```

---

## 📊 Estructura Final

Después de ejecutar todo, tendrás:

```
Tu Cuenta de GitHub
├── proyecto-de-titulo-local/
│   ├── backend/
│   ├── frontend/
│   ├── docs/
│   ├── README.md
│   └── ... (todo el código)
│
└── proyecto-de-titulo-produccion/
    └── (vacío, listo para deployment)
```

---

## ✅ Checklist Final

Antes de considerar completo el setup:

- [ ] `prepare_for_production.py` ejecutado sin errores
- [ ] `setup_git_repos.bat` ejecutado exitosamente
- [ ] Repositorio `proyecto-de-titulo-local` creado en GitHub
- [ ] Repositorio `proyecto-de-titulo-produccion` creado en GitHub
- [ ] Código subido al repositorio local
- [ ] `.gitignore` configurado correctamente
- [ ] Archivos sensibles NO subidos a Git
- [ ] README actualizado
- [ ] Documentación revisada

---

## 🎓 Próximos Pasos

1. ✅ **Repositorios creados** ← Estás aquí
2. 📝 **Configurar deployment** (ver DEPLOYMENT_GUIDE.md)
3. 🚀 **Deploy a producción**
4. 📊 **Monitoreo y mantenimiento**

---

## 📞 Soporte

Si tienes problemas:

1. Revisa la sección de Troubleshooting arriba
2. Consulta `GITHUB_SETUP_MANUAL.md` para método manual
3. Verifica que Git y GitHub CLI estén instalados
4. Verifica tu conexión a internet

---

**¡Listo para crear tus repositorios!** 🚀

Ejecuta: `setup_git_repos.bat`
