/**
 * SparePartForm component - Form for creating/editing spare parts
 */
import { useState, useEffect } from 'react';
import { FaTimes } from 'react-icons/fa';
import { inventoryService } from '../../services/inventoryService';
import assetService from '../../services/assetService';
import type { SparePart, SparePartFormData } from '../../types/inventory.types';
import type { Location } from '../../types/asset.types';

interface SparePartFormProps {
  sparePart: SparePart | null;
  onClose: () => void;
  onSuccess: () => void;
}

const SparePartForm = ({ sparePart, onClose, onSuccess }: SparePartFormProps) => {
  const [formData, setFormData] = useState<SparePartFormData>({
    part_number: '',
    name: '',
    description: '',
    category: '',
    manufacturer: '',
    quantity: 0,
    min_quantity: 0,
    unit_of_measure: 'unidad',
    unit_cost: 0,
    storage_location: '',
    is_active: true,
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [locations, setLocations] = useState<Location[]>([]);
  const [loadingLocations, setLoadingLocations] = useState(true);

  useEffect(() => {
    loadLocations();
  }, []);

  useEffect(() => {
    if (sparePart) {
      setFormData({
        part_number: sparePart.part_number,
        name: sparePart.name,
        description: sparePart.description || '',
        category: sparePart.category || '',
        manufacturer: sparePart.manufacturer || '',
        quantity: sparePart.quantity,
        min_quantity: sparePart.min_quantity,
        unit_of_measure: sparePart.unit_of_measure,
        unit_cost: parseFloat(sparePart.unit_cost),
        storage_location: sparePart.storage_location || '',
        is_active: sparePart.is_active,
      });
    }
  }, [sparePart]);

  const loadLocations = async () => {
    try {
      setLoadingLocations(true);
      const data = await assetService.getLocations();
      setLocations(data);
    } catch (err) {
      console.error('Error loading locations:', err);
    } finally {
      setLoadingLocations(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      if (sparePart) {
        await inventoryService.updateSparePart(sparePart.id, formData);
      } else {
        await inventoryService.createSparePart(formData);
      }
      onSuccess();
    } catch (err: any) {
      setError(
        err.response?.data?.message ||
          err.response?.data?.part_number?.[0] ||
          'Error al guardar el repuesto'
      );
      console.error('Error saving spare part:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    const { name, value, type } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]:
        type === 'number'
          ? parseFloat(value) || 0
          : type === 'checkbox'
          ? (e.target as HTMLInputElement).checked
          : value,
    }));
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200 dark:border-gray-700">
          <h2 className="text-2xl font-bold text-gray-800 dark:text-white">
            {sparePart ? 'Editar Repuesto' : 'Nuevo Repuesto'}
          </h2>
          <button
            onClick={onClose}
            className="text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
          >
            <FaTimes size={24} />
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-6">
          {error && (
            <div className="mb-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 px-4 py-3 rounded-lg">
              {error}
            </div>
          )}

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Part Number */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Número de Parte *
              </label>
              <input
                type="text"
                name="part_number"
                value={formData.part_number}
                onChange={handleChange}
                required
                disabled={!!sparePart}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100 dark:disabled:bg-gray-700 dark:bg-gray-700 dark:text-white"
              />
            </div>

            {/* Name */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Nombre *
              </label>
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                required
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
              />
            </div>

            {/* Category */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Categoría
              </label>
              <select
                name="category"
                value={formData.category}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
              >
                <option value="">Seleccione una categoría</option>
                <option value="Filtros">Filtros</option>
                <option value="Frenos">Frenos</option>
                <option value="Lubricantes">Lubricantes</option>
                <option value="Transmisión">Transmisión</option>
                <option value="Eléctrico">Eléctrico</option>
                <option value="Neumáticos">Neumáticos</option>
                <option value="Fluidos">Fluidos</option>
                <option value="Motor">Motor</option>
                <option value="Suspensión">Suspensión</option>
                <option value="Carrocería">Carrocería</option>
                <option value="Sistema Hidráulico">Sistema Hidráulico</option>
                <option value="Herramientas">Herramientas</option>
                <option value="Seguridad">Seguridad</option>
                <option value="Limpieza">Limpieza</option>
                <option value="Otros">Otros</option>
              </select>
            </div>

            {/* Manufacturer */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Fabricante
              </label>
              <input
                type="text"
                name="manufacturer"
                value={formData.manufacturer}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
              />
            </div>

            {/* Quantity */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Cantidad *
              </label>
              <input
                type="number"
                name="quantity"
                value={formData.quantity}
                onChange={handleChange}
                required
                min="0"
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
              />
            </div>

            {/* Min Quantity */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Cantidad Mínima *
              </label>
              <input
                type="number"
                name="min_quantity"
                value={formData.min_quantity}
                onChange={handleChange}
                required
                min="0"
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
              />
            </div>

            {/* Unit of Measure */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Unidad de Medida *
              </label>
              <select
                name="unit_of_measure"
                value={formData.unit_of_measure}
                onChange={handleChange}
                required
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
              >
                <option value="unidad">Unidad</option>
                <option value="juego">Juego</option>
                <option value="litro">Litro</option>
                <option value="galón">Galón</option>
                <option value="kilogramo">Kilogramo</option>
                <option value="metro">Metro</option>
                <option value="caja">Caja</option>
              </select>
            </div>

            {/* Unit Cost */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Costo Unitario *
              </label>
              <input
                type="number"
                name="unit_cost"
                value={formData.unit_cost}
                onChange={handleChange}
                required
                min="0"
                step="0.01"
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
              />
            </div>

            {/* Storage Location */}
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Ubicación de Almacenamiento
              </label>
              {loadingLocations ? (
                <div className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700 text-gray-500 dark:text-gray-400">
                  Cargando ubicaciones...
                </div>
              ) : (
                <select
                  name="storage_location"
                  value={formData.storage_location}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                >
                  <option value="">Seleccione una ubicación</option>
                  {locations.map((location) => (
                    <option key={location.id} value={location.name}>
                      {location.name}
                      {location.city && ` - ${location.city}`}
                    </option>
                  ))}
                  <option value="Bodega Principal">Bodega Principal</option>
                  <option value="Bodega Eléctrica">Bodega Eléctrica</option>
                  <option value="Bodega de Neumáticos">Bodega de Neumáticos</option>
                  <option value="Estante A-1">Estante A-1</option>
                  <option value="Estante A-2">Estante A-2</option>
                  <option value="Estante A-3">Estante A-3</option>
                  <option value="Estante B-1">Estante B-1</option>
                  <option value="Estante B-2">Estante B-2</option>
                  <option value="Estante B-3">Estante B-3</option>
                  <option value="Estante C-1">Estante C-1</option>
                  <option value="Estante C-2">Estante C-2</option>
                </select>
              )}
              <p className="mt-1 text-xs text-gray-500">
                Seleccione la ubicación física donde se almacena el repuesto
              </p>
            </div>

            {/* Description */}
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Descripción
              </label>
              <textarea
                name="description"
                value={formData.description}
                onChange={handleChange}
                rows={3}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
              />
            </div>

            {/* Is Active */}
            <div className="md:col-span-2">
              <label className="flex items-center gap-2">
                <input
                  type="checkbox"
                  name="is_active"
                  checked={formData.is_active}
                  onChange={handleChange}
                  className="w-4 h-4 text-blue-600 rounded focus:ring-2 focus:ring-blue-500"
                />
                <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Activo</span>
              </label>
            </div>
          </div>

          {/* Actions */}
          <div className="flex justify-end gap-3 mt-6">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
            >
              Cancelar
            </button>
            <button
              type="submit"
              disabled={loading}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Guardando...' : sparePart ? 'Actualizar' : 'Crear'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default SparePartForm;
