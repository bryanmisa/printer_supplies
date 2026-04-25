# Project Skills

## Overview
This file defines the skills/agents available for developing the Printer Supplies Management System. Each skill represents a specialized agent for specific aspects of the project development.

## Available Skills

### 1. django-setup
**Purpose**: Initialize and configure Django project
**Capabilities**:
- Create Django project structure
- Configure settings (development/staging/production)
- Set up database connections
- Configure static files
- Environment variable setup

**Usage**: Use when starting a new Django project or making major configuration changes.

---

### 2. model-creator
**Purpose**: Create Django database models
**Capabilities**:
- Define model classes with fields
- Set up relationships (ForeignKey, ManyToMany)
- Add constraints and indexes
- Generate migrations
- Document model fields

**Usage**: Use when creating new database models or modifying existing ones.

---

### 3. crud-generator
**Purpose**: Generate CRUD views and templates
**Capabilities**:
- Create class-based or function-based views
- Generate forms
- Create Django templates
- Implement search and filtering
- Add pagination

**Usage**: Use when building standard create/read/update/delete functionality.

---

### 4. business-logic
**Purpose**: Implement business logic and constraints
**Capabilities**:
- Supply installation/disposal logic
- Stock level management
- Delivery processing
- Validation rules
- Signals and middleware

**Usage**: Use when implementing core business rules and workflows.

---

### 5. dashboard-builder
**Purpose**: Create dashboard with widgets and charts
**Capabilities**:
- Dashboard view implementation
- Widget creation (counts, alerts)
- Chart.js integration
- Real-time data updates
- Quick action links

**Usage**: Use when building the main dashboard interface.

---

### 6. reporter
**Purpose**: Build reporting system
**Capabilities**:
- Monthly consumption reports
- Inventory reports
- Replenishment reports
- PDF generation
- Email functionality

**Usage**: Use when implementing reporting and export features.

---

### 7. audit-trail
**Purpose**: Implement audit logging
**Capabilities**:
- Create audit log model
- Implement logging middleware/signals
- Audit viewing interface
- Filtering and search
- Export functionality

**Usage**: Use when adding audit trail capabilities.

---

### 8. frontend-enhancer
**Purpose**: Enhance frontend with JavaScript
**Capabilities**:
- Dependent dropdowns
- Form validation
- Dynamic updates
- AJAX interactions
- Responsive enhancements

**Usage**: Use when adding dynamic JavaScript functionality.

---

### 9. tester
**Purpose**: Write tests for the application
**Capabilities**:
- Unit tests for models
- View tests
- Integration tests
- Test fixtures
- Test coverage reports

**Usage**: Use when writing or running tests.

---

### 10. code-reviewer
**Purpose**: Review code for quality
**Capabilities**:
- PEP 8 compliance check
- Security review
- Performance analysis
- Best practices verification
- Documentation review

**Usage**: Use when reviewing code before committing or merging.

---

### 11. devops
**Purpose**: Handle deployment and DevOps
**Capabilities**:
- Production settings
- Static file configuration
- Database backup
- Environment setup
- Deployment scripts

**Usage**: Use when preparing for production deployment.

---

## Skill Development Order

When building the project, follow this order:

1. **django-setup** - Initialize project
2. **model-creator** - Create core models
3. **crud-generator** - Build CRUD for each model
4. **business-logic** - Implement business logic
5. **dashboard-builder** - Create dashboard
6. **frontend-enhancer** - Add dynamic features
7. **reporter** - Implement reports
8. **audit-trail** - Add audit logging
9. **tester** - Write tests
10. **code-reviewer** - Review code
11. **devops** - Prepare deployment

## Notes

- Each skill can be used independently for specific tasks
- Prefer class-based views for standard CRUD operations
- Keep business logic in model methods or service classes
- Use Django signals for cross-model updates
- Maintain separation of concerns between layers