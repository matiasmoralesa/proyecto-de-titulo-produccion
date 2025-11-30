# Script simple para instalar Redis
Write-Host "Instalando Redis para Windows..."

$redisDir = "$env:USERPROFILE\redis"
New-Item -ItemType Directory -Path $redisDir -Force | Out-Null

$redisUrl = "https://github.com/microsoftarchive/redis/releases/download/win-3.0.504/Redis-x64-3.0.504.zip"
$zipFile = "$redisDir\redis.zip"

Write-Host "Descargando Redis..."
Invoke-WebRequest -Uri $redisUrl -OutFile $zipFile -UseBasicParsing

Write-Host "Extrayendo archivos..."
Expand-Archive -Path $zipFile -DestinationPath $redisDir -Force

Remove-Item $zipFile

Write-Host "Redis instalado en: $redisDir"
Write-Host "Para iniciar Redis: cd $redisDir y ejecuta redis-server.exe"
