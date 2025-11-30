/**
 * Main page for Checklists management
 */
import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { ChecklistTemplate, ChecklistResponse } from '../types/checklist';
import { checklistService } from '../services/checklistService';
import MainLayout from '../components/layout/MainLayout';
import ChecklistTemplateViewer from '../components/checklists/ChecklistTemplateViewer';
import ChecklistViewer from '../components/checklists/ChecklistViewer';

const ChecklistsPage: React.FC = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [activeTab, setActiveTab] = useState<'templates' | 'responses'>('templates');
  const [responses, setResponses] = useState<ChecklistResponse[]>([]);
  const [selectedChecklistId, setSelectedChecklistId] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (activeTab === 'responses') {
      loadResponses();
    }
  }, [activeTab]);

  useEffect(() => {
    // Check if we should view a specific checklist from URL
    const viewId = searchParams.get('view');
    if (viewId) {
      setSelectedChecklistId(Number(viewId));
      setActiveTab('responses');
    }
  }, [searchParams]);

  const loadResponses = async () => {
    try {
      setLoading(true);
      const data = await checklistService.getResponses();
      setResponses(data);
    } catch (err) {
      console.error('Error loading responses:', err);
    } finally {
      setLoading(false);
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

  if (selectedChecklistId) {
    return (
      <MainLayout>
        <div className="container mx-auto px-4 py-8">
          <ChecklistViewer
            checklistId={selectedChecklistId}
            onClose={() => setSelectedChecklistId(null)}
          />
        </div>
      </MainLayout>
    );
  }

  return (
    <MainLayout>
      <div className="container mx-auto px-4 py-8">
      <div className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Checklists</h1>
          <p className="text-gray-600 mt-2">
            Gestiona las plantillas y respuestas de checklists de inspección
          </p>
        </div>
        <button
          onClick={() => navigate('/checklists/new')}
          className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center space-x-2"
        >
          <span>+</span>
          <span>Nuevo Checklist</span>
        </button>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200 mb-6">
        <nav className="-mb-px flex space-x-8">
          <button
            onClick={() => setActiveTab('templates')}
            className={`py-4 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'templates'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            📋 Plantillas
          </button>
          <button
            onClick={() => setActiveTab('responses')}
            className={`py-4 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'responses'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            📝 Respuestas
          </button>
        </nav>
      </div>

      {/* Content */}
      {activeTab === 'templates' && (
        <ChecklistTemplateViewer />
      )}

      {activeTab === 'responses' && (
        <div className="space-y-4">
          {loading ? (
            <div className="flex justify-center items-center p-8">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            </div>
          ) : responses.length === 0 ? (
            <div className="bg-white rounded-lg shadow p-8 text-center">
              <p className="text-gray-500">No hay checklists completados</p>
            </div>
          ) : (
            <div className="grid gap-4">
              {responses.map((response) => (
                <div
                  key={response.id}
                  className="bg-white rounded-lg shadow hover:shadow-md transition-shadow"
                >
                  <div className="p-6">
                    <div className="flex items-start justify-between mb-4">
                      <div 
                        className="flex-1 cursor-pointer"
                        onClick={() => setSelectedChecklistId(response.id)}
                      >
                        <h3 className="text-lg font-semibold text-gray-900">
                          {response.template.name}
                        </h3>
                        <p className="text-sm text-gray-500">
                          Código: {response.template.code}
                        </p>
                      </div>
                      <div className="flex items-center space-x-2">
                        <button
                          onClick={async (e) => {
                            e.stopPropagation();
                            try {
                              const blob = await checklistService.downloadPDF(response.id);
                              const url = window.URL.createObjectURL(blob);
                              const a = document.createElement('a');
                              a.href = url;
                              a.download = `checklist-${response.template.code}-${response.asset.name}-${new Date(response.completed_at || '').toLocaleDateString('es-ES')}.pdf`;
                              document.body.appendChild(a);
                              a.click();
                              window.URL.revokeObjectURL(url);
                              document.body.removeChild(a);
                            } catch (error) {
                              console.error('Error downloading PDF:', error);
                              alert('Error al descargar el PDF');
                            }
                          }}
                          className="px-3 py-1 bg-green-600 text-white rounded hover:bg-green-700 transition-colors text-sm flex items-center space-x-1"
                          title="Descargar PDF"
                        >
                          <span>📄</span>
                          <span>PDF</span>
                        </button>
                        <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(response.status)}`}>
                          {getStatusText(response.status)}
                        </span>
                      </div>
                    </div>

                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                      <div>
                        <p className="text-gray-500">Activo</p>
                        <p className="font-medium text-gray-900">{response.asset.name}</p>
                      </div>
                      <div>
                        <p className="text-gray-500">Completado Por</p>
                        <p className="font-medium text-gray-900">
                          {response.completed_by_name || 'N/A'}
                        </p>
                      </div>
                      <div>
                        <p className="text-gray-500">Fecha</p>
                        <p className="font-medium text-gray-900">
                          {response.completed_at
                            ? new Date(response.completed_at).toLocaleDateString('es-ES')
                            : 'N/A'}
                        </p>
                      </div>
                      <div>
                        <p className="text-gray-500">Puntuación</p>
                        <p className={`text-lg font-bold ${
                          response.score && response.score >= response.template.passing_score
                            ? 'text-green-600'
                            : 'text-red-600'
                        }`}>
                          {response.score ? `${response.score}%` : 'N/A'}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
      </div>
    </MainLayout>
  );
};

export default ChecklistsPage;
