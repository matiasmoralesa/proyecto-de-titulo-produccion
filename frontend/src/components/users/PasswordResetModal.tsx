import React, { useState } from 'react';
import { User, ResetPasswordData } from '../../services/userManagementService';

interface PasswordResetModalProps {
  user: User;
  onSubmit: (data: ResetPasswordData) => Promise<void>;
  onClose: () => void;
}

const PasswordResetModal: React.FC<PasswordResetModalProps> = ({ user, onSubmit, onClose }) => {
  const [formData, setFormData] = useState({
    new_password: '',
    new_password_confirm: '',
  });

  const [errors, setErrors] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(false);

  const validateForm = () => {
    const newErrors: Record<string, string> = {};

    if (!formData.new_password) {
      newErrors.new_password = 'La contraseña es requerida';
    } else if (formData.new_password.length < 8) {
      newErrors.new_password = 'La contraseña debe tener al menos 8 caracteres';
    }

    if (formData.new_password !== formData.new_password_confirm) {
      newErrors.new_password_confirm = 'Las contraseñas no coinciden';
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
      await onSubmit(formData);
      onClose();
    } catch (error: any) {
      console.error('Error resetting password:', error);
      if (error.response?.data) {
        setErrors(error.response.data);
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
      <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
        <h2 className="text-xl font-bold mb-4">Resetear Contraseña</h2>
        
        <div className="mb-4 p-3 bg-blue-50 border border-blue-200 rounded-md">
          <p className="text-sm text-blue-800">
            Resetear contraseña para: <strong>{user.username}</strong>
          </p>
          <p className="text-xs text-blue-600 mt-1">
            El usuario deberá cambiar su contraseña en el próximo inicio de sesión.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
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

          {/* Confirm Password */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Confirmar Contraseña *
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

          {/* Form Actions */}
          <div className="flex justify-end space-x-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
              disabled={loading}
            >
              Cancelar
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700 disabled:bg-purple-300"
              disabled={loading}
            >
              {loading ? 'Reseteando...' : 'Resetear Contraseña'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default PasswordResetModal;
