/**
 * Component to view completed checklists
 */
import React, { useEffect, useState } from 'react';
import { ChecklistResponse } from '../../types/checklist';
import { checklistService } from '../../services/checklistService';

interface ChecklistViewerProps {
  checklistId: number;
  onClose?: () => void;
}

const ChecklistViewer: React.FC<ChecklistViewerProps> = ({ checklistId, onClose }) => {
  const [checklist, setChecklist] = useState<ChecklistResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [downloading, setDownloading] = useState(false);

  useEffect(() => {
    loadChecklist();
  }, [checklistId]);

  const loadChecklist = async () => {
    try {
      setLoading(true);
      const data = await checklistService.getResponse(checklistId);
      setChecklist(data);
    } catch (err: any) {
      setError(err.message || 'Error al cargar checklist');
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadPDF = async () => {
    if (!checklist) return;
    
    try {
      setDownloading(true);
      const blob = await checklistService.downloadPDF(checklist.id);
      
      // Create download link
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `checklist_${checklist.id}.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (err: any) {
      setError(err.message || 'Error al descargar PDF');
    } finally {
      setDownloading(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'APPROVED':
        return 'bg-green-100 text-green-800';
      case 'REJECTED':
        return 'bg-red-100 text-red-800';
      case 'COMPLETED':
        return 'bg-blue-100 text-blue-800';
      case 'IN_PROGRESS':
        return 'bg-yellow-100 text-yellow-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'APPROVED':
        return 'Aprobado';
      case 'REJECTED':
        return 'Rechazado';
      case 'COMPLETED':
        return 'Completado';
      case 'IN_PROGRESS':
        return 'En Progreso';
      default:
        return status;
    }
  };

  const groupItemsBySection = () => {
    if (!checklist) return {};
    
    const sections: { [key: string]: typeof checklist.item_responses } = {};
    
    checklist.item_responses.forEach((response) => {
      const section = response.template_item?.section || 'Sin Sección';
      if (!sections[section]) {
        sections[section] = [];
      }
      sections[section].push(response);
    });
    
    return sections;
  };

  const formatResponseValue = (value: string) => {
    switch (value) {
      case 'yes':
        return <span className="text-green-600 font-semibold">✓ Sí</span>;
      case 'no':
        return <span className="text-red-600 font-semibold">✗ No</span>;
      case 'na':
        return <span className="text-gray-600 font-semibold">○ N/A</span>;
      default:
        return value;
    }
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

  if (!checklist) {
    return null;
  }

  return (
    <div className="bg-white rounded-lg shadow-lg">
      {/* Header */}
      <div className="border-b border-gray-200 p-6">
        <div className="flex items-start justify-between mb-4">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">{checklist.template.name}</h2>
            <p className="text-sm text-gray-500 mt-1">Código: {checklist.template.code}</p>
          </div>
          <div className="flex items-center space-x-2">
            <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(checklist.status)}`}>
              {getStatusText(checklist.status)}
            </span>
            {onClose && (
              <button
                onClick={onClose}
                className="text-gray-400 hover:text-gray-600"
              >
                ✕
              </button>
            )}
          </div>
        </div>

        {/* Info Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div>
            <p className="text-sm text-gray-500">Activo</p>
            <p className="font-semibold text-gray-900">{checklist.asset.name}</p>
            <p className="text-xs text-gray-500">{checklist.asset.license_plate}</p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Completado Por</p>
            <p className="font-semibold text-gray-900">{checklist.completed_by_name || 'N/A'}</p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Fecha</p>
            <p className="font-semibold text-gray-900">
              {checklist.completed_at
                ? new Date(checklist.completed_at).toLocaleDateString('es-ES')
                : 'N/A'}
            </p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Puntuación</p>
            <p className={`text-2xl font-bold ${
              checklist.score && checklist.score >= checklist.template.passing_score
                ? 'text-green-600'
                : 'text-red-600'
            }`}>
              {checklist.score ? `${checklist.score}%` : 'N/A'}
            </p>
          </div>
        </div>

        {/* Download PDF Button */}
        {checklist.pdf_url && (
          <div className="mt-4">
            <button
              onClick={handleDownloadPDF}
              disabled={downloading}
              className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
            >
              {downloading ? (
                <>
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Descargando...
                </>
              ) : (
                <>
                  📄 Descargar PDF
                </>
              )}
            </button>
          </div>
        )}
      </div>

      {/* Items by Section */}
      <div className="p-6 space-y-6">
        {Object.entries(groupItemsBySection()).map(([section, items]) => (
          <div key={section} className="border-l-4 border-blue-500 pl-4">
            <h3 className="text-lg font-semibold text-gray-900 mb-3">{section}</h3>
            <div className="space-y-3">
              {items.map((response) => (
                <div
                  key={response.id}
                  className="bg-gray-50 rounded-lg p-4"
                >
                  <div className="flex items-start space-x-3">
                    <span className="flex-shrink-0 w-8 h-8 flex items-center justify-center bg-blue-100 text-blue-800 rounded-full text-sm font-medium">
                      {response.template_item?.order}
                    </span>
                    <div className="flex-1">
                      <p className="text-gray-900 font-medium mb-2">
                        {response.template_item?.question}
                      </p>
                      <div className="flex items-center space-x-4">
                        <div>
                          <span className="text-sm text-gray-500">Respuesta: </span>
                          {formatResponseValue(response.response_value)}
                        </div>
                      </div>
                      {response.observations && (
                        <div className="mt-2 p-2 bg-yellow-50 border border-yellow-200 rounded">
                          <p className="text-sm text-gray-700">
                            <span className="font-medium">Observaciones:</span> {response.observations}
                          </p>
                        </div>
                      )}
                      {response.photo_url && (
                        <div className="mt-2">
                          <img
                            src={response.photo_url}
                            alt="Foto de inspección"
                            className="max-w-xs rounded-lg border border-gray-300"
                          />
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>

      {/* Signature */}
      {checklist.signature_data && (
        <div className="border-t border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-3">Firma Digital</h3>
          <div className="bg-gray-50 p-4 rounded-lg inline-block">
            <img
              src={checklist.signature_data}
              alt="Firma digital"
              className="max-w-md border border-gray-300 rounded"
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default ChecklistViewer;
