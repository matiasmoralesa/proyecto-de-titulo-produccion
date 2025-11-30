/**
 * Component to view checklist templates
 */
import React, { useEffect, useState } from 'react';
import { ChecklistTemplate } from '../../types/checklist';
import { checklistService } from '../../services/checklistService';

interface ChecklistTemplateViewerProps {
  templateId?: number;
  vehicleType?: string;
  onSelectTemplate?: (template: ChecklistTemplate) => void;
}

const ChecklistTemplateViewer: React.FC<ChecklistTemplateViewerProps> = ({
  templateId,
  vehicleType,
  onSelectTemplate,
}) => {
  const [templates, setTemplates] = useState<ChecklistTemplate[]>([]);
  const [selectedTemplate, setSelectedTemplate] = useState<ChecklistTemplate | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadTemplates();
  }, [vehicleType]);

  useEffect(() => {
    if (templateId) {
      loadTemplate(templateId);
    }
  }, [templateId]);

  const loadTemplates = async () => {
    try {
      setLoading(true);
      const data = vehicleType
        ? await checklistService.getTemplatesByVehicleType(vehicleType)
        : await checklistService.getTemplates();
      setTemplates(data);
      
      if (data.length > 0 && !selectedTemplate) {
        setSelectedTemplate(data[0]);
      }
    } catch (err: any) {
      setError(err.message || 'Error al cargar plantillas');
    } finally {
      setLoading(false);
    }
  };

  const loadTemplate = async (id: number) => {
    try {
      setLoading(true);
      const data = await checklistService.getTemplate(id);
      setSelectedTemplate(data);
    } catch (err: any) {
      setError(err.message || 'Error al cargar plantilla');
    } finally {
      setLoading(false);
    }
  };

  const handleSelectTemplate = (template: ChecklistTemplate) => {
    setSelectedTemplate(template);
    if (onSelectTemplate) {
      onSelectTemplate(template);
    }
  };

  const groupItemsBySection = (template: ChecklistTemplate) => {
    const sections: { [key: string]: typeof template.items } = {};
    
    template.items.forEach((item) => {
      if (!sections[item.section]) {
        sections[item.section] = [];
      }
      sections[item.section].push(item);
    });
    
    return sections;
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center p-8">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
        {error}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Template Selector */}
      {templates.length > 1 && (
        <div className="bg-white rounded-lg shadow p-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Seleccionar Plantilla
          </label>
          <select
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={selectedTemplate?.id || ''}
            onChange={(e) => {
              const template = templates.find((t) => t.id === Number(e.target.value));
              if (template) handleSelectTemplate(template);
            }}
          >
            {templates.map((template) => (
              <option key={template.id} value={template.id}>
                {template.code} - {template.name}
              </option>
            ))}
          </select>
        </div>
      )}

      {/* Template Details */}
      {selectedTemplate && (
        <div className="bg-white rounded-lg shadow">
          {/* Header */}
          <div className="border-b border-gray-200 p-6">
            <div className="flex items-start justify-between">
              <div>
                <h2 className="text-2xl font-bold text-gray-900">{selectedTemplate.name}</h2>
                <p className="text-sm text-gray-500 mt-1">Código: {selectedTemplate.code}</p>
              </div>
              <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800">
                {selectedTemplate.is_system_template ? 'Sistema' : 'Personalizada'}
              </span>
            </div>
            
            {selectedTemplate.description && (
              <p className="mt-4 text-gray-600">{selectedTemplate.description}</p>
            )}
            
            <div className="mt-4 grid grid-cols-3 gap-4">
              <div>
                <p className="text-sm text-gray-500">Total de Items</p>
                <p className="text-lg font-semibold text-gray-900">{selectedTemplate.total_items}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Items Requeridos</p>
                <p className="text-lg font-semibold text-gray-900">{selectedTemplate.required_items_count}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Puntuación Mínima</p>
                <p className="text-lg font-semibold text-gray-900">{selectedTemplate.passing_score}%</p>
              </div>
            </div>
          </div>

          {/* Items by Section */}
          <div className="p-6 space-y-6">
            {Object.entries(groupItemsBySection(selectedTemplate)).map(([section, items]) => (
              <div key={section} className="border-l-4 border-blue-500 pl-4">
                <h3 className="text-lg font-semibold text-gray-900 mb-3">{section}</h3>
                <div className="space-y-2">
                  {items.map((item) => (
                    <div
                      key={item.id}
                      className="flex items-start space-x-3 p-3 bg-gray-50 rounded-lg"
                    >
                      <span className="flex-shrink-0 w-8 h-8 flex items-center justify-center bg-blue-100 text-blue-800 rounded-full text-sm font-medium">
                        {item.order}
                      </span>
                      <div className="flex-1">
                        <p className="text-gray-900">{item.question}</p>
                        <div className="mt-1 flex items-center space-x-4 text-xs text-gray-500">
                          <span className="inline-flex items-center">
                            Tipo: {item.response_type === 'yes_no_na' ? 'Sí/No/NA' : item.response_type}
                          </span>
                          {item.required && (
                            <span className="inline-flex items-center text-red-600">
                              * Requerido
                            </span>
                          )}
                          {item.observations_allowed && (
                            <span className="inline-flex items-center">
                              📝 Permite observaciones
                            </span>
                          )}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default ChecklistTemplateViewer;
