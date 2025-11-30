/**
 * StockAdjustmentModal component - Modal for adjusting stock quantities
 */
import { useState } from 'react';
import { FaTimes } from 'react-icons/fa';
import { inventoryService } from '../../services/inventoryService';
import type { SparePart, StockAdjustment } from '../../types/inventory.types';
import { MOVEMENT_TYPES } from '../../types/inventory.types';

interface StockAdjustmentModalProps {
  sparePart: SparePart;
  onClose: () => void;
  onSuccess: () => void;
}

const StockAdjustmentModal = ({
  sparePart,
  onClose,
  onSuccess,
}: StockAdjustmentModalProps) => {
  const [formData, setFormData] = useState<StockAdjustment>({
    quantity_change: 0,
    movement_type: 'IN',
    notes: '',
    reference_type: '',
    reference_id: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      await inventoryService.adjustStock(sparePart.id, formData);
      onSuccess();
    } catch (err: any) {
      setError(
        err.response?.data?.error ||
          err.response?.data?.message ||
          'Error al ajustar el stock'
      );
      console.error('Error adjusting stock:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: name === 'quantity_change' ? parseInt(value) || 0 : value,
    }));
  };

  const newQuantity = sparePart.quantity + formData.quantity_change;
  const isValidAdjustment = newQuantity >= 0;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-lg w-full">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <div>
            <h2 className="text-2xl font-bold text-gray-800">Ajustar Stock</h2>
            <p className="text-sm text-gray-600 mt-1">
              {sparePart.part_number} - {sparePart.name}
            </p>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <FaTimes size={24} />
          </button>
        </div>

        {/* Current Stock Info */}
        <div className="p-6 bg-gray-50 border-b border-gray-200">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-sm text-gray-600">Stock Actual</p>
              <p className="text-2xl font-bold text-gray-800">
                {sparePart.quantity} {sparePart.unit_of_measure}
              </p>
            </div>
            <div>
              <p className="text-sm text-gray-600">
                Nuevo Stock
                {formData.quantity_change !== 0 && (
                  <span
                    className={`ml-2 text-xs font-medium ${
                      formData.quantity_change > 0 ? 'text-green-600' : 'text-red-600'
                    }`}
                  >
                    ({formData.quantity_change > 0 ? '+' : ''}
                    {formData.quantity_change})
                  </span>
                )}
              </p>
              <p
                className={`text-2xl font-bold ${
                  formData.quantity_change === 0
                    ? 'text-gray-400'
                    : isValidAdjustment
                    ? newQuantity <= sparePart.min_quantity
                      ? 'text-yellow-600'
                      : 'text-green-600'
                    : 'text-red-600'
                }`}
              >
                {newQuantity} {sparePart.unit_of_measure}
              </p>
              {formData.quantity_change === 0 && (
                <p className="text-xs text-gray-500 mt-1">Sin cambios</p>
              )}
            </div>
          </div>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-6">
          {error && (
            <div className="mb-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
              {error}
            </div>
          )}

          {!isValidAdjustment && (
            <div className="mb-4 bg-yellow-50 border border-yellow-200 text-yellow-700 px-4 py-3 rounded-lg">
              ⚠️ El ajuste resultaría en stock negativo
            </div>
          )}

          <div className="space-y-4">
            {/* Movement Type */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Tipo de Movimiento *
              </label>
              <select
                name="movement_type"
                value={formData.movement_type}
                onChange={handleChange}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                {Object.entries(MOVEMENT_TYPES).map(([key, label]) => (
                  <option key={key} value={key}>
                    {label}
                  </option>
                ))}
              </select>
            </div>

            {/* Quantity Change */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Cantidad a Ajustar *
              </label>
              <div className="relative">
                <input
                  type="number"
                  name="quantity_change"
                  value={formData.quantity_change === 0 ? '' : formData.quantity_change}
                  onChange={handleChange}
                  required
                  placeholder="Ej: +10 para entrada, -5 para salida"
                  className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                    formData.quantity_change === 0
                      ? 'border-gray-300'
                      : formData.quantity_change > 0
                      ? 'border-green-300 bg-green-50'
                      : 'border-red-300 bg-red-50'
                  }`}
                />
                {formData.quantity_change !== 0 && (
                  <div className="absolute right-3 top-2.5">
                    <span
                      className={`text-sm font-medium ${
                        formData.quantity_change > 0 ? 'text-green-600' : 'text-red-600'
                      }`}
                    >
                      {formData.quantity_change > 0 ? '↑' : '↓'}
                    </span>
                  </div>
                )}
              </div>
              
              {/* Quick adjustment buttons */}
              <div className="mt-2 flex gap-2">
                <div className="flex gap-1">
                  <button
                    type="button"
                    onClick={() =>
                      setFormData((prev) => ({ ...prev, quantity_change: prev.quantity_change + 1 }))
                    }
                    className="px-2 py-1 text-xs bg-green-100 text-green-700 rounded hover:bg-green-200"
                  >
                    +1
                  </button>
                  <button
                    type="button"
                    onClick={() =>
                      setFormData((prev) => ({ ...prev, quantity_change: prev.quantity_change + 5 }))
                    }
                    className="px-2 py-1 text-xs bg-green-100 text-green-700 rounded hover:bg-green-200"
                  >
                    +5
                  </button>
                  <button
                    type="button"
                    onClick={() =>
                      setFormData((prev) => ({ ...prev, quantity_change: prev.quantity_change + 10 }))
                    }
                    className="px-2 py-1 text-xs bg-green-100 text-green-700 rounded hover:bg-green-200"
                  >
                    +10
                  </button>
                </div>
                <div className="flex gap-1">
                  <button
                    type="button"
                    onClick={() =>
                      setFormData((prev) => ({ ...prev, quantity_change: prev.quantity_change - 1 }))
                    }
                    className="px-2 py-1 text-xs bg-red-100 text-red-700 rounded hover:bg-red-200"
                  >
                    -1
                  </button>
                  <button
                    type="button"
                    onClick={() =>
                      setFormData((prev) => ({ ...prev, quantity_change: prev.quantity_change - 5 }))
                    }
                    className="px-2 py-1 text-xs bg-red-100 text-red-700 rounded hover:bg-red-200"
                  >
                    -5
                  </button>
                  <button
                    type="button"
                    onClick={() =>
                      setFormData((prev) => ({ ...prev, quantity_change: prev.quantity_change - 10 }))
                    }
                    className="px-2 py-1 text-xs bg-red-100 text-red-700 rounded hover:bg-red-200"
                  >
                    -10
                  </button>
                </div>
              </div>
              
              <p className="mt-1 text-xs text-gray-500">
                Ingrese un número positivo para entrada (+) o negativo para salida (-)
              </p>
            </div>

            {/* Reference Type */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Tipo de Referencia
              </label>
              <input
                type="text"
                name="reference_type"
                value={formData.reference_type}
                onChange={handleChange}
                placeholder="ej: work_order, purchase_order"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            {/* Reference ID */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                ID de Referencia
              </label>
              <input
                type="text"
                name="reference_id"
                value={formData.reference_id}
                onChange={handleChange}
                placeholder="ej: WO-123, PO-456"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            {/* Notes */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Notas
              </label>
              <textarea
                name="notes"
                value={formData.notes}
                onChange={handleChange}
                rows={3}
                placeholder="Motivo del ajuste..."
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>

          {/* Actions */}
          <div className="flex justify-end gap-3 mt-6">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
            >
              Cancelar
            </button>
            <button
              type="submit"
              disabled={loading || !isValidAdjustment || formData.quantity_change === 0}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Ajustando...' : 'Ajustar Stock'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default StockAdjustmentModal;
