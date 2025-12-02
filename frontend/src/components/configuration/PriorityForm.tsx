/**
 * Form component for creating/editing Priorities
 */
import React, { useEffect, useState } from 'react';
import { useForm } from 'react-hook-form';
import { Priority } from '../../types/configuration';

interface PriorityFormProps {
  priority?: Priority | null;
  onSubmit: (data: Partial<Priority>) => Promise<void>;
  onCancel: () => void;
  loading?: boolean;
}

interface PriorityFormData {
  level: number;
  name: string;
  description: string;
  color_code: string;
  is_active: boolean;
}

const PriorityForm: React.FC<PriorityFormProps> = ({
  priority,
  onSubmit,
  onCancel,
  loading = false,
}) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
    watch,
    setValue,
  } = useForm<PriorityFormData>({
    defaultValues: {
      level: priority?.level || 1,
      name: priority?.name || '',
      description: priority?.description || '',
      color_code: priority?.color_code || '#000000',
      is_active: priority?.is_active ?? true,
    },
  });

  const colorCode = watch('color_code');

  useEffect(() => {
    if (priority) {
      reset({
        level: priority.level,
        name: priority.name,
        description: priority.description,
        color_code: priority.color_code,
        is_active: priority.is_active,
      });
    }
  }, [priority, reset]);

  const onFormSubmit = async (data: PriorityFormData) => {
    await onSubmit(data);
  };

  const presetColors = [
    '#EF4444', // Red
    '#F59E0B', // Orange
    '#EAB308', // Yellow
    '#10B981', // Green
    '#3B82F6', // Blue
    '#8B5CF6', // Purple
    '#EC4899', // Pink
    '#6B7280', // Gray
  ];

  return (
    <form onSubmit={handleSubmit(onFormSubmit)} className="space-y-4">
      {/* Level Field */}
      <div>
        <label htmlFor="level" className="block text-sm font-medium text-gray-700 mb-1">
          Nivel <span className="text-red-500">*</span>
        </label>
        <input
          id="level"
          type="number"
          {...register('level', {
            required: 'El nivel es requerido',
            min: {
              value: 1,
              message: 'El nivel debe ser al menos 1',
            },
            max: {
              value: 10,
              message: 'El nivel no puede exceder 10',
            },
            valueAsNumber: true,
          })}
          className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
            errors.level ? 'border-red-500' : 'border-gray-300'
          }`}
          placeholder="1-10"
          disabled={loading}
        />
        {errors.level && (
          <p className="mt-1 text-sm text-red-600">{errors.level.message}</p>
        )}
        <p className="mt-1 text-xs text-gray-500">1 = Más alta, 10 = Más baja</p>
      </div>

      {/* Name Field */}
      <div>
        <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">
          Nombre <span className="text-red-500">*</span>
        </label>
        <input
          id="name"
          type="text"
          {...register('name', {
            required: 'El nombre es requerido',
            maxLength: {
              value: 50,
              message: 'El nombre no puede exceder 50 caracteres',
            },
          })}
          className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
            errors.name ? 'border-red-500' : 'border-gray-300'
          }`}
          placeholder="Ej: Urgente"
          disabled={loading}
        />
        {errors.name && (
          <p className="mt-1 text-sm text-red-600">{errors.name.message}</p>
        )}
      </div>

      {/* Color Code Field */}
      <div>
        <label htmlFor="color_code" className="block text-sm font-medium text-gray-700 mb-1">
          Color <span className="text-red-500">*</span>
        </label>
        <div className="flex items-center space-x-3">
          <input
            id="color_code"
            type="text"
            {...register('color_code', {
              required: 'El código de color es requerido',
              pattern: {
                value: /^#[0-9A-Fa-f]{6}$/,
                message: 'El código de color debe estar en formato hexadecimal (#RRGGBB)',
              },
            })}
            className={`flex-1 px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
              errors.color_code ? 'border-red-500' : 'border-gray-300'
            }`}
            placeholder="#000000"
            disabled={loading}
          />
          <div
            className="w-12 h-10 rounded-lg border-2 border-gray-300"
            style={{ backgroundColor: colorCode }}
          />
        </div>
        {errors.color_code && (
          <p className="mt-1 text-sm text-red-600">{errors.color_code.message}</p>
        )}
        
        {/* Preset Colors */}
        <div className="mt-2">
          <p className="text-xs text-gray-500 mb-2">Colores predefinidos:</p>
          <div className="flex flex-wrap gap-2">
            {presetColors.map((color) => (
              <button
                key={color}
                type="button"
                onClick={() => setValue('color_code', color)}
                className="w-8 h-8 rounded border-2 border-gray-300 hover:border-blue-500 transition-colors"
                style={{ backgroundColor: color }}
                disabled={loading}
                title={color}
              />
            ))}
          </div>
        </div>
      </div>

      {/* Description Field */}
      <div>
        <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
          Descripción
        </label>
        <textarea
          id="description"
          {...register('description')}
          rows={3}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="Descripción de la prioridad..."
          disabled={loading}
        />
      </div>

      {/* Active Status */}
      <div className="flex items-center">
        <input
          id="is_active"
          type="checkbox"
          {...register('is_active')}
          className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
          disabled={loading}
        />
        <label htmlFor="is_active" className="ml-2 block text-sm text-gray-700">
          Activo
        </label>
      </div>

      {/* Form Actions */}
      <div className="flex justify-end space-x-3 pt-4">
        <button
          type="button"
          onClick={onCancel}
          className="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
          disabled={loading}
        >
          Cancelar
        </button>
        <button
          type="submit"
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          disabled={loading}
        >
          {loading ? 'Guardando...' : priority ? 'Actualizar' : 'Crear'}
        </button>
      </div>
    </form>
  );
};

export default PriorityForm;
