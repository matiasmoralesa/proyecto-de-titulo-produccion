/**
 * Component to execute/complete checklists (mobile-optimized)
 */
import React, { useState, useEffect, useRef } from 'react';
import { ChecklistTemplate, ChecklistItemResponse, ChecklistCompletionRequest } from '../../types/checklist';
import { checklistService } from '../../services/checklistService';
import SignatureCanvas from 'react-signature-canvas';

interface ChecklistExecutorProps {
  template: ChecklistTemplate;
  assetId: string | number;
  workOrderId?: number;
  onComplete?: (checklistId: number) => void;
  onCancel?: () => void;
}

const ChecklistExecutor: React.FC<ChecklistExecutorProps> = ({
  template,
  assetId,
  workOrderId,
  onComplete,
  onCancel,
}) => {
  const [responses, setResponses] = useState<Map<number, ChecklistItemResponse>>(new Map());
  const [currentSection, setCurrentSection] = useState(0);
  const [showSignature, setShowSignature] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const signatureRef = useRef<SignatureCanvas>(null);

  const sections = getSections();
  const currentSectionName = sections[currentSection];
  const currentItems = template.items.filter((item) => item.section === currentSectionName);
  const progress = (responses.size / template.items.length) * 100;

  function getSections(): string[] {
    const sectionSet = new Set<string>();
    template.items.forEach((item) => sectionSet.add(item.section));
    return Array.from(sectionSet);
  }

  const handleResponse = (itemId: number, value: string) => {
    const item = template.items.find((i) => i.id === itemId);
    if (!item) return;

    const newResponses = new Map(responses);
    newResponses.set(itemId, {
      template_item_id: itemId,
      response_value: value,
      observations: responses.get(itemId)?.observations || '',
    });
    setResponses(newResponses);
  };

  const handleObservation = (itemId: number, observation: string) => {
    const newResponses = new Map(responses);
    const existing = newResponses.get(itemId) || {
      template_item_id: itemId,
      response_value: '',
      observations: '',
    };
    newResponses.set(itemId, { ...existing, observations: observation });
    setResponses(newResponses);
  };

  const handlePhotoUpload = (itemId: number, file: File) => {
    const newResponses = new Map(responses);
    const existing = newResponses.get(itemId) || {
      template_item_id: itemId,
      response_value: 'photo_uploaded',
      observations: '',
    };
    newResponses.set(itemId, { ...existing, photo: file });
    setResponses(newResponses);
  };

  const canProceed = () => {
    // Check if all required items in current section are answered
    return currentItems.every((item) => {
      if (!item.required) return true;
      const response = responses.get(item.id);
      return response && response.response_value;
    });
  };

  const handleNext = () => {
    if (currentSection < sections.length - 1) {
      setCurrentSection(currentSection + 1);
    } else {
      setShowSignature(true);
    }
  };

  const handlePrevious = () => {
    if (currentSection > 0) {
      setCurrentSection(currentSection - 1);
    }
  };

  const handleSubmit = async () => {
    try {
      setSubmitting(true);
      setError(null);

      // Get signature data
      let signatureData = '';
      if (signatureRef.current && !signatureRef.current.isEmpty()) {
        signatureData = signatureRef.current.toDataURL();
      }

      // Prepare completion request
      const completionData: ChecklistCompletionRequest = {
        template_id: template.id,
        asset_id: assetId,
        work_order_id: workOrderId,
        signature_data: signatureData,
        item_responses: Array.from(responses.values()),
      };

      const result = await checklistService.completeChecklist(completionData);
      
      if (onComplete) {
        onComplete(result.id);
      }
    } catch (err: any) {
      setError(err.response?.data?.message || 'Error al completar el checklist');
    } finally {
      setSubmitting(false);
    }
  };

  const clearSignature = () => {
    if (signatureRef.current) {
      signatureRef.current.clear();
    }
  };

  if (showSignature) {
    return (
      <div className="min-h-screen bg-gray-50 p-4">
        <div className="max-w-2xl mx-auto bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Firma Digital</h2>
          <p className="text-gray-600 mb-6">
            Por favor, firma en el recuadro para confirmar la inspección
          </p>

          <div className="border-2 border-gray-300 rounded-lg mb-4">
            <SignatureCanvas
              ref={signatureRef}
              canvasProps={{
                className: 'w-full h-64',
              }}
            />
          </div>

          <div className="flex space-x-3">
            <button
              onClick={clearSignature}
              className="flex-1 px-4 py-3 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
            >
              Limpiar
            </button>
            <button
              onClick={() => setShowSignature(false)}
              className="flex-1 px-4 py-3 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
            >
              Volver
            </button>
            <button
              onClick={handleSubmit}
              disabled={submitting}
              className="flex-1 px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
            >
              {submitting ? 'Enviando...' : 'Finalizar'}
            </button>
          </div>

          {error && (
            <div className="mt-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
              {error}
            </div>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="px-4 py-3">
          <div className="flex items-center justify-between mb-2">
            <h1 className="text-lg font-bold text-gray-900">{template.name}</h1>
            {onCancel && (
              <button
                onClick={onCancel}
                className="text-gray-500 hover:text-gray-700"
              >
                ✕
              </button>
            )}
          </div>
          
          {/* Progress Bar */}
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-blue-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            />
          </div>
          <p className="text-xs text-gray-500 mt-1">
            {responses.size} de {template.items.length} completados ({Math.round(progress)}%)
          </p>
        </div>
      </div>

      {/* Section Content */}
      <div className="p-4 space-y-4">
        <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded">
          <h2 className="text-lg font-semibold text-gray-900">{currentSectionName}</h2>
          <p className="text-sm text-gray-600 mt-1">
            Sección {currentSection + 1} de {sections.length}
          </p>
        </div>

        {/* Items */}
        {currentItems.map((item) => {
          const response = responses.get(item.id);
          
          return (
            <div key={item.id} className="bg-white rounded-lg shadow p-4">
              <div className="flex items-start space-x-3 mb-3">
                <span className="flex-shrink-0 w-8 h-8 flex items-center justify-center bg-blue-100 text-blue-800 rounded-full text-sm font-medium">
                  {item.order}
                </span>
                <div className="flex-1">
                  <p className="text-gray-900 font-medium">{item.question}</p>
                  {item.required && (
                    <span className="text-xs text-red-600">* Requerido</span>
                  )}
                </div>
              </div>

              {/* Response Input */}
              {item.response_type === 'yes_no_na' && (
                <div className="grid grid-cols-3 gap-2 mb-3">
                  {['yes', 'no', 'na'].map((value) => (
                    <button
                      key={value}
                      onClick={() => handleResponse(item.id, value)}
                      className={`py-3 px-4 rounded-lg font-medium transition-colors ${
                        response?.response_value === value
                          ? value === 'yes'
                            ? 'bg-green-600 text-white'
                            : value === 'no'
                            ? 'bg-red-600 text-white'
                            : 'bg-gray-600 text-white'
                          : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                      }`}
                    >
                      {value === 'yes' ? '✓ Sí' : value === 'no' ? '✗ No' : '○ N/A'}
                    </button>
                  ))}
                </div>
              )}

              {item.response_type === 'text' && (
                <input
                  type="text"
                  value={response?.response_value || ''}
                  onChange={(e) => handleResponse(item.id, e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 mb-3"
                  placeholder="Ingrese su respuesta"
                />
              )}

              {item.response_type === 'numeric' && (
                <input
                  type="number"
                  value={response?.response_value || ''}
                  onChange={(e) => handleResponse(item.id, e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 mb-3"
                  placeholder="Ingrese un valor numérico"
                />
              )}

              {item.response_type === 'photo' && (
                <div className="mb-3">
                  <input
                    type="file"
                    accept="image/*"
                    capture="environment"
                    onChange={(e) => {
                      const file = e.target.files?.[0];
                      if (file) handlePhotoUpload(item.id, file);
                    }}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                  />
                  {response?.photo && (
                    <p className="text-sm text-green-600 mt-2">✓ Foto cargada</p>
                  )}
                </div>
              )}

              {/* Observations */}
              {item.observations_allowed && (
                <textarea
                  value={response?.observations || ''}
                  onChange={(e) => handleObservation(item.id, e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Observaciones (opcional)"
                  rows={2}
                />
              )}
            </div>
          );
        })}
      </div>

      {/* Navigation */}
      <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 p-4">
        <div className="max-w-2xl mx-auto flex space-x-3">
          <button
            onClick={handlePrevious}
            disabled={currentSection === 0}
            className="flex-1 px-4 py-3 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            ← Anterior
          </button>
          <button
            onClick={handleNext}
            disabled={!canProceed()}
            className="flex-1 px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {currentSection === sections.length - 1 ? 'Firmar →' : 'Siguiente →'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChecklistExecutor;
