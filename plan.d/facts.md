# Printer Supplies Management System - Project Facts

## Project Overview
A web-based Printer Supplies Management System built with Django (Backend), Bootstrap (Frontend UI), and JavaScript. The system manages inventory, suppliers, printers, supply lifecycle tracking, and reporting with automated replenishment alerts.

## Technical Architecture

### Backend Stack
- **Framework**: Django (function-based or class-based views)
- **Python**: 3.x (latest stable)
- **Settings**: Environment-based configuration (dev/staging/prod)

### Frontend Stack
- **UI Framework**: Bootstrap 5 (responsive grid, components)
- **JavaScript**: Vanilla JS with Fetch API
- **Charts**: Chart.js for dashboard graphs
- **Approach**: No heavy frontend frameworks

### Database
- **Production**: PostgreSQL
- **Development**: SQLite
- **ORM**: Django ORM

### Key Dependencies
- `django` - Framework
- `psycopg2-binary` - PostgreSQL adapter
- `python-decouple` - Environment configuration
- `whitenoise` - Static file serving
- `chart.js` - Data visualization
- `reportlab` or `weasyprint` - PDF generation

## Core Features

### 1. Authentication & Authorization
- Username/password login
- Role-based permissions (Admin/Staff)
- Secure logout

### 2. Inventory Management
- CRUD operations for supplies
- Stock level tracking (Out of Stock, Low Stock, Normal, Overstock)
- Search and filtering
- Status indicators

### 3. Printer Management
- CRUD for printers and printer models
- Custodian assignment
- Current supply tracking

### 4. Supplier Management
- CRUD for suppliers with contact info
- Supply-supplier relationships (ManyToMany)

### 5. Supply Installation Tracking
- Install supplies in compatible printers
- Dispose of installed supplies
- Installation history
- Business rule enforcement (prevent double installation)

### 6. Delivery Management
- Record deliveries from suppliers
- Add multiple items per delivery
- Automatic stock level updates on delivery save
- Delivery history

### 7. Dashboard
- Total supplies count
- Installed supplies count
- Out of stock alerts (red)
- Low stock alerts (orange)
- Monthly consumption graph (Chart.js)
- Quick links

### 8. Reporting System
- Monthly consumption line graph (filterable by date/custodian)
- Inventory summary by stock status
- Replenishment report with suggested quantities
- PDF export capability
- Email to suppliers

### 9. Audit Trail
- Log all create/update/delete actions
- Log installation/disposal events
- Log deliveries
- Filter by user, action type, date range

## Database Models

### Supply
```
- name: CharField
- sku: CharField (unique)
- description: TextField
- printer_models: ManyToManyField(PrinterModel)
- suppliers: ManyToManyField(Supplier)
- current_stock: IntegerField
- low_stock_threshold: IntegerField
- max_stock_threshold: IntegerField (optional)
- status: CharField (computed)
```

### PrinterModel
```
- name: CharField
- manufacturer: CharField
- description: TextField
```

### Printer
```
- name: CharField
- printer_model: ForeignKey(PrinterModel)
- serial_number: CharField (unique)
- custodian: ForeignKey(User)
- status: CharField
- location: CharField
```

### Supplier
```
- name: CharField
- contact_name: CharField
- email: EmailField
- phone: CharField
- address: TextField
```

### Delivery
```
- supplier: ForeignKey(Supplier)
- delivery_date: DateField
- notes: TextField
- created_by: ForeignKey(User)
- created_at: DateTimeField
```

### DeliveryItem
```
- delivery: ForeignKey(Delivery)
- supply: ForeignKey(Supply)
- quantity: IntegerField
```

### SupplyInstallation
```
- printer: ForeignKey(Printer)
- supply: ForeignKey(Supply)
- installed_by: ForeignKey(User)
- installed_at: DateTimeField
- disposed_at: DateTimeField (nullable)
- is_active: BooleanField
```

### AuditLog
```
- user: ForeignKey(User)
- action: CharField
- content_type: ForeignKey(ContentType)
- object_id: PositiveIntegerField
- object_repr: CharField
- timestamp: DateTimeField
- changes: TextField (JSON)
```

## Development Process

### Methodology
- Agile-inspired 2-week sprints
- Feature branching with git
- Unit and integration testing
- Code reviews (mandatory)

### Code Standards
- Python: PEP 8 with docstrings
- JavaScript: ES6+ (camelCase)
- HTML/Django: Semantic elements, proper indentation
- CSS: BEM naming convention
- Commits: Conventional Commits format

### Testing Strategy
- Django test framework / pytest
- Minimum 80% coverage for critical paths
- Test factories or fixtures
- Browser testing on Chrome/Firefox

### Deployment Preparation
- Environment variables via python-decouple
- WhiteNoise for static files
- DEBUG=False in production
- Allowed hosts configuration

## Risk Considerations

### Technical Risks
- Complex business logic causing bugs (mitigation: TDD, code reviews)
- Performance with large datasets (mitigation: indexing, query optimization)
- Frontend-backend integration (mitigation: clear API contracts)

### Schedule Risks
- JavaScript complexity underestimated (mitigation: timeboxing)
- Third-party dependency delays (mitigation: early identification)

## Success Criteria

### Functional
- All core workflows work correctly
- Stock levels accurate under all operations
- Invalid business operations prevented
- Reports match source data

### Non-Functional
- Page load under 3 seconds
- Support 50+ concurrent users
- Compatible with major browsers

## Timeline (10 Weeks)

### Phase 1 (Week 1): Core Setup
- Django project init
- Database setup
- Base template with Bootstrap/sidebar
- Authentication system

### Phase 2 (Weeks 2-3): Core Models and CRUD
- Supply CRUD
- Printer/PrinterModel CRUD
- Supplier CRUD
- Delivery/DeliveryItem CRUD

### Phase 3 (Weeks 4-5): Business Logic
- Supply installation tracking
- Stock update logic
- Delivery processing
- Validation rules

### Phase 4 (Week 6): Dashboard & UI
- Dashboard widgets
- JavaScript dynamic features
- Chart.js integration
- Responsive layout

### Phase 5 (Week 7): Reporting
- Monthly consumption report
- Inventory report
- Replenishment report
- PDF/Email export

### Phase 6 (Week 8): Audit & Export
- Audit log model
- Audit viewing interface
- CSV export
- UI polish

### Phase 7 (Week 9): Testing
- Unit/integration tests
- User acceptance testing
- Performance optimization
- Security review

### Phase 8 (Week 10): Deployment
- Production settings
- Static files setup
- Documentation
- Final review