# Script para instalar Redis en Windows
Write-Host "🔧 Instalando Redis para Windows..." -ForegroundColor Green

# Crear directorio para Redis
$redisDir = "$env:USERPROFILE\redis"
if (-not (Test-Path $redisDir)) {
    New-Item -ItemType Directory -Path $redisDir | Out-Null
}

Write-Host "📥 Descargando Redis..." -ForegroundColor Yellow

# URL de Redis para Windows (versión 5.0.14.1)
$redisUrl = "https://github.com/microsoftarchive/redis/releases/download/win-3.0.504/Redis-x64-3.0.504.zip"
$zipFile = "$redisDir\redis.zip"

try {
    # Descargar Redis
    Invoke-WebRequest -Uri $redisUrl -OutFile $zipFile -UseBasicParsing
    
    Write-Host "📦 Extrayendo archivos..." -ForegroundColor Yellow
    
    # Extraer ZIP
    Expand-Archive -Path $zipFile -DestinationPath $redisDir -Force
    
    # Limpiar ZIP
    Remove-Item $zipFile
    
    Write-Host "✅ Redis instalado en: $redisDir" -ForegroundColor Green
    Write-Host ""
    Write-Host "🚀 Para iniciar Redis, ejecuta:" -ForegroundColor Cyan
    Write-Host "   cd $redisDir" -ForegroundColor White
    Write-Host "   .\redis-server.exe" -ForegroundColor White
    Write-Host ""
    Write-Host "💡 O ejecuta este comando desde aquí:" -ForegroundColor Cyan
    Write-Host "   Start-Process ""$redisDir\redis-server.exe""" -ForegroundColor White
    
} catch {
    Write-Host "❌ Error al descargar Redis: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "📝 Alternativa: Descarga manual" -ForegroundColor Yellow
    Write-Host "   1. Ve a: https://github.com/microsoftarchive/redis/releases" -ForegroundColor White
    Write-Host "   2. Descarga: Redis-x64-3.0.504.zip" -ForegroundColor White
    Write-Host "   3. Extrae en: $redisDir" -ForegroundColor White
}
