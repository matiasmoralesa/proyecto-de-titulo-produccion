import { useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { useAuthStore } from './store/authStore';
import ErrorBoundary from './components/common/ErrorBoundary';
import ProtectedRoute from './components/auth/ProtectedRoute';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Assets from './pages/Assets';
import WorkOrders from './pages/WorkOrders';
import MaintenancePlans from './pages/MaintenancePlans';
import Inventory from './pages/Inventory';
import ChecklistsPage from './pages/ChecklistsPage';
import NewChecklistPage from './pages/NewChecklistPage';
import NotificationsPage from './pages/NotificationsPage';
import ReportsPage from './pages/ReportsPage';
import ConfigurationPage from './pages/ConfigurationPage';
import LocationsPage from './pages/LocationsPage';
import UsersPage from './pages/UsersPage';
import MachineStatusPage from './pages/MachineStatusPage';
import StatusHistoryPage from './pages/StatusHistoryPage';
import AssetDetailPage from './pages/AssetDetailPage';
import MLPredictionsPage from './pages/MLPredictionsPage';
import CeleryMonitorPage from './pages/CeleryMonitorPage';
import Unauthorized from './pages/Unauthorized';
import NotFound from './pages/NotFound';

function App() {
  const { loadUserFromStorage } = useAuthStore();

  // Load user from localStorage on app mount
  useEffect(() => {
    loadUserFromStorage();
  }, [loadUserFromStorage]);

  return (
    <ErrorBoundary>
      <BrowserRouter>
        <Toaster position="top-right" />
        <Routes>
          {/* Public routes */}
          <Route path="/login" element={<Login />} />
          <Route path="/unauthorized" element={<Unauthorized />} />

          {/* Protected routes */}
          <Route element={<ProtectedRoute />}>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/assets" element={<Assets />} />
            <Route path="/work-orders" element={<WorkOrders />} />
            <Route path="/maintenance" element={<MaintenancePlans />} />
            <Route path="/inventory" element={<Inventory />} />
            <Route path="/checklists" element={<ChecklistsPage />} />
            <Route path="/checklists/new" element={<NewChecklistPage />} />
            <Route path="/notifications" element={<NotificationsPage />} />
            <Route path="/reports" element={<ReportsPage />} />
            <Route path="/configuration" element={<ConfigurationPage />} />
            <Route path="/locations" element={<LocationsPage />} />
            <Route path="/users" element={<UsersPage />} />
            <Route path="/machine-status" element={<MachineStatusPage />} />
            <Route path="/status-history" element={<StatusHistoryPage />} />
            <Route path="/assets/:id" element={<AssetDetailPage />} />
            <Route path="/ml-predictions" element={<MLPredictionsPage />} />
            <Route path="/celery-monitor" element={<CeleryMonitorPage />} />
          </Route>

          {/* Redirect root to dashboard or login */}
          <Route path="/" element={<Navigate to="/dashboard" replace />} />

          {/* 404 - Not Found */}
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </ErrorBoundary>
  );
}

export default App;
