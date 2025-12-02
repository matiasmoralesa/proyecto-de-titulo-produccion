# Implementation Plan

- [ ] 1. Fix KPI calculation logic in dashboard
- [x] 1.1 Update dashboard_views.py to validate work order dates before calculating average duration


  - Add date validation function to check completed_date >= created_at
  - Filter out work orders with invalid dates
  - Add logging for invalid date scenarios
  - Ensure avg_duration_days is always >= 0
  - _Requirements: 1.1, 1.2, 1.4_

- [ ] 1.2 Write property test for KPI non-negative values
  - **Property 1: KPI values are non-negative**
  - **Validates: Requirements 1.1**

- [ ] 1.3 Write property test for invalid date exclusion
  - **Property 2: Invalid date data is excluded**
  - **Validates: Requirements 1.2, 1.4**


- [ ] 1.4 Add error logging for data quality issues in KPI calculations
  - Log warnings when work orders have invalid dates
  - Log when completed orders are missing completed_date
  - Continue processing with valid data only
  - _Requirements: 1.5_

- [ ] 1.5 Write property test for error logging and handling
  - **Property 3: Data errors are logged and handled**
  - **Validates: Requirements 1.5**



- [ ] 2. Fix notification navigation to prevent 404 errors
- [ ] 2.1 Update NotificationsPage.tsx to validate objects before navigation
  - Add API call to verify work order exists before navigating
  - Add API call to verify asset exists before navigating


  - Show error toast if object doesn't exist
  - Mark notification as read even if navigation fails
  - _Requirements: 2.1, 2.2, 2.3, 2.4_

- [ ] 2.2 Update NotificationBell.tsx with same navigation validation
  - Apply same validation logic as NotificationsPage
  - Ensure consistent error handling
  - _Requirements: 2.1, 2.2, 2.3, 2.4_

- [ ] 2.3 Write property test for valid object navigation
  - **Property 4: Valid objects navigate correctly**
  - **Validates: Requirements 2.1, 2.2**

- [ ] 2.4 Write unit test for invalid object error handling
  - Test that non-existent objects show error messages
  - Test that notifications are marked as read
  - _Requirements: 2.3, 2.4_

- [ ] 3. Create backend configuration models and API
- [x] 3.1 Create configuration app and models


  - Create apps/configuration/ directory structure
  - Create AssetCategory model with code, name, description, is_active
  - Create Priority model with level, name, color_code, is_active
  - Create WorkOrderType model with code, name, description, requires_approval, is_active
  - Create SystemParameter model with key, value, data_type, is_editable
  - Add can_delete property to each model
  - _Requirements: 3.1, 3.2, 3.3, 3.4_

- [x] 3.2 Create database migrations for configuration models


  - Generate migrations for new models
  - Run migrations
  - _Requirements: 3.1, 3.2, 3.3, 3.4_


- [ ] 3.3 Create serializers with validation logic
  - Create AssetCategorySerializer with code uniqueness validation
  - Create PrioritySerializer with level uniqueness and color validation
  - Create WorkOrderTypeSerializer with code uniqueness validation
  - Create SystemParameterSerializer with type validation
  - Add field-specific error messages
  - _Requirements: 3.4, 3.5, 4.6, 4.7_

- [ ] 3.4 Write property test for type validation
  - **Property 8: Type validation for parameters**
  - **Validates: Requirements 3.4**

- [ ] 3.5 Write property test for unique constraints
  - **Property 15: Unique constraints are enforced**
  - **Validates: Requirements 4.7**

- [x] 3.4 Create viewsets for CRUD operations

  - Create AssetCategoryViewSet with full CRUD
  - Create PriorityViewSet with full CRUD
  - Create WorkOrderTypeViewSet with full CRUD
  - Create SystemParameterViewSet with full CRUD
  - Add permission checks (admin only)
  - Implement can_delete logic in destroy method
  - _Requirements: 3.1, 3.2, 3.3_

- [ ] 3.5 Write property test for CRUD data integrity
  - **Property 6: CRUD operations preserve data integrity**
  - **Validates: Requirements 3.1, 3.2**

- [ ] 3.6 Write property test for delete validation
  - **Property 7: Delete operations validate dependencies**
  - **Validates: Requirements 3.3**

- [x] 3.6 Add URL routing for configuration endpoints

  - Register viewsets with router
  - Add configuration URLs to main urls.py
  - Test endpoints with curl or Postman
  - _Requirements: 3.1, 3.2, 3.3, 3.4_

- [ ] 4. Create configuration form components
- [x] 4.1 Create CategoryForm component


  - Add fields: code, name, description, is_active
  - Add React Hook Form validation
  - Add required field validation
  - Add code uniqueness check
  - Display field-specific error messages
  - _Requirements: 3.1, 3.5, 4.1, 4.5, 4.7_

- [x] 4.2 Create PriorityForm component

  - Add fields: level, name, color_code, description, is_active
  - Add React Hook Form validation
  - Add color picker component
  - Add hex color format validation
  - Add level uniqueness check
  - Display field-specific error messages
  - _Requirements: 3.2, 3.5, 4.2, 4.5, 4.6, 4.7_

- [ ] 4.3 Write property test for color validation
  - **Property 14: Color codes are validated**
  - **Validates: Requirements 4.6**

- [x] 4.4 Create WorkOrderTypeForm component

  - Add fields: code, name, description, requires_approval, is_active
  - Add React Hook Form validation
  - Add required field validation
  - Add code uniqueness check
  - Display field-specific error messages
  - _Requirements: 3.1, 3.5, 4.3, 4.5, 4.7_


- [ ] 4.5 Create ParameterForm component
  - Add fields: value, description (key is read-only)
  - Add type-aware input fields (text, number, boolean, json)
  - Add validation based on data_type
  - Only allow editing if is_editable is true
  - Display field-specific error messages
  - _Requirements: 3.4, 3.5, 4.4, 4.5_

- [ ] 4.6 Write property test for non-editable parameters
  - **Property 12: Non-editable parameters cannot be modified**
  - **Validates: Requirements 4.4**

- [ ] 4.7 Write property test for required field validation
  - **Property 13: Required fields block submission**
  - **Validates: Requirements 4.5**

- [ ] 5. Integrate forms into ConfigurationPage
- [x] 5.1 Update ConfigurationPage to use real forms instead of placeholders


  - Replace placeholder modal with CategoryForm for categories tab
  - Replace placeholder modal with PriorityForm for priorities tab
  - Replace placeholder modal with WorkOrderTypeForm for types tab
  - Replace placeholder modal with ParameterForm for parameters tab
  - Wire up create/edit/delete handlers to API
  - _Requirements: 3.1, 3.2, 3.3, 3.4_

- [x] 5.2 Add success and error handling to CRUD operations

  - Show success toast on successful create/update/delete
  - Show error toast on failure
  - Keep modal open on error
  - Close modal on success
  - Refresh data table after successful operation
  - _Requirements: 3.6, 3.7_

- [ ] 5.3 Write property test for success feedback
  - **Property 10: Successful operations provide feedback**
  - **Validates: Requirements 3.6**

- [ ] 5.4 Write property test for error handling
  - **Property 11: Failed operations keep modal open**
  - **Validates: Requirements 3.7**

- [ ] 5.5 Write property test for validation error messages
  - **Property 9: Validation errors display field-specific messages**
  - **Validates: Requirements 3.5**

- [ ] 6. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 7. Manual testing and bug fixes
- [ ] 7.1 Test dashboard KPIs display correctly
  - Verify no negative values appear
  - Test with various work order date scenarios
  - _Requirements: 1.1, 1.2, 1.3, 1.4_

- [ ] 7.2 Test notification navigation
  - Click notifications for existing work orders
  - Click notifications for existing assets
  - Click notifications for deleted objects
  - Verify error messages appear correctly
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

- [ ] 7.3 Test configuration CRUD operations
  - Create new category, priority, type, parameter
  - Edit existing items
  - Try to delete items with dependencies
  - Delete items without dependencies
  - Test form validation with invalid inputs
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7_

- [ ] 8. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.
