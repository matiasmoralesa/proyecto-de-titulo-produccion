import React, { useState } from 'react';
import MainLayout from '../components/layout/MainLayout';
import UserList from '../components/users/UserList';
import UserForm from '../components/users/UserForm';
import PasswordResetModal from '../components/users/PasswordResetModal';
import userManagementService, {
  User,
  CreateUserData,
  UpdateUserData,
  ResetPasswordData,
} from '../services/userManagementService';

const UsersPage: React.FC = () => {
  const [showForm, setShowForm] = useState(false);
  const [selectedUser, setSelectedUser] = useState<User | null>(null);
  const [showPasswordReset, setShowPasswordReset] = useState(false);
  const [userForPasswordReset, setUserForPasswordReset] = useState<User | null>(null);
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleCreateUser = () => {
    setSelectedUser(null);
    setShowForm(true);
  };

  const handleEditUser = (user: User) => {
    setSelectedUser(user);
    setShowForm(true);
  };

  const handleResetPassword = (user: User) => {
    setUserForPasswordReset(user);
    setShowPasswordReset(true);
  };

  const handleSubmitUser = async (data: CreateUserData | UpdateUserData) => {
    try {
      if (selectedUser) {
        // Update existing user
        await userManagementService.updateUser(selectedUser.id, data as UpdateUserData);
        alert('Usuario actualizado exitosamente');
      } else {
        // Create new user
        await userManagementService.createUser(data as CreateUserData);
        alert('Usuario creado exitosamente');
      }
      setShowForm(false);
      setSelectedUser(null);
      setRefreshTrigger((prev) => prev + 1);
    } catch (error: any) {
      console.error('Error submitting user:', error);
      if (error.response?.data) {
        // Let the form handle the errors
        throw error;
      } else {
        alert('Error al guardar el usuario');
      }
    }
  };

  const handleSubmitPasswordReset = async (data: ResetPasswordData) => {
    if (!userForPasswordReset) return;

    try {
      await userManagementService.resetPassword(userForPasswordReset.id, data);
      alert('Contraseña reseteada exitosamente. El usuario deberá cambiarla en el próximo inicio de sesión.');
      setShowPasswordReset(false);
      setUserForPasswordReset(null);
    } catch (error: any) {
      console.error('Error resetting password:', error);
      alert('Error al resetear la contraseña');
      throw error;
    }
  };

  const handleCancelForm = () => {
    setShowForm(false);
    setSelectedUser(null);
  };

  const handleClosePasswordReset = () => {
    setShowPasswordReset(false);
    setUserForPasswordReset(null);
  };

  return (
    <MainLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Gestión de Usuarios</h1>
            <p className="text-gray-600 dark:text-gray-400 mt-1">
              Administra los usuarios del sistema y sus permisos
            </p>
          </div>
          {!showForm && (
            <button
              onClick={handleCreateUser}
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 flex items-center gap-2"
            >
              <svg
                className="w-5 h-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 4v16m8-8H4"
                />
              </svg>
              Nuevo Usuario
            </button>
          )}
        </div>

        {/* Form or List */}
        {showForm ? (
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 dark:border dark:border-gray-700">
            <h2 className="text-xl font-bold mb-4 dark:text-white">
              {selectedUser ? 'Editar Usuario' : 'Crear Nuevo Usuario'}
            </h2>
            <UserForm
              user={selectedUser}
              onSubmit={handleSubmitUser}
              onCancel={handleCancelForm}
            />
          </div>
        ) : (
          <UserList
            onEdit={handleEditUser}
            onResetPassword={handleResetPassword}
            refreshTrigger={refreshTrigger}
          />
        )}

        {/* Password Reset Modal */}
        {showPasswordReset && userForPasswordReset && (
          <PasswordResetModal
            user={userForPasswordReset}
            onSubmit={handleSubmitPasswordReset}
            onClose={handleClosePasswordReset}
          />
        )}
      </div>
    </MainLayout>
  );
};

export default UsersPage;
