# Changelog

All notable changes to the SuppliesPro project will be documented in this file.

## [Unreleased]

### Fixed
- Added missing password fields (password1, password2) to user creation form template
- Fixed user creation not working due to missing password fields in template
- Fixed `is_active` field not being saved in `user_create` and `user_edit` views
- Added non-field error display to user form template
- Updated text color palette variables for better contrast and readability:
  - `--text-1`: changed from `#f8fafc` to `#ffffff` (pure white)
  - `--text-2`: changed from `#cbd5e1` to `#f1f5f9` (much whiter)
  - `--text-3`: changed from `#94a3b8` to `#e2e8f0` (much whiter)
- Fixed gray password labels by adding `.form-check-label` and `h6` to CSS form labels rule
- Added `text-white` class to Password and Permissions headings in user form

---

## [2026-04-29] - Version 0.1.0

### Changed
- Updated virtual environment dependencies and package files (commit: 704a3ad)

---

## [2026-04-27] - UI and Access Control Updates

### Style
- Updated text color palette variables for better contrast (commit: 69f8f06)

### Refactored
- Removed staff role restrictions and added department, location, and custodian model support to inventory views (commit: bebfbaa)
- Removed staff role restrictions, updated UI forms, and adjusted color palette variables (commit: 0e78ec1)

### Features
- Implemented staff role-based access control and restricted CRUD operations for supplies, suppliers, and printers (commit: 57be41b)
- Added the dist folder for production builds (commit: 3f713ef)

---

## [2026-04-26] - Cross-Platform and Navigation Updates

### Features
- Added collapsible navigation sections and updated production deployment scripts (commit: 4348fed)
- Added cross-platform production support with Waitress and restructured deployment scripts (commit: 893dbd3)
- Supported cross-platform deployment by restructuring scripts for Windows and Linux and updating dependency requirements (commit: 0cc724b)

---

## [2026-04-25] - Initial Development

### Features
- Initialized SuppliesPro printer inventory management system with RBAC and reporting modules (commit: 52859a6)
- Added printer model list view template (commit: 63d6843)

### Refactored
- Updated base and inventory templates and removed stale virtual environment cache files (commit: 1987777)

### Chore
- Updated project dependencies and initialized inventory management command structure (commit: 8d5e885)

### Security
- Restricted staff data access, implemented admin password reset, and updated configuration settings (commit: 6304fc3)

---

## [2026-04-25] - Project Initialization

### Added
- Initial project setup with Django framework
- User authentication with custom User model (AbstractUser)
- Role-based access control (RBAC) system with admin and manager roles
- Inventory management for supplies, printers, and printer models
- Supplier management module
- Delivery and installation tracking
- Department, location, and custodian management
- Reporting modules (inventory status, replenishment, consumption)
- Audit trail logging
- Database backup functionality
- Dark theme UI with Inter font family
- Responsive design with collapsible sidebar navigation
- Select2 integration for enhanced dropdowns
- Bootstrap 5 integration with custom dark theme
