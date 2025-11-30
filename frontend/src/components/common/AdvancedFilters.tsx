/**
 * Advanced filters component
 */
import { useState } from 'react';
import { FiFilter, FiX, FiCheck } from 'react-icons/fi';

export interface FilterOption {
  key: string;
  label: string;
  type: 'select' | 'multiselect' | 'date' | 'daterange' | 'text' | 'number';
  options?: { value: string; label: string }[];
  placeholder?: string;
}

interface AdvancedFiltersProps {
  filters: FilterOption[];
  values: Record<string, any>;
  onChange: (key: string, value: any) => void;
  onClear: () => void;
  onApply: () => void;
}

export default function AdvancedFilters({
  filters,
  values,
  onChange,
  onClear,
  onApply,
}: AdvancedFiltersProps) {
  const [isOpen, setIsOpen] = useState(false);

  const activeFiltersCount = Object.values(values).filter(
    (v) => v !== null && v !== undefined && v !== ''
  ).length;

  const renderFilter = (filter: FilterOption) => {
    const value = values[filter.key];

    switch (filter.type) {
      case 'select':
        return (
          <select
            value={value || ''}
            onChange={(e) => onChange(filter.key, e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">Todos</option>
            {filter.options?.map((opt) => (
              <option key={opt.value} value={opt.value}>
                {opt.label}
              </option>
            ))}
          </select>
        );

      case 'multiselect':
        return (
          <div className="space-y-2">
            {filter.options?.map((opt) => {
              const selected = Array.isArray(value) && value.includes(opt.value);
              return (
                <label
                  key={opt.value}
                  className="flex items-center gap-2 cursor-pointer"
                >
                  <input
                    type="checkbox"
                    checked={selected}
                    onChange={(e) => {
                      const currentValues = Array.isArray(value) ? value : [];
                      if (e.target.checked) {
                        onChange(filter.key, [...currentValues, opt.value]);
                      } else {
                        onChange(
                          filter.key,
                          currentValues.filter((v) => v !== opt.value)
                        );
                      }
                    }}
                    className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  />
                  <span className="text-sm text-gray-700">{opt.label}</span>
                </label>
              );
            })}
          </div>
        );

      case 'date':
        return (
          <input
            type="date"
            value={value || ''}
            onChange={(e) => onChange(filter.key, e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        );

      case 'daterange':
        return (
          <div className="grid grid-cols-2 gap-2">
            <input
              type="date"
              value={value?.from || ''}
              onChange={(e) =>
                onChange(filter.key, { ...value, from: e.target.value })
              }
              placeholder="Desde"
              className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <input
              type="date"
              value={value?.to || ''}
              onChange={(e) =>
                onChange(filter.key, { ...value, to: e.target.value })
              }
              placeholder="Hasta"
              className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        );

      case 'text':
        return (
          <input
            type="text"
            value={value || ''}
            onChange={(e) => onChange(filter.key, e.target.value)}
            placeholder={filter.placeholder}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        );

      case 'number':
        return (
          <input
            type="number"
            value={value || ''}
            onChange={(e) => onChange(filter.key, e.target.value)}
            placeholder={filter.placeholder}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        );

      default:
        return null;
    }
  };

  return (
    <div className="relative">
      {/* Filter Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 px-4 py-2 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
      >
        <FiFilter className="w-4 h-4" />
        <span>Filtros</span>
        {activeFiltersCount > 0 && (
          <span className="px-2 py-0.5 text-xs font-semibold text-white bg-blue-600 rounded-full">
            {activeFiltersCount}
          </span>
        )}
      </button>

      {/* Filters Panel */}
      {isOpen && (
        <>
          {/* Backdrop */}
          <div
            className="fixed inset-0 z-40"
            onClick={() => setIsOpen(false)}
          />

          {/* Panel */}
          <div className="absolute right-0 mt-2 w-80 bg-white rounded-lg shadow-xl border border-gray-200 z-50">
            {/* Header */}
            <div className="flex items-center justify-between px-4 py-3 border-b">
              <h3 className="font-semibold text-gray-900">Filtros Avanzados</h3>
              <button
                onClick={() => setIsOpen(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                <FiX className="w-5 h-5" />
              </button>
            </div>

            {/* Filters */}
            <div className="p-4 space-y-4 max-h-96 overflow-y-auto">
              {filters.map((filter) => (
                <div key={filter.key}>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    {filter.label}
                  </label>
                  {renderFilter(filter)}
                </div>
              ))}
            </div>

            {/* Footer */}
            <div className="flex items-center justify-between px-4 py-3 bg-gray-50 border-t">
              <button
                onClick={() => {
                  onClear();
                  setIsOpen(false);
                }}
                className="px-4 py-2 text-sm text-gray-700 hover:text-gray-900"
              >
                Limpiar
              </button>
              <button
                onClick={() => {
                  onApply();
                  setIsOpen(false);
                }}
                className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                <FiCheck className="w-4 h-4" />
                Aplicar
              </button>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
