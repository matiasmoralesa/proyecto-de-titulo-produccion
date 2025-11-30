import React, { useState } from 'react';
import authService from '../../services/authService';

interface FirstLoginPasswordChangeProps {
  onSuccess: () => void;
}

const FirstLoginPasswordChange: React.FC<FirstLoginPasswordChangeProps> = ({ onSuccess }) => {
  const [formData, setFormData] = useState({
    old_password: '',
    new_password: '',
    new_password_confirm: '',
  });

  const [errors, setErrors] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(false);

  const validateForm = () => {
    const newErrors: Record<string, string> = {};

    if (!formData.old_password) {
      newErrors.old_password = 'La contraseña actual es requerida';
    }

    if (!formData.new_password) {
      newErrors.new_password = 'La nueva contraseña es requerida';
    } else if (formData.new_password.length < 8) {
      newErrors.new_password = 'La contraseña debe tener al menos 8 caracteres';
    }

    if (formData.new_password !== formData.new_password_confirm) {
      newErrors.new_password_confirm = 'Las contraseñas no coinciden';
    }

    if (formData.old_password === formData.new_password) {
      newErrors.new_password = 'La nueva contraseña debe ser diferente a la actual';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setLoading(true);
    try {
      await authService.changePassword({
        old_password: formData.old_password,
        new_password: formData.new_password,
        new_password_confirm: formData.new_password_confirm,
      });
      
      alert('Contraseña cambiada exitosamente');
      onSuccess();
    } catch (error: any) {
      console.error('Error changing password:', error);
      if (error.response?.data) {
        setErrors(error.response.data);
      } else {
        alert('Error al cambiar la contraseña');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
    // Clear error for this field
    if (errors[name]) {
      setErrors((prev) => {
        const newErrors = { ...prev };
        delete newErrors[name];
        return newErrors;
      });
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-8 max-w-md w-full mx-4">
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            Cambio de Contraseña Requerido
          </h2>
          <p className="text-gray-600">
            Por seguridad, debes cambiar tu contraseña antes de continuar.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Current Password */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Contraseña Actual *
            </label>
            <input
              type="password"
              name="old_password"
              value={formData.old_password}
              onChange={handleChange}
              className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                errors.old_password ? 'border-red-500' : 'border-gray-300'
              }`}
              autoFocus
            />
            {errors.old_password && (
              <p className="mt-1 text-sm text-red-600">{errors.old_password}</p>
            )}
          </div>

          {/* New Password */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Nueva Contraseña *
            </label>
            <input
              type="password"
              name="new_password"
              value={formData.new_password}
              onChange={handleChange}
              className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                errors.new_password ? 'border-red-500' : 'border-gray-300'
              }`}
              placeholder="Mínimo 8 caracteres"
            />
            {errors.new_password && (
              <p className="mt-1 text-sm text-red-600">{errors.new_password}</p>
            )}
          </div>

          {/* Confirm New Password */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Confirmar Nueva Contraseña *
            </label>
            <input
              type="password"
              name="new_password_confirm"
              value={formData.new_password_confirm}
              onChange={handleChange}
              className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                errors.new_password_confirm ? 'border-red-500' : 'border-gray-300'
              }`}
            />
            {errors.new_password_confirm && (
              <p className="mt-1 text-sm text-red-600">{errors.new_password_confirm}</p>
            )}
          </div>

          {/* Password Requirements */}
          <div className="bg-blue-50 border border-blue-200 rounded-md p-3">
            <p className="text-sm text-blue-800 font-medium mb-1">
              Requisitos de la contraseña:
            </p>
            <ul className="text-xs text-blue-700 space-y-1 list-disc list-inside">
              <li>Mínimo 8 caracteres</li>
              <li>Debe ser diferente a la contraseña actual</li>
              <li>Se recomienda usar letras, números y símbolos</li>
            </ul>
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            className="w-full px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-blue-300 font-medium"
            disabled={loading}
          >
            {loading ? 'Cambiando contraseña...' : 'Cambiar Contraseña'}
          </button>
        </form>

        <p className="mt-4 text-xs text-gray-500 text-center">
          No podrás acceder al sistema hasta que cambies tu contraseña.
        </p>
      </div>
    </div>
  );
};

export default FirstLoginPasswordChange;
