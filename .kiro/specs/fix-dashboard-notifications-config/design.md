# Design Document

## Overview

This design addresses three critical issues in the CMMS system:

1. **Negative KPI Values**: Dashboard displays negative values (e.g., -12.5 days) for time-based metrics due to invalid date calculations
2. **404 Errors on Notifications**: Clicking notifications leads to 404 pages because routes don't exist or objects are missing
3. **Incomplete Configuration CRUD**: Configuration page has placeholder modals without actual create/edit/delete functionality

The solution involves:
- Adding data validation and error handling to KPI calculations
- Implementing route validation and error handling for notification navigation
- Building complete CRUD forms with validation for all configuration entities

## Architecture

### Component Structure

```
Backend (Django)
├── dashboard_views.py (KPI calculation fixes)
├── configuration/
│   ├── models.py (new models for master data)
│   ├── serializers.py (validation logic)
│   ├── views.py (CRUD endpoints)
│   └── urls.py (API routes)

Frontend (React + TypeScript)
├── pages/
│   ├── Dashboard.tsx (KPI display)
│   ├── NotificationsPage.tsx (navigation fixes)
│   └── ConfigurationPage.tsx (CRUD forms)
├── components/
│   ├── notifications/NotificationBell.tsx (navigation fixes)
│   └── configuration/
│       ├── CategoryForm.tsx (new)
│       ├── PriorityForm.tsx (new)
│       ├── WorkOrderTypeForm.tsx (new)
│       └── ParameterForm.tsx (new)
└── services/
    └── configurationService.ts (already exists)
```

## Components and Interfaces

### 1. KPI Calculation Service (Backend)

**Location**: `backend/apps/core/dashboard_views.py`

**Changes**:
- Add date validation before calculating durations
- Filter out invalid work orders (completed_date < created_at)
- Ensure all KPI values are non-negative
- Add error logging for data quality issues

**Key Functions**:
```python
def calculate_avg_duration_days(work_orders):
    """Calculate average duration with validation"""
    valid_durations = []
    for order in work_orders:
        if order.completed_date and order.created_at:
            if order.completed_date >= order.created_at:
                duration = (order.completed_date - order.created_at).days
                if duration >= 0:
                    valid_durations.append(duration)
            else:
                logger.warning(f"Invalid dates for WO {order.id}")
    return sum(valid_durations) / len(valid_durations) if valid_durations else 0
```

### 2. Notification Navigation (Frontend)

**Location**: 
- `frontend/src/pages/NotificationsPage.tsx`
- `frontend/src/components/notifications/NotificationBell.tsx`

**Changes**:
- Validate route exists before navigation
- Check if related object exists via API call
- Display error toast if object not found
- Mark notification as read even if navigation fails

**Key Functions**:
```typescript
const handleNotificationClick = async (notification: Notification) => {
  try {
    // Verify object exists before navigating
    if (notification.related_object_type === 'work_order') {
      await api.get(`/work-orders/${notification.related_object_id}/`);
      navigate(`/work-orders/${notification.related_object_id}`);
    } else if (notification.related_object_type === 'asset') {
      await api.get(`/assets/${notification.related_object_id}/`);
      navigate(`/assets/${notification.related_object_id}`);
    }
    markAsRead(notification.id);
  } catch (error) {
    toast.error('El objeto relacionado ya no existe');
    markAsRead(notification.id);
  }
};
```

### 3. Configuration Models (Backend)

**Location**: `backend/apps/configuration/models.py` (new file)

**Models**:

```python
class AssetCategory(TimeStampedModel):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)

class Priority(TimeStampedModel):
    level = models.IntegerField(unique=True)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    color_code = models.CharField(max_length=7)  # Hex color
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)

class WorkOrderType(TimeStampedModel):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    requires_approval = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)

class SystemParameter(TimeStampedModel):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    description = models.TextField()
    data_type = models.CharField(max_length=20, choices=DATA_TYPE_CHOICES)
    is_editable = models.BooleanField(default=True)
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT)
```

### 4. Configuration Forms (Frontend)

**Location**: `frontend/src/components/configuration/`

**Components**:

- **CategoryForm**: Form for creating/editing asset categories
- **PriorityForm**: Form for creating/editing priorities with color picker
- **WorkOrderTypeForm**: Form for creating/editing work order types
- **ParameterForm**: Form for editing system parameters (type-aware)

**Common Form Features**:
- Field validation (required, format, uniqueness)
- Error display per field
- Loading states during save
- Success/error toast notifications
- Cancel button to close modal

## Data Models

### AssetCategory
```typescript
{
  id: number;
  code: string;          // Unique, max 20 chars
  name: string;          // Required, max 100 chars
  description: string;   // Optional
  is_active: boolean;    // Default true
  can_delete: boolean;   // Computed based on usage
}
```

### Priority
```typescript
{
  id: number;
  level: number;         // Unique, 1-5
  name: string;          // Required
  color_code: string;    // Hex format #RRGGBB
  description: string;   // Optional
  is_active: boolean;    // Default true
  can_delete: boolean;   // Computed based on usage
}
```

### WorkOrderType
```typescript
{
  id: number;
  code: string;          // Unique, max 20 chars
  name: string;          // Required
  description: string;   // Optional
  requires_approval: boolean;  // Default false
  is_active: boolean;    // Default true
  can_delete: boolean;   // Computed based on usage
}
```

### SystemParameter
```typescript
{
  id: number;
  key: string;           // Unique, max 100 chars
  value: string;         // Stored as text
  data_type: 'string' | 'integer' | 'float' | 'boolean' | 'json';
  description: string;
  is_editable: boolean;  // Some params are read-only
  typed_value: any;      // Parsed value based on data_type
}
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*


### KPI Calculation Properties

Property 1: KPI values are non-negative
*For any* set of work orders, the calculated average duration KPI should always be greater than or equal to zero
**Validates: Requirements 1.1**

Property 2: Invalid date data is excluded
*For any* work order with completed_date before created_at, that work order should not be included in KPI calculations
**Validates: Requirements 1.2, 1.4**

Property 3: Data errors are logged and handled
*For any* KPI calculation that encounters invalid data, the system should log the error and continue processing with valid data only
**Validates: Requirements 1.5**

### Notification Navigation Properties

Property 4: Valid objects navigate correctly
*For any* notification with a valid related_object_id and related_object_type, clicking the notification should navigate to the correct detail page
**Validates: Requirements 2.1, 2.2**

Property 5: Invalid objects show error messages
*For any* notification referencing a non-existent object, clicking should display an error message and mark the notification as read without navigating
**Validates: Requirements 2.3, 2.4**

### Configuration CRUD Properties

Property 6: CRUD operations preserve data integrity
*For any* valid configuration entity (category, priority, type, parameter), create and update operations should save all provided fields correctly to the database
**Validates: Requirements 3.1, 3.2**

Property 7: Delete operations validate dependencies
*For any* configuration entity, delete operations should only succeed if the entity has no dependencies (can_delete is true)
**Validates: Requirements 3.3**

Property 8: Type validation for parameters
*For any* system parameter update, the provided value should match the parameter's defined data_type or be rejected
**Validates: Requirements 3.4**

Property 9: Validation errors display field-specific messages
*For any* form submission with validation errors, each invalid field should display a specific error message
**Validates: Requirements 3.5**

Property 10: Successful operations provide feedback
*For any* successful CRUD operation, the system should refresh the data table and display a success message
**Validates: Requirements 3.6**

Property 11: Failed operations keep modal open
*For any* failed CRUD operation, the system should display an error message without closing the modal
**Validates: Requirements 3.7**

### Form Validation Properties

Property 12: Non-editable parameters cannot be modified
*For any* system parameter where is_editable is false, the edit form should prevent modifications
**Validates: Requirements 4.4**

Property 13: Required fields block submission
*For any* form with required fields, submission should be prevented if any required field is empty
**Validates: Requirements 4.5**

Property 14: Color codes are validated
*For any* color code input, only valid hexadecimal color formats (#RRGGBB) should be accepted
**Validates: Requirements 4.6**

Property 15: Unique constraints are enforced
*For any* code or key field with uniqueness constraints, duplicate values should be rejected with an error message
**Validates: Requirements 4.7**

## Error Handling

### KPI Calculation Errors

**Invalid Date Scenarios**:
- completed_date is null but status is "Completada"
- completed_date < created_at
- Dates are in the future

**Handling Strategy**:
1. Log warning with work order ID
2. Exclude from calculation
3. Continue with remaining valid data
4. Return 0 if no valid data exists

### Notification Navigation Errors

**Error Scenarios**:
- Related object deleted after notification created
- Invalid related_object_id
- Route doesn't exist in frontend
- API returns 404

**Handling Strategy**:
1. Catch navigation errors
2. Display user-friendly toast message
3. Mark notification as read anyway
4. Don't navigate to 404 page

### Configuration CRUD Errors

**Validation Errors**:
- Required field missing
- Invalid format (e.g., color code)
- Duplicate code/key
- Type mismatch for parameters
- Cannot delete (has dependencies)

**Handling Strategy**:
1. Return 400 with field-specific errors
2. Display errors in form
3. Keep modal open for correction
4. Highlight invalid fields

**Server Errors**:
- Database connection issues
- Permission denied
- Unexpected errors

**Handling Strategy**:
1. Display generic error message
2. Log error details
3. Keep modal open
4. Allow retry

## Testing Strategy

### Unit Testing

**Backend Unit Tests**:
- Test KPI calculation functions with various date scenarios
- Test configuration model validation
- Test serializer validation logic
- Test can_delete logic for each entity

**Frontend Unit Tests**:
- Test form validation functions
- Test notification click handlers
- Test error message display
- Test modal open/close logic

### Property-Based Testing

We will use **pytest with Hypothesis** for Python backend tests and **fast-check** for TypeScript frontend tests.

Each property-based test should run a minimum of 100 iterations to ensure comprehensive coverage.

**Backend Property Tests**:
- Property 1: Generate random work order datasets, verify KPIs are non-negative
- Property 2: Generate work orders with invalid dates, verify they're excluded
- Property 3: Generate data with errors, verify logging and continuation
- Property 7: Generate entities with/without dependencies, verify delete behavior
- Property 8: Generate parameter updates with mismatched types, verify rejection

**Frontend Property Tests**:
- Property 13: Generate forms with missing required fields, verify submission blocked
- Property 14: Generate random strings, verify only valid hex colors accepted
- Property 15: Generate duplicate codes, verify rejection

### Integration Testing

**End-to-End Scenarios**:
1. Dashboard loads with correct KPIs (no negatives)
2. Click notification → navigate to correct page
3. Click notification for deleted object → see error message
4. Create new category → appears in table
5. Edit priority → changes saved
6. Try to delete used work order type → see error
7. Submit form with errors → see field-specific messages

### Manual Testing Checklist

- [ ] Dashboard shows all KPIs as non-negative values
- [ ] Clicking work order notification navigates correctly
- [ ] Clicking asset notification navigates correctly
- [ ] Clicking notification for deleted object shows error
- [ ] Can create new asset category
- [ ] Can edit existing priority
- [ ] Can delete unused work order type
- [ ] Cannot delete used work order type
- [ ] Form validation shows field-specific errors
- [ ] Color picker validates hex format
- [ ] Duplicate codes are rejected
- [ ] Success messages appear after save
- [ ] Error messages appear on failure
- [ ] Modal stays open on error

## Implementation Notes

### Backend Considerations

1. **Database Migrations**: Need to create new configuration models
2. **Permissions**: Only admins can access configuration endpoints
3. **Audit Logging**: All configuration changes should be logged
4. **Cache Invalidation**: Clear dashboard cache when data changes
5. **Soft Deletes**: Consider soft delete for configuration entities

### Frontend Considerations

1. **Form State Management**: Use React Hook Form for validation
2. **Color Picker**: Use a library like react-color
3. **Toast Notifications**: Use existing react-hot-toast
4. **Loading States**: Show spinners during API calls
5. **Optimistic Updates**: Update UI before API response for better UX

### Performance Considerations

1. **Dashboard Caching**: Keep 5-minute cache for KPIs
2. **Configuration Caching**: Cache configuration data in frontend
3. **Lazy Loading**: Load configuration data only when tab is active
4. **Debouncing**: Debounce form validation for better UX

### Security Considerations

1. **Admin-Only Access**: Verify user role on backend
2. **CSRF Protection**: Ensure CSRF tokens on all mutations
3. **Input Sanitization**: Sanitize all user inputs
4. **SQL Injection**: Use ORM parameterized queries
5. **XSS Prevention**: Escape all user-generated content

## Dependencies

### Backend
- Django REST Framework (already installed)
- Django Cache Framework (already configured)
- Python logging (built-in)

### Frontend
- React Hook Form (for form validation)
- react-color (for color picker)
- react-hot-toast (already installed)
- React Router (already installed)

## Migration Strategy

### Phase 1: Backend Fixes
1. Fix KPI calculation logic
2. Add data validation
3. Add error logging

### Phase 2: Notification Fixes
1. Add route validation
2. Add error handling
3. Update click handlers

### Phase 3: Configuration Models
1. Create models
2. Create serializers
3. Create viewsets
4. Add URLs

### Phase 4: Configuration Forms
1. Create form components
2. Add validation
3. Wire up to API
4. Add error handling

### Phase 5: Testing & Deployment
1. Write unit tests
2. Write property tests
3. Manual testing
4. Deploy to production
