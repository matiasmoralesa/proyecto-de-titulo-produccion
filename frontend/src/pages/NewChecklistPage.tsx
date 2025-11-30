/**
 * Page to start a new checklist
 */
import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { ChecklistTemplate } from '../types/checklist';
import { checklistService } from '../services/checklistService';
import assetService from '../services/assetService';
import MainLayout from '../components/layout/MainLayout';
import ChecklistExecutor from '../components/checklists/ChecklistExecutor';

interface Asset {
  id: string;
  name: string;
  license_plate: string;
  vehicle_type: string;
}

const NewChecklistPage: React.FC = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  
  const [step, setStep] = useState<'select' | 'execute'>('select');
  const [assets, setAssets] = useState<Asset[]>([]);
  const [templates, setTemplates] = useState<ChecklistTemplate[]>([]);
  const [selectedAsset, setSelectedAsset] = useState<Asset | null>(null);
  const [selectedTemplate, setSelectedTemplate] = useState<ChecklistTemplate | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadData();
  }, []);

  useEffect(() => {
    // Pre-select asset from URL params
    const assetId = searchParams.get('asset_id');
    if (assetId && assets.length > 0) {
      const asset = assets.find(a => a.id === Number(assetId));
      if (asset) {
        setSelectedAsset(asset);
        loadTemplatesForAsset(asset);
      }
    }
  }, [searchParams, assets]);

  const loadData = async () => {
    try {
      setLoading(true);
      const [assetsResponse, templatesData] = await Promise.all([
        assetService.getAssets(),
        checklistService.getTemplates(),
      ]);
      setAssets(assetsResponse.results || []);
      setTemplates(templatesData);
    } catch (err: any) {
      setError(err.message || 'Error al cargar datos');
    } finally {
      setLoading(false);
    }
  };

  const loadTemplatesForAsset = async (asset: Asset) => {
    try {
      console.log('Loading templates for vehicle type:', asset.vehicle_type);
      const templatesData = await checklistService.getTemplatesByVehicleType(asset.vehicle_type);
      console.log('Templates loaded:', templatesData);
      setTemplates(templatesData);
      
      // Auto-select template if only one available
      if (templatesData.length === 1) {
        setSelectedTemplate(templatesData[0]);
      } else if (templatesData.length === 0) {
        setError(`No hay plantillas disponibles para el tipo de vehículo: ${asset.vehicle_type}`);
      }
    } catch (err: any) {
      console.error('Error loading templates:', err);
      setError(err.message || 'Error al cargar plantillas');
    }
  };

  const handleAssetChange = (assetId: string) => {
    const asset = assets.find(a => a.id === assetId);
    if (asset) {
      setSelectedAsset(asset);
      setSelectedTemplate(null);
      setError(null); // Clear any previous errors
      loadTemplatesForAsset(asset);
    }
  };

  const handleStart = () => {
    if (selectedAsset && selectedTemplate) {
      setStep('execute');
    }
  };

  const handleComplete = (checklistId: number) => {
    navigate(`/checklists?view=${checklistId}`);
  };

  const handleCancel = () => {
    if (step === 'execute') {
      setStep('select');
    } else {
      navigate('/checklists');
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (step === 'execute' && selectedAsset && selectedTemplate) {
    return (
      <ChecklistExecutor
        template={selectedTemplate}
        assetId={selectedAsset.id}
        onComplete={handleComplete}
        onCancel={handleCancel}
      />
    );
  }

  return (
    <MainLayout>
      <div className="container mx-auto px-4 py-8 max-w-4xl">
      <div className="mb-8">
        <button
          onClick={() => navigate('/checklists')}
          className="text-blue-600 hover:text-blue-800 mb-4 flex items-center"
        >
          ← Volver a Checklists
        </button>
        <h1 className="text-3xl font-bold text-gray-900">Nuevo Checklist</h1>
        <p className="text-gray-600 mt-2">
          Selecciona un activo y una plantilla para comenzar la inspección
        </p>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-6">
          {error}
        </div>
      )}

      <div className="bg-white rounded-lg shadow-lg p-6 space-y-6">
        {/* Step 1: Select Asset */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            1. Seleccionar Activo *
          </label>
          <select
            value={selectedAsset?.id || ''}
            onChange={(e) => handleAssetChange(e.target.value)}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">-- Seleccione un activo --</option>
            {assets.map((asset) => (
              <option key={asset.id} value={asset.id}>
                {asset.name} - {asset.license_plate}
              </option>
            ))}
          </select>
          {selectedAsset && (
            <p className="mt-2 text-sm text-gray-600">
              Tipo: {selectedAsset.vehicle_type}
            </p>
          )}
        </div>

        {/* Step 2: Select Template */}
        {selectedAsset && (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              2. Seleccionar Plantilla de Checklist *
            </label>
            {templates.length === 0 ? (
              <div className="bg-yellow-50 border border-yellow-200 text-yellow-700 px-4 py-3 rounded">
                No hay plantillas disponibles para este tipo de vehículo
              </div>
            ) : (
              <div className="space-y-3">
                {templates.map((template) => (
                  <div
                    key={template.id}
                    onClick={() => setSelectedTemplate(template)}
                    className={`p-4 border-2 rounded-lg cursor-pointer transition-all ${
                      selectedTemplate?.id === template.id
                        ? 'border-blue-500 bg-blue-50'
                        : 'border-gray-200 hover:border-blue-300'
                    }`}
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <h3 className="font-semibold text-gray-900">{template.name}</h3>
                        <p className="text-sm text-gray-600 mt-1">Código: {template.code}</p>
                        {template.description && (
                          <p className="text-sm text-gray-600 mt-2">{template.description}</p>
                        )}
                        <div className="flex items-center space-x-4 mt-3 text-sm text-gray-500">
                          <span>📋 {template.total_items} items</span>
                          <span>✓ {template.required_items_count} requeridos</span>
                          <span>🎯 {template.passing_score}% mínimo</span>
                        </div>
                      </div>
                      {selectedTemplate?.id === template.id && (
                        <div className="ml-4">
                          <div className="w-6 h-6 bg-blue-600 rounded-full flex items-center justify-center">
                            <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                              <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                            </svg>
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex space-x-4 pt-6 border-t border-gray-200">
          <button
            onClick={handleCancel}
            className="flex-1 px-6 py-3 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
          >
            Cancelar
          </button>
          <button
            onClick={handleStart}
            disabled={!selectedAsset || !selectedTemplate}
            className="flex-1 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            Iniciar Checklist →
          </button>
        </div>
      </div>

      {/* Info Box */}
      <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h4 className="font-semibold text-blue-900 mb-2">💡 Información</h4>
        <ul className="text-sm text-blue-800 space-y-1">
          <li>• Selecciona el activo que vas a inspeccionar</li>
          <li>• El sistema mostrará solo las plantillas compatibles con el tipo de vehículo</li>
          <li>• Podrás completar el checklist sección por sección</li>
          <li>• Al finalizar, se generará automáticamente un PDF con los resultados</li>
        </ul>
      </div>
      </div>
    </MainLayout>
  );
};

export default NewChecklistPage;
