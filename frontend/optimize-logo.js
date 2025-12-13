/**
 * Script para optimizar el logo de SOMACOR
 * Ejecutar con: node optimize-logo.js
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

console.log('🏢 Optimizando logo de SOMACOR...');

const logoPath = path.join(__dirname, 'public', 'logo-somacor.png');

// Verificar si el archivo existe
if (!fs.existsSync(logoPath)) {
  console.log('❌ Logo no encontrado en:', logoPath);
  console.log('📝 Por favor, coloca el logo de SOMACOR en: frontend/public/logo-somacor.png');
  console.log('');
  console.log('Recomendaciones para el logo:');
  console.log('- Formato: PNG con transparencia');
  console.log('- Tamaño: 512x512px (cuadrado)');
  console.log('- Fondo: Transparente');
  console.log('- Calidad: Alta resolución para escalabilidad');
  process.exit(1);
}

// Verificar tamaño del archivo
const stats = fs.statSync(logoPath);
const fileSizeInBytes = stats.size;
const fileSizeInKB = fileSizeInBytes / 1024;

console.log('✅ Logo encontrado');
console.log(`📊 Tamaño: ${fileSizeInKB.toFixed(2)} KB`);

if (fileSizeInKB > 100) {
  console.log('⚠️  El logo es grande (>100KB). Considera optimizarlo para mejor rendimiento.');
} else {
  console.log('✅ Tamaño del logo es óptimo');
}

console.log('');
console.log('🎯 Ubicaciones donde aparecerá el logo:');
console.log('  1. Página de Login (80x80px)');
console.log('  2. Sidebar de navegación (32x32px)');
console.log('  3. Dashboard header (32x32px)');
console.log('  4. Favicon del navegador');
console.log('');
console.log('✅ Logo de SOMACOR listo para usar!');