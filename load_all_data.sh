#!/bin/bash
echo "========================================="
echo "Cargando datos en producción (Railway)"
echo "========================================="

echo ""
echo "1️⃣  Cargando Roles..."
python manage.py loaddata backend/roles_export.json
if [ $? -eq 0 ]; then
    echo "   ✅ Roles cargados"
else
    echo "   ❌ Error cargando roles"
    exit 1
fi

echo ""
echo "2️⃣  Cargando Plantillas de Checklist..."
python manage.py loaddata backend/checklist_templates_export.json
if [ $? -eq 0 ]; then
    echo "   ✅ Plantillas cargadas"
else
    echo "   ❌ Error cargando plantillas"
    exit 1
fi

echo ""
echo "3️⃣  Cargando Prioridades..."
python manage.py loaddata backend/priorities_export.json
if [ $? -eq 0 ]; then
    echo "   ✅ Prioridades cargadas"
else
    echo "   ❌ Error cargando prioridades"
    exit 1
fi

echo ""
echo "4️⃣  Cargando Tipos de Orden de Trabajo..."
python manage.py loaddata backend/workorder_types_export.json
if [ $? -eq 0 ]; then
    echo "   ✅ Tipos de OT cargados"
else
    echo "   ❌ Error cargando tipos de OT"
    exit 1
fi

echo ""
echo "5️⃣  Cargando Categorías de Activos..."
python manage.py loaddata backend/asset_categories_export.json
if [ $? -eq 0 ]; then
    echo "   ✅ Categorías cargadas"
else
    echo "   ❌ Error cargando categorías"
    exit 1
fi

echo ""
echo "6️⃣  Cargando Ubicaciones..."
python manage.py loaddata backend/locations_export.json
if [ $? -eq 0 ]; then
    echo "   ✅ Ubicaciones cargadas"
else
    echo "   ❌ Error cargando ubicaciones"
    exit 1
fi

echo ""
echo "========================================="
echo "✅ Todos los datos cargados exitosamente!"
echo "========================================="
echo ""
echo "Ejecutando verificación..."
python backend/check_production_data.py
