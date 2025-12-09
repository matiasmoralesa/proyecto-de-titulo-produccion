# ⚡ Comandos Rápidos - Deployment Dashboard

## 🚀 Deployment Rápido (5 minutos)

### Windows:
```cmd
cd frontend
verify-dashboard.bat
cd ..
git add .
git commit -m "feat: Mejorar dashboard con KPIs visuales y gráficos interactivos"
git push origin main
```

### Linux/Mac:
```bash
cd frontend
chmod +x verify-dashboard.sh
./verify-dashboard.sh
cd ..
git add .
git commit -m "feat: Mejorar dashboard con KPIs visuales y gráficos interactivos"
git push origin main
```

## 🔍 Verificaciones Pre-Deployment

### Verificación Completa:
```bash
cd frontend

# 1. Verificar TypeScript
npm run build:check

# 2. Verificar Linting
npm run lint

# 3. Build local
npm run build

# 4. Verificar dependencias
npm list recharts
npm list react-icons
```

### Verificación Rápida:
```bash
cd frontend
npm run build
```

## 🔄 Deployment con Preview (Recomendado)

```bash
# 1. Crear rama
git checkout -b feature/dashboard-improvements

# 2. Commit
git add .
git commit -m "feat: Mejorar dashboard con KPIs y gráficos"

# 3. Push
git push origin feature/dashboard-improvements

# 4. Ir a GitHub y crear Pull Request
# 5. Vercel creará preview automáticamente
# 6. Revisar preview y hacer merge
```

## 🐛 Rollback Rápido

### Opción 1 - Vercel Dashboard:
1. Ir a https://vercel.com/dashboard
2. Seleccionar proyecto
3. Click en deployment anterior
4. Click "Promote to Production"

### Opción 2 - Git Revert:
```bash
git revert HEAD
git push origin main
```

### Opción 3 - Rollback Manual:
```bash
git checkout HEAD~1 frontend/src/pages/Dashboard.tsx
git commit -m "revert: Revertir mejoras del dashboard"
git push origin main
```

## 🔧 Troubleshooting

### Error: recharts no encontrado
```bash
cd frontend
npm install recharts@^2.10.3
npm run build
```

### Error: Build falla
```bash
cd frontend
rm -rf node_modules
rm -rf dist
npm install
npm run build
```

### Error: TypeScript
```bash
cd frontend
npm run build:check
# Revisar errores y corregir
```

### Limpiar caché
```bash
cd frontend
rm -rf node_modules
rm -rf dist
rm -rf .vite
npm install
npm run build
```

## 📊 Verificar en Producción

### Después del deployment:
```bash
# Abrir en navegador
start https://tu-proyecto.vercel.app

# O en Linux/Mac
open https://tu-proyecto.vercel.app
```

### Verificar logs de Vercel:
```bash
# Instalar Vercel CLI (si no está instalado)
npm i -g vercel

# Ver logs
vercel logs
```

## 🧪 Testing Local

### Ejecutar en desarrollo:
```bash
cd frontend
npm run dev
# Abrir http://localhost:5173
```

### Build y preview local:
```bash
cd frontend
npm run build
npm run preview
# Abrir http://localhost:4173
```

## 📦 Gestión de Dependencias

### Ver dependencias instaladas:
```bash
cd frontend
npm list --depth=0
```

### Actualizar dependencias:
```bash
cd frontend
npm update
```

### Verificar vulnerabilidades:
```bash
cd frontend
npm audit
```

## 🔐 Variables de Entorno

### Verificar variables:
```bash
cd frontend
cat .env.production
```

### Actualizar en Vercel:
1. Ir a Vercel Dashboard
2. Settings → Environment Variables
3. Agregar/Actualizar variables
4. Redeploy

## 📈 Monitoreo

### Ver analytics de Vercel:
```bash
# Abrir dashboard
start https://vercel.com/dashboard/analytics
```

### Ver logs en tiempo real:
```bash
vercel logs --follow
```

## 🎯 Comandos Útiles

### Ver status de Git:
```bash
git status
git log --oneline -5
```

### Ver branches:
```bash
git branch -a
```

### Cambiar de branch:
```bash
git checkout main
git checkout -b nueva-rama
```

### Ver diferencias:
```bash
git diff
git diff HEAD~1
```

### Deshacer cambios locales:
```bash
git checkout -- frontend/src/pages/Dashboard.tsx
```

## 🚨 Comandos de Emergencia

### Rollback inmediato:
```bash
git revert HEAD --no-edit
git push origin main
```

### Forzar push (usar con cuidado):
```bash
git push origin main --force
```

### Resetear a commit anterior:
```bash
git reset --hard HEAD~1
git push origin main --force
```

## 📝 Notas

- Siempre ejecutar `verify-dashboard` antes de deployment
- Usar deployment con preview para máxima seguridad
- Monitorear logs después del deployment
- Tener plan de rollback listo
- Notificar al equipo antes y después

## ✅ Checklist Rápido

```bash
# 1. Verificar
cd frontend && verify-dashboard.bat

# 2. Commit
git add . && git commit -m "feat: Dashboard mejorado"

# 3. Push
git push origin main

# 4. Monitorear
# Ir a Vercel Dashboard

# 5. Verificar
# Abrir sitio en producción

# 6. Confirmar
# Todo funciona correctamente
```

---

**Tip:** Guarda este archivo como referencia rápida para futuros deployments.
