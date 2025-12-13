/**
 * Form component for editing System Parameters
 */
import React, { useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { SystemParameter } from '../../types/configuration';

interface ParameterFormProps {
  parameter: SystemParameter;
  onSubmit: (data: Partial<SystemParameter>) => Promise<void>;
  onCancel: () => void;
  loading?: boolean;
}

interface ParameterFormData {
  value: string;
  description: string;
}

const ParameterForm: React.FC<ParameterFormProps> = ({
  parameter,
  onSubmit,
  onCancel,
  loading = false,
}) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<ParameterFormData>({
    defaultValues: {
      value: parameter.value,
      description: parameter.description,
    },
  });

  useEffect(() => {
    reset({
      value: parameter.value,
      description: parameter.description,
    });
  }, [parameter, reset]);

  const onFormSubmit = async (data: ParameterFormData) => {
    await onSubmit(data);
  };

  const getInputType = () => {
    switch (parameter.data_type) {
      case 'integer':
      case 'float':
        return 'number';
      case 'boolean':
        return 'checkbox';
      default:
        return 'text';
    }
  };

  const getValidationRules = () => {
    const rules: any = {
      required: 'El valor es requerido',
    };

    if (parameter.data_type === 'integer') {
      rules.pattern = {
        value: /^-?\d+$/,
        message: 'Debe ser un número entero',
      };
    } else if (parameter.data_type === 'float') {
      rules.pattern = {
        value: /^-?\d+(\.\d+)?$/,
        message: 'Debe ser un número decimal',
      };
    }

    return rules;
  };

  if (!parameter.is_editable) {
    return (
      <div className="space-y-4">
        <div className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-4">
          <p className="text-sm text-yellow-800 dark:text-yellow-400">
            Este parámetro no es editable por razones de seguridad del sistema.
          </p>
        </div>

        {/* Read-only display */}
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            Clave
          </label>
          <input
            type="text"
            value={parameter.key}
            disabled
            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700 dark:text-gray-400"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            Valor
          </label>
          <input
            type="text"
            value={parameter.value}
            disabled
            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700 dark:text-gray-400"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            Tipo de Dato
          </label>
          <input
            type="text"
            value={parameter.data_type}
            disabled
            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700 dark:text-gray-400"
          />
        </div>

        <div className="flex justify-end">
          <button
            type="button"
            onClick={onCancel}
            className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
          >
            Cerrar
          </button>
        </div>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit(onFormSubmit)} className="space-y-4">
      {/* Key Field (Read-only) */}
      <div>
        <label htmlFor="key" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
          Clave
        </label>
        <input
          id="key"
          type="text"
          value={parameter.key}
          disabled
          className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700 dark:text-gray-400"
        />
      </div>

      {/* Data Type (Read-only) */}
      <div>
        <label htmlFor="data_type" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
          Tipo de Dato
        </label>
        <input
          id="data_type"
          type="text"
          value={parameter.data_type}
          disabled
          className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700 dark:text-gray-400"
        />
      </div>

      {/* Value Field */}
      <div>
        <label htmlFor="value" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
          Valor <span className="text-red-500">*</span>
        </label>
        {parameter.data_type === 'boolean' ? (
          <select
            id="value"
            {...register('value', getValidationRules())}
            className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white dark:border-gray-600 ${
              errors.value ? 'border-red-500 dark:border-red-500' : 'border-gray-300 dark:border-gray-600'
            }`}
            disabled={loading}
          >
            <option value="true">Verdadero</option>
            <option value="false">Falso</option>
          </select>
        ) : parameter.data_type === 'json' ? (
          <textarea
            id="value"
            {...register('value', getValidationRules())}
            rows={5}
            className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent font-mono text-sm dark:bg-gray-700 dark:text-white dark:border-gray-600 ${
              errors.value ? 'border-red-500 dark:border-red-500' : 'border-gray-300 dark:border-gray-600'
            }`}
            placeholder='{"key": "value"}'
            disabled={loading}
          />
        ) : (
          <input
            id="value"
            type={getInputType()}
            {...register('value', getValidationRules())}
            className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white dark:border-gray-600 ${
              errors.value ? 'border-red-500 dark:border-red-500' : 'border-gray-300 dark:border-gray-600'
            }`}
            disabled={loading}
          />
        )}
        {errors.value && (
          <p className="mt-1 text-sm text-red-600 dark:text-red-400">{errors.value.message}</p>
        )}
      </div>

      {/* Description Field */}
      <div>
        <label htmlFor="description" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
          Descripción
        </label>
        <textarea
          id="description"
          {...register('description')}
          rows={3}
          className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
          placeholder="Descripción del parámetro..."
          disabled={loading}
        />
      </div>

      {/* Form Actions */}
      <div className="flex justify-end space-x-3 pt-4">
        <button
          type="button"
          onClick={onCancel}
          className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
          disabled={loading}
        >
          Cancelar
        </button>
        <button
          type="submit"
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          disabled={loading}
        >
          {loading ? 'Guardando...' : 'Actualizar'}
        </button>
      </div>
    </form>
  );
};

export default ParameterForm;
