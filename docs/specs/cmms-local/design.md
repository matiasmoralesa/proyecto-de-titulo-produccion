# Design Document - Sistema CMMS Local

## Overview

El Sistema CMMS (Computerized Maintenance Management System) es una aplicación web completa para la gestión de mantenimiento de activos industriales. El sistema está diseñado para funcionar completamente en entorno local, sin dependencias de servicios cloud externos.

**Arquitectura:** Cliente-Servidor con API REST
**Backend:** Django REST Framework
**Frontend:** React + TypeScript + Vite
**Base de Datos:** SQLite (desarrollo) / PostgreSQL (producción)

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend (React)                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │Dashboard │  │ Assets   │  │Work Order│  │ Reports  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         State Management (Zustand)                    │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         API Client (Axios)                            │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────┬───────────────────────────────────────┘
                       │ HTTP/REST (JSON)
                       │ JWT Authentication
┌──────────────────────▼───────────────────────────────────────┐
│                  Backend API (Django REST Framework)          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Auth    │  │ Assets   │  │Work Order│  │ Reports  │   │
│  │  API     │  │  API     │  │   API    │  │   API    │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Business Logic Layer                          │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Data Access Layer (Django ORM)                │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────┬───────────────────────────────────────┘
                       │
┌──────────────────────▼───────────────────────────────────────┐
│              Database (SQLite / PostgreSQL)                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Users   │  │ Assets   │  │Work Order│  │ Reports  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└───────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│              File Storage (Local Media Folder)                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                   │
│  │Documents │  │  Photos  │  │   PDFs   │                   │
│  └──────────┘  └──────────┘  └──────────┘                   │
└───────────────────────────────────────────────────────────────┘
```

### Technology Stack

**Backend:**
- Django 4.2+
- Django REST Framework 3.14+
- djangorestframework-simplejwt (JWT authentication)
- drf-spectacular (OpenAPI/Swagger documentation)
- Pillow (image processing)
- ReportLab (PDF generation)
- Python 3.9+

**Frontend:**
- React 18+
- TypeScript 5+
- Vite 5+ (build tool)
- React Router v6 (routing)
- Zustand (state management)
- Axios (HTTP client)
- Tailwind CSS (styling)
- Recharts (charts and graphs)

**Database:**
- SQLite (development)
- PostgreSQL 14+ (production recommended)

**Development Tools:**
- Git (version control)
- ESLint + Prettier (code formatting)
- Black + isort (Python formatting)

## Components and Interfaces

### Backend Apps Structure

```
backend/
├── config/
│   ├── settings/
│   │   ├── base.py          # Base settings
│   │   ├── development.py   # Development settings
│   │   └── production.py    # Production settings
│   ├── urls.py              # Main URL configuration
│   └── wsgi.py
│
├── apps/
│   ├── authentication/      # User authentication and authorization
│   │   ├── models.py        # User, Role models
│   │   ├── serializers.py   # User serializers
│   │   ├── views.py         # Auth endpoints
│   │   └── permissions.py   # Custom permissions
│   │
│   ├── assets/              # Asset management
│   │   ├── models.py        # Asset, Location, AssetDocument
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── filters.py
│   │
│   ├── work_orders/         # Work order management
│   │   ├── models.py        # WorkOrder, WorkOrderStatus
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── signals.py       # Notification triggers
│   │
│   ├── maintenance/         # Maintenance planning
│   │   ├── models.py        # MaintenancePlan
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── utils.py         # Recurrence calculation
│   │
│   ├── inventory/           # Spare parts inventory
│   │   ├── models.py        # SparePart, StockMovement
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── signals.py       # Low stock alerts
│   │
│   ├── checklists/          # Checklist system
│   │   ├── models.py        # ChecklistTemplate, ChecklistResponse
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── pdf_generator.py # PDF generation
│   │   └── management/
│   │       └── commands/
│   │           └── load_checklist_templates.py
│   │
│   ├── notifications/       # Notification system
│   │   ├── models.py        # Notification, NotificationPreference
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── utils.py         # Notification creation helpers
│   │
│   ├── reports/             # Reports and analytics
│   │   ├── models.py        # Report configurations
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── calculators.py   # KPI calculations
│   │
│   ├── machine_status/      # Machine status updates
│   │   ├── models.py        # AssetStatus, AssetStatusHistory
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── signals.py       # Status change alerts
│   │
│   └── core/                # Shared utilities
│       ├── models.py        # Base models, audit fields
│       ├── permissions.py   # Shared permissions
│       ├── pagination.py    # Custom pagination
│       └── utils.py         # Helper functions
│
├── media/                   # User uploaded files
│   ├── documents/
│   ├── photos/
│   └── pdfs/
│
└── manage.py
```

### Frontend Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Layout.tsx           # Main layout wrapper
│   │   │   ├── Sidebar.tsx          # Navigation sidebar
│   │   │   ├── Header.tsx           # Top header
│   │   │   └── Footer.tsx
│   │   │
│   │   ├── auth/
│   │   │   ├── ProtectedRoute.tsx   # Route guard
│   │   │   └── LoginForm.tsx
│   │   │
│   │   ├── assets/
│   │   │   ├── AssetList.tsx
│   │   │   ├── AssetForm.tsx
│   │   │   ├── AssetDetail.tsx
│   │   │   └── AssetCard.tsx
│   │   │
│   │   ├── work-orders/
│   │   │   ├── WorkOrderList.tsx
│   │   │   ├── WorkOrderForm.tsx
│   │   │   ├── WorkOrderDetail.tsx
│   │   │   └── WorkOrderKanban.tsx
│   │   │
│   │   ├── checklists/
│   │   │   ├── ChecklistTemplateViewer.tsx
│   │   │   ├── ChecklistExecutor.tsx
│   │   │   └── ChecklistViewer.tsx
│   │   │
│   │   ├── notifications/
│   │   │   ├── NotificationBell.tsx
│   │   │   ├── NotificationList.tsx
│   │   │   └── ToastContainer.tsx
│   │   │
│   │   └── common/
│   │       ├── Button.tsx
│   │       ├── Input.tsx
│   │       ├── Modal.tsx
│   │       ├── Table.tsx
│   │       └── Card.tsx
│   │
│   ├── pages/
│   │   ├── Login.tsx
│   │   ├── Dashboard.tsx
│   │   ├── Assets.tsx
│   │   ├── WorkOrders.tsx
│   │   ├── Maintenance.tsx
│   │   ├── Inventory.tsx
│   │   ├── Checklists.tsx
│   │   ├── Reports.tsx
│   │   ├── Notifications.tsx
│   │   ├── Admin.tsx
│   │   ├── LocationsPage.tsx
│   │   ├── UsersPage.tsx
│   │   └── MachineStatusPage.tsx
│   │
│   ├── services/
│   │   ├── api.ts               # Axios instance configuration
│   │   ├── authService.ts       # Authentication API calls
│   │   ├── assetService.ts      # Asset API calls
│   │   ├── workOrderService.ts  # Work order API calls
│   │   └── ...
│   │
│   ├── store/
│   │   ├── authStore.ts         # Authentication state
│   │   ├── notificationStore.ts # Notifications state
│   │   └── ...
│   │
│   ├── types/
│   │   ├── auth.types.ts
│   │   ├── asset.types.ts
│   │   ├── workOrder.types.ts
│   │   └── ...
│   │
│   ├── utils/
│   │   ├── formatters.ts        # Date, number formatters
│   │   ├── validators.ts        # Form validators
│   │   └── constants.ts         # App constants
│   │
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css
│
├── public/
├── package.json
├── tsconfig.json
├── vite.config.ts
└── tailwind.config.js
```

## Data Models

### Core Models

#### User Model
```python
class User(AbstractUser):
    id = UUIDField(primary_key=True, default=uuid4)
    email = EmailField(unique=True)
    role = ForeignKey('Role', on_delete=PROTECT)
    phone = CharField(max_length=20, blank=True)
    is_active = BooleanField(default=True)
    must_change_password = BooleanField(default=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
```

#### Role Model
```python
class Role(Model):
    name = CharField(max_length=50, unique=True)  # ADMIN, SUPERVISOR, OPERADOR
    description = TextField()
    permissions = ManyToManyField('Permission')
```

#### Asset Model
```python
class Asset(Model):
    id = UUIDField(primary_key=True, default=uuid4)
    name = CharField(max_length=200)
    vehicle_type = CharField(max_length=50, choices=VEHICLE_TYPE_CHOICES)
    model = CharField(max_length=100)
    serial_number = CharField(max_length=100, unique=True)
    license_plate = CharField(max_length=20, unique=True, null=True)
    location = ForeignKey('Location', on_delete=PROTECT)
    installation_date = DateField()
    status = CharField(max_length=50, choices=STATUS_CHOICES)
    is_archived = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    created_by = ForeignKey('User', on_delete=PROTECT)
```

#### WorkOrder Model
```python
class WorkOrder(Model):
    id = UUIDField(primary_key=True, default=uuid4)
    work_order_number = CharField(max_length=50, unique=True)
    title = CharField(max_length=200)
    description = TextField()
    priority = CharField(max_length=20, choices=PRIORITY_CHOICES)
    status = CharField(max_length=50, choices=STATUS_CHOICES)
    asset = ForeignKey('Asset', on_delete=PROTECT)
    assigned_to = ForeignKey('User', on_delete=PROTECT, related_name='assigned_work_orders')
    scheduled_date = DateTimeField()
    completed_date = DateTimeField(null=True)
    completion_notes = TextField(blank=True)
    actual_hours = DecimalField(max_digits=5, decimal_places=2, null=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    created_by = ForeignKey('User', on_delete=PROTECT)
```

#### MaintenancePlan Model
```python
class MaintenancePlan(Model):
    id = UUIDField(primary_key=True, default=uuid4)
    name = CharField(max_length=200)
    description = TextField()
    asset = ForeignKey('Asset', on_delete=CASCADE)
    recurrence_type = CharField(max_length=20, choices=RECURRENCE_CHOICES)
    recurrence_interval = IntegerField()
    next_due_date = DateField()
    is_active = BooleanField(default=True)
    is_paused = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
```

#### SparePart Model
```python
class SparePart(Model):
    id = UUIDField(primary_key=True, default=uuid4)
    part_number = CharField(max_length=100, unique=True)
    name = CharField(max_length=200)
    description = TextField()
    quantity = IntegerField(default=0)
    minimum_stock_level = IntegerField()
    unit_price = DecimalField(max_digits=10, decimal_places=2)
    location = CharField(max_length=200)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
```

#### ChecklistTemplate Model
```python
class ChecklistTemplate(Model):
    id = UUIDField(primary_key=True, default=uuid4)
    code = CharField(max_length=50, unique=True)
    name = CharField(max_length=200)
    vehicle_type = CharField(max_length=50, choices=VEHICLE_TYPE_CHOICES)
    is_system_template = BooleanField(default=False)
    items = JSONField()  # List of checklist items
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
```

#### Notification Model
```python
class Notification(Model):
    id = UUIDField(primary_key=True, default=uuid4)
    user = ForeignKey('User', on_delete=CASCADE)
    title = CharField(max_length=200)
    message = TextField()
    notification_type = CharField(max_length=50, choices=TYPE_CHOICES)
    is_read = BooleanField(default=False)
    related_object_type = CharField(max_length=50, null=True)
    related_object_id = UUIDField(null=True)
    created_at = DateTimeField(auto_now_add=True)
```

### Database Relationships

```
User ──┬─── WorkOrder (created_by)
       ├─── WorkOrder (assigned_to)
       ├─── Asset (created_by)
       ├─── Notification
       └─── Role

Asset ──┬─── WorkOrder
        ├─── MaintenancePlan
        ├─── ChecklistResponse
        ├─── AssetStatus
        └─── Location

WorkOrder ──┬─── ChecklistResponse
            └─── StockMovement

ChecklistTemplate ─── ChecklistResponse

SparePart ─── StockMovement
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Unique Asset Identifiers
*For any* two Assets in the system, their serial numbers and license plates (if present) must be unique.
**Validates: Requirements 1.5**

### Property 2: Role-Based Access Control
*For any* user with OPERADOR role, they can only view and modify Work_Orders and Assets that are explicitly assigned to them.
**Validates: Requirements 6.4**

### Property 3: Work Order Status Transitions
*For any* Work_Order, status transitions must follow the valid sequence: pending → in-progress → completed (or cancelled from any state).
**Validates: Requirements 2.3**

### Property 4: Stock Level Non-Negativity
*For any* SparePart, the quantity must never be negative after any stock operation.
**Validates: Requirements 4.5**

### Property 5: Maintenance Plan Recurrence Calculation
*For any* MaintenancePlan with recurrence rules, the next_due_date must be correctly calculated based on the recurrence_type and recurrence_interval.
**Validates: Requirements 3.4**

### Property 6: Checklist Template Immutability
*For any* ChecklistTemplate where is_system_template is True, the structure (items) cannot be modified or deleted.
**Validates: Requirements 5.2**

### Property 7: Notification Creation on Work Order Assignment
*For any* Work_Order that is created or has its assigned_to field changed, a Notification must be created for the assigned user.
**Validates: Requirements 2.2**

### Property 8: Low Stock Alert Generation
*For any* SparePart where quantity falls below minimum_stock_level, an alert Notification must be created.
**Validates: Requirements 4.2**

### Property 9: Asset Archival Instead of Deletion
*For any* Asset deletion request, the Asset must be marked as archived (is_archived=True) rather than being permanently deleted from the database.
**Validates: Requirements 1.6**

### Property 10: JWT Token Expiration
*For any* authenticated request, if the JWT token is expired, the Backend_API must return HTTP 401 Unauthorized.
**Validates: Requirements 6.1**

### Property 11: Admin-Only User Management
*For any* user management operation (create, update, delete), only users with ADMIN role can perform these actions.
**Validates: Requirements 10.3**

### Property 12: Master Data Deletion Prevention
*For any* master data record (Location, Role, etc.) that is referenced by other records, deletion must be prevented.
**Validates: Requirements 13.2**

### Property 13: Status History Audit Trail
*For any* Asset status update, a complete history record must be created with timestamp, user, and previous values.
**Validates: Requirements 11.7**

### Property 14: Complete Asset History Retrieval
*For any* Asset, the history endpoint must return all related activities including status updates, Work_Orders, maintenance activities, Checklist completions, and Spare_Part usage in chronological order.
**Validates: Requirements 11.3**

### Property 15: Asset Timeline Completeness
*For any* activity performed on an Asset (status update, work order, maintenance, checklist), that activity must appear in the Asset's unified timeline view.
**Validates: Requirements 11.4**

### Property 16: Asset KPI Calculation Accuracy
*For any* Asset, the calculated KPIs (total maintenance hours, work orders completed, average downtime, maintenance cost) must accurately reflect the sum/average of all related historical records.
**Validates: Requirements 11.10**

### Property 17: Checklist Completion Percentage Calculation
*For any* completed Checklist, the completion percentage must accurately reflect the ratio of completed items to total items.
**Validates: Requirements 5.6**

### Property 18: Work Order Completion Requirements
*For any* Work_Order being marked as completed, completion_notes and actual_hours must be provided.
**Validates: Requirements 2.5**

## Error Handling

### Backend Error Handling Strategy

1. **Validation Errors (HTTP 400)**
   - Invalid input data
   - Missing required fields
   - Format errors

2. **Authentication Errors (HTTP 401)**
   - Invalid credentials
   - Expired JWT token
   - Missing authentication

3. **Authorization Errors (HTTP 403)**
   - Insufficient permissions
   - Role-based access denied

4. **Not Found Errors (HTTP 404)**
   - Resource does not exist
   - Invalid UUID

5. **Conflict Errors (HTTP 409)**
   - Unique constraint violations
   - Concurrent modification conflicts

6. **Server Errors (HTTP 500)**
   - Unexpected exceptions
   - Database errors
   - File system errors

### Frontend Error Handling

1. **Network Errors**
   - Display user-friendly error messages
   - Retry mechanism for failed requests
   - Offline detection

2. **Validation Errors**
   - Real-time form validation
   - Clear error messages next to fields
   - Prevent submission of invalid data

3. **Authorization Errors**
   - Redirect to login page
   - Clear stored tokens
   - Display "session expired" message

4. **User Feedback**
   - Toast notifications for success/error
   - Loading states during operations
   - Confirmation dialogs for destructive actions

## Testing Strategy

### Backend Testing

**Unit Tests:**
- Model validation logic
- Business logic functions
- Permission classes
- Utility functions

**Integration Tests:**
- API endpoint functionality
- Database operations
- File upload/download
- Authentication flow

**Property-Based Tests:**
- Test correctness properties with multiple random inputs
- Use hypothesis library for Python
- Minimum 100 iterations per property test

### Frontend Testing

**Unit Tests:**
- Component rendering
- Utility functions
- State management logic

**Integration Tests:**
- User workflows
- API integration
- Form submissions

**E2E Tests (Optional):**
- Complete user journeys
- Cross-browser testing

### Testing Tools

**Backend:**
- pytest
- pytest-django
- factory_boy (test data generation)
- hypothesis (property-based testing)

**Frontend:**
- Vitest
- React Testing Library
- MSW (Mock Service Worker)

## Security Considerations

1. **Authentication**
   - JWT tokens with expiration
   - Secure password hashing (Django's PBKDF2)
   - Password complexity requirements

2. **Authorization**
   - Role-based access control
   - Permission checks on all endpoints
   - Object-level permissions

3. **Data Protection**
   - SQL injection prevention (Django ORM)
   - XSS prevention (React escaping)
   - CSRF protection (Django middleware)

4. **File Upload Security**
   - File type validation
   - File size limits
   - Virus scanning (optional)
   - Secure file storage

5. **API Security**
   - Rate limiting
   - CORS configuration
   - HTTPS enforcement (production)
   - Security headers

## Performance Considerations

1. **Database Optimization**
   - Proper indexing on frequently queried fields
   - Query optimization with select_related/prefetch_related
   - Database connection pooling

2. **API Performance**
   - Pagination for list endpoints
   - Filtering and search optimization
   - Response caching where appropriate

3. **Frontend Performance**
   - Code splitting
   - Lazy loading of routes
   - Image optimization
   - Bundle size optimization

4. **File Storage**
   - Efficient file serving
   - Thumbnail generation for images
   - File compression

## Deployment Architecture

### Development Environment
```
┌─────────────────────────────────────┐
│  Developer Machine                   │
│  ┌─────────────┐  ┌───────────────┐│
│  │  Frontend   │  │   Backend     ││
│  │  (Vite Dev) │  │ (Django Dev)  ││
│  │  :5173      │  │   :8000       ││
│  └─────────────┘  └───────────────┘│
│         │                 │          │
│         └────────┬────────┘          │
│                  │                   │
│         ┌────────▼────────┐          │
│         │  SQLite DB      │          │
│         └─────────────────┘          │
└─────────────────────────────────────┘
```

### Production Environment (Recommended)
```
┌─────────────────────────────────────────────────┐
│  CDN / Static Hosting (Vercel/Netlify)          │
│  ┌─────────────────────────────────────────┐   │
│  │  Frontend (React Build)                  │   │
│  └─────────────────────────────────────────┘   │
└────────────────┬────────────────────────────────┘
                 │ HTTPS
┌────────────────▼────────────────────────────────┐
│  Application Server (Railway/Render)            │
│  ┌─────────────────────────────────────────┐   │
│  │  Backend (Django + Gunicorn)             │   │
│  └─────────────────────────────────────────┘   │
│                 │                                │
│  ┌──────────────▼──────────────┐                │
│  │  PostgreSQL Database         │                │
│  └─────────────────────────────┘                │
│                                                  │
│  ┌─────────────────────────────┐                │
│  │  Media Files Storage         │                │
│  └─────────────────────────────┘                │
└──────────────────────────────────────────────────┘
```

## Future Enhancements (Out of Scope)

The following features are documented but not part of the current implementation:

1. **Machine Learning / Predictive Maintenance**
   - Failure prediction models
   - Anomaly detection
   - Predictive analytics

2. **Real-time Chat System**
   - Team communication
   - Work order discussions
   - File sharing in chat

3. **Mobile Application**
   - Native iOS/Android apps
   - Offline-first architecture
   - Push notifications

4. **Advanced Reporting**
   - Custom report builder
   - Scheduled report generation
   - Email report delivery

5. **Integration APIs**
   - ERP system integration
   - IoT sensor data integration
   - Third-party tool webhooks

6. **Cloud Services Integration**
   - Cloud storage (S3, GCS)
   - Cloud databases
   - Serverless functions

