# Master Plan: Printer Supplies Management System

## 1. Project Overview
Build a web-based Printer Supplies Management System using Django (Backend), Bootstrap (Frontend UI), and JavaScript (Dynamic UI, no Redis). The system manages inventory, suppliers, printers, supply lifecycle, and reporting with automated replenishment.

## 2. Technical Architecture

### 2.1 Backend (Django)
- **Models**: Supply, PrinterModel, Printer, Supplier, Delivery, DeliveryItem, SupplyInstallation, AuditLog, User (custom or extended)
- **Views**: Function-based or class-based views for CRUD operations and business logic
- **URLs**: RESTful URL patterns for all resources
- **Templates**: Bootstrap-based HTML templates with consistent layout
- **Static Files**: CSS, JavaScript, images organized in Django static files structure
- **Forms**: Django forms for validation and rendering
- **Middleware**: Custom middleware for audit logging if needed
- **Settings**: Environment-based configuration (development, staging, production)

### 2.2 Frontend
- **Bootstrap 5**: Responsive grid system, components, and utilities
- **Custom CSS**: Minimal overrides for branding and specific UI needs
- **JavaScript**: Vanilla JS with Fetch API for dynamic interactions
  - Dependent dropdowns (Printer → Compatible Supplies)
  - Form validation and prevention of invalid actions
  - Dynamic updates without page reloads (e.g., stock counts)
  - Chart.js integration for dashboard graphs
- **Templates**: Base template with sidebar navigation, content blocks, and flash messages
- **Important**: The UI/ UX should have a modern look and feel.

### 2.3 Database
- **Primary**: PostgreSQL (recommended for production) or SQLite (development)
- **Relationships**: 
  - Supply ↔ PrinterModel (ManyToMany)
  - Supply ↔ Supplier (ManyToMany)
  - Printer → PrinterModel (ForeignKey)
  - Printer → User (ForeignKey for custodian)
  - Delivery → Supplier (ForeignKey)
  - DeliveryItem → Delivery and Supply (ForeignKeys)
  - SupplyInstallation → Printer, Supply, User (ForeignKeys)
  - AuditLog → User (ForeignKey), GenericForeignKey for any model
- **Indexes**: On frequently queried fields (status flags, dates, foreign keys)
- **Constraints**: Check constraints for stock levels, unique constraints where applicable

### 2.4 Development Tools
- **Version Control**: Git with feature branching strategy
- **Package Management**: pip for Python dependencies, npm/yarn for JS (if needed for Chart.js)
- **Testing**: Django's built-in test framework, pytest for advanced testing
- **Code Quality**: flake8 for linting, black for formatting
- **Documentation**: inline docstrings, external API documentation

## 3. Development Process

### 3.1 Methodology
- **Agile-inspired**: 2-week sprints with regular reviews
- **Definition of Done**: Code written, tested, documented, and reviewed
- **Code Reviews**: Mandatory pull request reviews before merging
- **Continuous Integration**: Automated tests on every push (to be set up later)

### 3.2 Coding Standards
- **Python**: PEP 8 compliance with docstrings for all functions/classes
- **JavaScript**: ES6+ standards, consistent naming (camelCase)
- **HTML/Django Templates**: Proper indentation, semantic elements
- **CSS**: BEM naming convention where applicable
- **Commit Messages**: Conventional Commits format (feat:, fix:, docs:, etc.)

### 3.3 Testing Strategy
- **Unit Tests**: Models, forms, views, utility functions
- **Integration Tests**: Critical workflows (installation, delivery, replenishment)
- **Test Coverage**: Minimum 80% coverage for critical paths
- **Test Data**: Factories or fixtures for consistent test data
- **Browser Testing**: Manual testing of key user flows on Chrome/Firefox

### 3.4 Deployment Preparation
- **Environment Variables**: Using python-decouple or similar for settings
- **Static Files**: WhiteNoise for serving static files in production
- **Media Files**: Cloud storage (AWS S3) for uploaded documents (if needed later)
- **Database Migrations**: Automated backup strategy before migrations
- **Production Settings**: DEBUG=False, allowed hosts, secure headers, CSRF trusted origins

## 4. Feature Breakdown (User Stories)

### 4.1 Authentication
- As a user, I can log in with username and password
- As a user, I can log out securely
- As an admin, I can manage user roles (Admin/Staff)
- As a user, I see appropriate menu items based on my role

### 4.2 Inventory Management
- As a user, I can view all supplies with current stock levels
- As a user, I can add/edit/delete supplies (with appropriate permissions)
- As a user, I can see supply status indicators (Out of Stock, Low Stock, Normal, Overstock)
- As a user, I can search and filter supplies by name, status, or associated printers/suppliers

### 4.3 Printer Management
- As a user, I can view all printers with their current status
- As a user, I can add/edit/delete printers
- As a user, I can assign a custodian to a printer
- As a user, I can see what supply is currently installed in a printer (if any)

### 4.4 Supply Installation Tracking
- As a user, I can install a supply in a printer (if compatible and no active installation)
- As a user, I can dispose of an installed supply from a printer
- As a user, I can view installation history for a printer or supply
- System prevents installing a supply if another is actively installed in the same printer
- System prevents disposing of a supply that is not currently installed

### 4.5 Supplier Management
- As a user, I can view all suppliers with contact information
- As a user, I can add/edit/delete suppliers
- As a user, I can see which supplies are provided by each supplier

### 4.6 Delivery Management
- As a user, I can record a delivery from a supplier
- As a user, I can add items to a delivery (supply and quantity)
- System automatically increases stock levels when a delivery is saved
- As a user, I can view delivery history and details

### 4.7 Reporting System
#### Monthly Consumption
- As a manager, I can view a line graph showing supply consumption by month and custodian
- As a manager, I can filter the graph by date range or custodian

#### Inventory Report
- As a user, I can view a summary of total supplies categorized by stock status
- As a user, I can see lists of out of stock, low stock, and overstock supplies

#### Replenishment Report
- As a user, I can generate a replenishment report showing:
  - Out of stock supplies (priority)
  - Low stock supplies
  - Suggested reorder quantities based on thresholds and usage patterns
- As a user, I can export the replenishment report as PDF
- As a user, I can email the replenishment report to suppliers

### 4.8 Dashboard
- As a user, I see a dashboard upon login with widgets:
  - Total supplies count
  - Currently installed supplies count
  - Out of stock alerts (highlighted in red)
  - Low stock alerts (highlighted in orange)
  - Monthly consumption graph (Chart.js)
  - Quick links to frequently used sections

### 4.9 Audit Trail
- As an auditor, I can view a log of all significant actions:
  - Create/update/delete of supplies, printers, suppliers
  - Supply installation and disposal events
  - Delivery recordings
- As an auditor, I can see who performed each action and when
- As an auditor, I can filter audit logs by user, action type, or date range

### 4.10 UI/UX
- As a user, I can navigate the system using a consistent sidebar menu
- As a user, I experience a responsive layout that works on mobile and desktop
- As a user, I receive clear feedback for successful actions and errors
- As a user, I see validation errors immediately when entering invalid data

## 5. Timeline and Milestones

### Phase 1: Core Setup (Week 1)
- [ ] Django project initialization and configuration
- [ ] Database setup and initial migrations
- [ ] Base template with Bootstrap and sidebar navigation
- [ ] User authentication system (login/logout)
- [ ] Deliverable: Functional login page and base layout

### Phase 2: Core Models and CRUD (Weeks 2-3)
- [ ] Supply model and CRUD views/templates
- [ ] PrinterModel and Printer models with CRUD
- [ ] Supplier model and CRUD
- [ ] Delivery and DeliveryItem models with basic CRUD
- [ ] Deliverable: Basic inventory management with supply, printer, and supplier CRUD

### Phase 3: Business Logic Implementation (Weeks 4-5)
- [ ] Supply installation tracking model and constraints
- [ ] Stock update logic on installation/disposal
- [ ] Delivery processing with automatic stock updates
- [ ] Validation to prevent invalid installations
- [ ] Deliverable: Working installation/disposal system with accurate stock levels

### Phase 4: Dashboard and UI Enhancements (Week 6)
- [ ] Dashboard widgets implementation
- [ ] JavaScript for dynamic dropdowns and form validation
- [ ] Chart.js integration for consumption graph
- [ ] Responsive testing and adjustments
- [ ] Deliverable: Interactive dashboard with real-time data

### Phase 5: Reporting System (Week 7)
- [ ] Monthly consumption report with Chart.js
- [ ] Inventory report with stock categorization
- [ ] Replenishment report with PDF generation
- [ ] Email functionality for replenishment reports
- [ ] Deliverable: Complete reporting suite with export capabilities

### Phase 6: Audit Trail and Export Features (Week 8)
- [ ] Audit log model and middleware/signals
- [ ] Audit log viewing interface with filtering
- [ ] CSV export for key reports
- [ ] Final UI polishing and accessibility checks
- [ ] Deliverable: Complete audit trail and export functionality

### Phase 7: Testing and Refinement (Week 9)
- [ ] Comprehensive unit and integration testing
- [ ] User acceptance testing with sample data
- [ ] Performance optimization and query optimization
- [ ] Security review and hardening
- [ ] Deliverable: Tested, secure, and performant system

### Phase 8: Deployment Preparation (Week 10)
- [ ] Production settings configuration
- [ ] Static and media files setup for production
- [ ] Documentation of deployment process
- [ ] Final system review against requirements
- [ ] Deliverable: Production-ready application package

## 6. Risk Management

### Technical Risks
- **Risk**: Complex business logic leading to bugs
  **Mitigation**: Strict TDD approach, code reviews, and comprehensive testing
- **Risk**: Performance issues with large datasets
  **Mitigation**: Proper indexing, query optimization, and pagination
- **Risk**: Frontend-backend integration issues
  **Mitigation**: Clear API contracts, regular integration testing

### Schedule Risks
- **Risk**: Underestimation of JavaScript complexity
  **Mitigation**: Timeboxing frontend tasks, starting with basic functionality
- **Risk**: Dependency delays (third-party packages)
  **Mitigation**: Early identification of dependencies, having fallback options

### Mitigation Strategies
- Weekly progress reviews and adjustment of plans
- Maintaining a buffer in the schedule for unexpected issues
- Regular communication between team members (if applicable)
- Prioritizing core functionality over nice-to-have features

## 7. Maintenance and Future Enhancements

### 7.1 Ongoing Maintenance
- Regular dependency updates (monthly)
- Periodic security audits
- Backup verification and disaster recovery drills
- Log monitoring and error tracking

### 7.2 Future Enhancements
- **Mobile Application**: React Native or Flutter app for barcode scanning
- **Advanced Analytics**: Machine learning for predictive restocking
- **Integration Capabilities**: REST API for ERP/accounting system integration
- **Multi-warehouse Support**: Managing supplies across multiple locations
- **Supplier Portal**: Allow suppliers to view delivery schedules and confirm shipments
- **Mobile Notifications**: Push alerts for critical stock levels
- **Role-Based Dashboards**: Customized views for different user types (admin, staff, manager)

## 8. Success Criteria

### Functional
- All core workflows (installation, delivery, reporting) work correctly
- Stock levels remain accurate under all operations
- System prevents all invalid business operations (double installation, etc.)
- Reports generate accurate data that matches source records

### Non-Functional
- Page load times under 3 seconds for dashboard
- System supports 50+ concurrent users
- 99.9% uptime in production environment
- Data recoverable within RPO/RTO targets
- Compatible with Chrome, Firefox, Safari, and Edge browsers

## 9. Appendices

### 9.1 Glossary
- **Custodian**: Person responsible for a specific printer
- **Threshold**: Minimum stock level before low stock alert
- **Max Threshold**: Optional maximum stock level for overstock identification
- **Supply Installation**: Record of a supply being installed in a printer
- **Delivery**: Record of supplies received from a supplier

### 9.2 Open Questions
- [ ] Should we use Django's built-in User model or create a custom one?
- [ ] What charting library should we use besides Chart.js for reports?
- [ ] Should we implement role-based permissions with Django Groups or custom solution?
- [ ] What PDF generation library should we use (ReportLab, WeasyPrint, etc.)?
- [ ] How should we handle email sending in development vs production?

## 10. Approval
This master plan represents the agreed-upon approach for building the Printer Supplies Management System. Any significant changes to scope, timeline, or technical approach should be reviewed and approved through the established change control process.

Prepared by: Development Team
Date: 2026-04-20
Version: 1.0