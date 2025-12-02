/**
 * Form component for creating/editing Asset Categories
 */
import React, { useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { AssetCategory } from '../../types/configuration';

interface CategoryFormProps {
  category?: AssetCategory | null;
  onSubmit: (data: Partial<AssetCategory>) => Promise<void>;
  onCancel: () => void;
  loading?: boolean;
}

interface CategoryFormData {
  code: string;
  name: string;
  description: string;
  is_active: boolean;
}

const CategoryForm: React.FC<CategoryFormProps> = ({
  category,
  onSubmit,
  onCancel,
  loading = false,
}) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<CategoryFormData>({
    defaultValues: {
      code: category?.code || '',
      name: category?.name || '',
      description: category?.description || '',
      is_active: category?.is_active ?? true,
    },
  });

  useEffect(() => {
    if (category) {
      reset({
        code: category.code,
        name: category.name,
        description: category.description,
        is_active: category.is_active,
      });
    }
  }, [category, reset]);

  const onFormSubmit = async (data: CategoryFormData) => {
    await onSubmit(data);
  };

  return (
    <form onSubmit={handleSubmit(onFormSubmit)} className="space-y-4">
      {/* Code Field */}
      <div>
        <label htmlFor="code" className="block text-sm font-medium text-gray-700 mb-1">
          Código <span className="text-red-500">*</span>
        </label>
        <input
          id="code"
          type="text"
          {...register('code', {
            required: 'El código es requerido',
            maxLength: {
              value: 50,
              message: 'El código no puede exceder 50 caracteres',
            },
            pattern: {
              value: /^[A-Z0-9_-]+$/,
              message: 'El código solo puede contener letras mayúsculas, números, guiones y guiones bajos',
            },
          })}
          className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
            errors.code ? 'border-red-500' : 'border-gray-300'
          }`}
          placeholder="Ej: CAT001"
          disabled={loading}
        />
        {errors.code && (
          <p className="mt-1 text-sm text-red-600">{errors.code.message}</p>
        )}
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
              value: 100,
              message: 'El nombre no puede exceder 100 caracteres',
            },
          })}
          className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
            errors.name ? 'border-red-500' : 'border-gray-300'
          }`}
          placeholder="Ej: Vehículos Pesados"
          disabled={loading}
        />
        {errors.name && (
          <p className="mt-1 text-sm text-red-600">{errors.name.message}</p>
        )}
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
          placeholder="Descripción de la categoría..."
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
          {loading ? 'Guardando...' : category ? 'Actualizar' : 'Crear'}
        </button>
      </div>
    </form>
  );
};

export default CategoryForm;
