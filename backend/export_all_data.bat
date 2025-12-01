@echo off
echo ========================================
echo Exportando Datos de Produccion
echo ========================================

echo.
echo Exportando Roles...
python manage.py dumpdata authentication.Role --indent 2 --output roles_export.json

echo Exportando Plantillas de Checklist...
python manage.py dumpdata checklists.ChecklistTemplate --indent 2 --output checklist_templates_export.json

echo Exportando Prioridades...
python manage.py dumpdata configuration.Priority --indent 2 --output priorities_export.json

echo Exportando Tipos de Orden de Trabajo...
python manage.py dumpdata configuration.WorkOrderType --indent 2 --output workorder_types_export.json

echo Exportando Categorias de Activos...
python manage.py dumpdata configuration.AssetCategory --indent 2 --output asset_categories_export.json

echo Exportando Ubicaciones...
python manage.py dumpdata assets.Location --indent 2 --output locations_export.json

echo.
echo ========================================
echo Exportacion Completada!
echo ========================================
echo.
echo Archivos generados:
echo - roles_export.json
echo - checklist_templates_export.json
echo - priorities_export.json
echo - workorder_types_export.json
echo - asset_categories_export.json
echo - locations_export.json
echo.
echo Para cargar en produccion:
echo railway run python manage.py loaddata roles_export.json
echo railway run python manage.py loaddata checklist_templates_export.json
echo railway run python manage.py loaddata priorities_export.json
echo railway run python manage.py loaddata workorder_types_export.json
echo railway run python manage.py loaddata asset_categories_export.json
echo railway run python manage.py loaddata locations_export.json
