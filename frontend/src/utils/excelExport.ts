/**
 * Utilidad para exportar datos a Excel con formato profesional
 */
import * as XLSX from 'xlsx';

interface ExcelColumn {
  header: string;
  key: string;
  width?: number;
  format?: 'text' | 'number' | 'date' | 'currency';
}

interface ExcelExportOptions {
  filename: string;
  sheetName: string;
  title?: string;
  subtitle?: string;
  columns: ExcelColumn[];
  data: any[];
  includeDate?: boolean;
}

/**
 * Formatea un valor según su tipo
 */
const formatValue = (value: any, format?: string): any => {
  if (value === null || value === undefined) return '';
  
  switch (format) {
    case 'date':
      if (value instanceof Date) {
        return value.toLocaleDateString('es-CL');
      }
      if (typeof value === 'string') {
        const date = new Date(value);
        return isNaN(date.getTime()) ? value : date.toLocaleDateString('es-CL');
      }
      return value;
    
    case 'currency':
      if (typeof value === 'number') {
        return `$${value.toLocaleString('es-CL')}`;
      }
      return value;
    
    case 'number':
      if (typeof value === 'number') {
        return value.toLocaleString('es-CL');
      }
      return value;
    
    default:
      return value;
  }
};

/**
 * Traduce valores comunes al español
 */
const translateValue = (value: any): any => {
  if (typeof value !== 'string') return value;
  
  const translations: Record<string, string> = {
    // Estados
    'PENDING': 'Pendiente',
    'IN_PROGRESS': 'En Progreso',
    'COMPLETED': 'Completada',
    'CANCELLED': 'Cancelada',
    
    // Prioridades
    'LOW': 'Baja',
    'MEDIUM': 'Media',
    'HIGH': 'Alta',
    'CRITICAL': 'Crítica',
    
    // Tipos
    'PREVENTIVE': 'Preventivo',
    'CORRECTIVE': 'Correctivo',
    'PREDICTIVE': 'Predictivo',
    
    // Estados de activos
    'OPERATIONAL': 'Operando',
    'MAINTENANCE': 'En Mantenimiento',
    'OUT_OF_SERVICE': 'Fuera de Servicio',
    'STOPPED': 'Detenida',
  };
  
  return translations[value] || value;
};

/**
 * Exporta datos a Excel con formato profesional
 */
export const exportToExcel = (options: ExcelExportOptions): void => {
  const {
    filename,
    sheetName,
    title,
    subtitle,
    columns,
    data,
    includeDate = true,
  } = options;

  // Crear workbook
  const wb = XLSX.utils.book_new();
  
  // Preparar datos para la hoja
  const worksheetData: any[][] = [];
  
  // Agregar título si existe
  if (title) {
    worksheetData.push([title]);
    worksheetData.push([]); // Fila vacía
  }
  
  // Agregar subtítulo si existe
  if (subtitle) {
    worksheetData.push([subtitle]);
    worksheetData.push([]); // Fila vacía
  }
  
  // Agregar fecha si se solicita
  if (includeDate) {
    worksheetData.push([`Fecha de generación: ${new Date().toLocaleString('es-CL')}`]);
    worksheetData.push([]); // Fila vacía
  }
  
  // Agregar encabezados
  const headers = columns.map(col => col.header);
  worksheetData.push(headers);
  
  // Agregar datos
  data.forEach(row => {
    const rowData = columns.map(col => {
      const value = row[col.key];
      const translated = translateValue(value);
      return formatValue(translated, col.format);
    });
    worksheetData.push(rowData);
  });
  
  // Crear worksheet
  const ws = XLSX.utils.aoa_to_sheet(worksheetData);
  
  // Configurar anchos de columna
  const colWidths = columns.map(col => ({
    wch: col.width || 15
  }));
  ws['!cols'] = colWidths;
  
  // Agregar worksheet al workbook
  XLSX.utils.book_append_sheet(wb, ws, sheetName);
  
  // Generar archivo
  const excelBuffer = XLSX.write(wb, { bookType: 'xlsx', type: 'array' });
  const blob = new Blob([excelBuffer], { 
    type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' 
  });
  
  // Descargar archivo
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `${filename}_${new Date().toISOString().split('T')[0]}.xlsx`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  window.URL.revokeObjectURL(url);
};

/**
 * Exporta órdenes de trabajo a Excel
 */
export const exportWorkOrdersToExcel = (workOrders: any[]): void => {
  exportToExcel({
    filename: 'ordenes_trabajo',
    sheetName: 'Órdenes de Trabajo',
    title: 'REPORTE DE ÓRDENES DE TRABAJO',
    subtitle: 'Sistema de Gestión de Mantenimiento - SOMACOR',
    columns: [
      { header: 'N° Orden', key: 'work_order_number', width: 15 },
      { header: 'Título', key: 'title', width: 30 },
      { header: 'Activo', key: 'asset_name', width: 25 },
      { header: 'Estado', key: 'status', width: 15 },
      { header: 'Prioridad', key: 'priority', width: 12 },
      { header: 'Tipo', key: 'work_order_type', width: 15 },
      { header: 'Asignado a', key: 'assigned_to_name', width: 25 },
      { header: 'Fecha Creación', key: 'created_at', width: 18, format: 'date' },
      { header: 'Fecha Completado', key: 'completed_date', width: 18, format: 'date' },
      { header: 'Horas Trabajadas', key: 'actual_hours', width: 15, format: 'number' },
    ],
    data: workOrders,
  });
};

/**
 * Exporta downtime de activos a Excel
 */
export const exportAssetDowntimeToExcel = (downtimeData: any[]): void => {
  exportToExcel({
    filename: 'downtime_activos',
    sheetName: 'Downtime de Activos',
    title: 'REPORTE DE TIEMPO FUERA DE SERVICIO',
    subtitle: 'Sistema de Gestión de Mantenimiento - SOMACOR',
    columns: [
      { header: 'ID Activo', key: 'asset__id', width: 12 },
      { header: 'Nombre Activo', key: 'asset__name', width: 30 },
      { header: 'Tipo de Vehículo', key: 'asset__vehicle_type', width: 25 },
      { header: 'Tiempo Fuera de Servicio (hrs)', key: 'total_downtime', width: 25, format: 'number' },
      { header: 'Cantidad de Órdenes', key: 'work_order_count', width: 20, format: 'number' },
    ],
    data: downtimeData,
  });
};

/**
 * Exporta consumo de repuestos a Excel
 */
export const exportSparePartsToExcel = (sparePartsData: any[]): void => {
  exportToExcel({
    filename: 'consumo_repuestos',
    sheetName: 'Consumo de Repuestos',
    title: 'REPORTE DE CONSUMO DE REPUESTOS',
    subtitle: 'Sistema de Gestión de Mantenimiento - SOMACOR',
    columns: [
      { header: 'ID', key: 'spare_part__id', width: 10 },
      { header: 'N° Parte', key: 'spare_part__part_number', width: 15 },
      { header: 'Nombre', key: 'spare_part__name', width: 35 },
      { header: 'Cantidad Consumida', key: 'total_quantity', width: 20, format: 'number' },
      { header: 'N° Movimientos', key: 'movement_count', width: 18, format: 'number' },
    ],
    data: sparePartsData,
  });
};

/**
 * Exporta activos a Excel
 */
export const exportAssetsToExcel = (assets: any[]): void => {
  exportToExcel({
    filename: 'activos',
    sheetName: 'Activos',
    title: 'LISTADO DE ACTIVOS',
    subtitle: 'Sistema de Gestión de Mantenimiento - SOMACOR',
    columns: [
      { header: 'ID', key: 'id', width: 10 },
      { header: 'Nombre', key: 'name', width: 30 },
      { header: 'Tipo de Vehículo', key: 'vehicle_type', width: 25 },
      { header: 'Marca', key: 'brand', width: 15 },
      { header: 'Modelo', key: 'model', width: 15 },
      { header: 'Año', key: 'year', width: 10, format: 'number' },
      { header: 'Patente', key: 'license_plate', width: 12 },
      { header: 'Estado', key: 'status', width: 18 },
      { header: 'Ubicación', key: 'location', width: 20 },
      { header: 'Fecha Adquisición', key: 'acquisition_date', width: 18, format: 'date' },
    ],
    data: assets,
  });
};

/**
 * Exporta inventario a Excel
 */
export const exportInventoryToExcel = (inventory: any[]): void => {
  exportToExcel({
    filename: 'inventario_repuestos',
    sheetName: 'Inventario',
    title: 'INVENTARIO DE REPUESTOS',
    subtitle: 'Sistema de Gestión de Mantenimiento - SOMACOR',
    columns: [
      { header: 'N° Parte', key: 'part_number', width: 15 },
      { header: 'Nombre', key: 'name', width: 35 },
      { header: 'Categoría', key: 'category', width: 20 },
      { header: 'Fabricante', key: 'manufacturer', width: 20 },
      { header: 'Stock Actual', key: 'quantity', width: 15, format: 'number' },
      { header: 'Stock Mínimo', key: 'min_quantity', width: 15, format: 'number' },
      { header: 'Unidad', key: 'unit_of_measure', width: 12 },
      { header: 'Costo Unitario', key: 'unit_cost', width: 15, format: 'currency' },
      { header: 'Ubicación', key: 'storage_location', width: 25 },
      { header: 'Estado', key: 'stock_status', width: 15 },
    ],
    data: inventory.map(item => ({
      ...item,
      stock_status: item.quantity === 0 ? 'Sin Stock' : 
                    item.quantity <= item.min_quantity ? 'Stock Bajo' : 
                    'Stock Normal'
    })),
  });
};
