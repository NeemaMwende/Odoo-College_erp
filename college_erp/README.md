# College ERP

A comprehensive Odoo 18 module for managing college education administration. This module handles student admissions, records management, and provides a complete solution for educational institution management.

## Features

### Student Management
- **Admission Tracking** - Record and manage student admission numbers and dates
- **Personal Information** - Store student first name, last name, father's name, and mother's name
- **Contact Details** - Manage email addresses and phone numbers
- **Address Management** - Complete address fields including street, street2, city, ZIP code, state, and country
- **Country Code Integration** - Automatic country code detection based on selected country

### User Interface
- **Form View** - intuitive form for entering and editing student records
- **List View** - View all students in a structured table format
- **Kanban View** - Visual kanban board for student management
- **Menu Integration** - Easy access from the Odoo application menu

## Installation

1. Place this module in your Odoo addons path:
   ```
   /path/to/your/odoo/addons/college_erp
   ```

2. Update the apps list in Odoo:
   - Go to **Apps**
   - Click on **Update Apps List**

3. Install the module:
   - Search for "College ERP"
   - Click **Install**

## Configuration

### Access Rights
The module automatically creates access rights for the `college.student` model. Make sure to assign appropriate group permissions to users who need access to student records.

### Dependencies
This module has no hard dependencies on other custom modules. It works with:
- Odoo 18.0
- PostgreSQL database

## Usage

### Creating a Student Record
1. Navigate to **College ERP** from the main menu
2. Click **Create** to add a new student
3. Fill in the required fields:
   - **Admission Number** (required) - Unique identifier for the student
   - **Admission Date** (required) - Date of admission
   - **First Name** (required) - Student's first name
   - **Last Name** (required) - Student's last name
   - **Father's Name** (required) - Father's name
   - **Mother's Name** (required) - Mother's name
   - **Contact Address** (required) - Full contact address
4. Optionally fill in additional details:
   - **Email** - Student email address
   - **Phone** - Contact phone number
   - **Street / Street 2** - Address details
   - **City** - City name
   - **ZIP** - Postal code
   - **State** - Geographic state (auto-filtered by country)
   - **Country** - Country selection
   - **Country Code** - Automatically populated based on country

### Managing Students
- **Search** - Use the search bar to find students by name, admission number, or other fields
- **Filter** - Apply filters to narrow down student records
- **Group By** - Group students by various criteria
- **Export** - Export student data to CSV/Excel

## Model Information

### college.student
Main model for storing student information.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| admission_no | Char | Yes | Unique admission number |
| admission_date | Date | Yes | Date of admission |
| first_name | Char | Yes | Student's first name |
| last_name | Char | Yes | Student's last name |
| father_name | Char | Yes | Father's name |
| mother_name | Char | Yes | Mother's name |
| contact_address | Text | Yes | Full contact address |
| street | Char | No | Street address |
| street2 | Char | No | Additional street address |
| zip | Char | No | ZIP/Postal code |
| city | Char | No | City name |
| state_id | Many2one | No | State/Province |
| country_id | Many2one | No | Country |
| country_code | Char | No | Country code (auto-calculated) |
| email | Char | No | Email address |
| phone | Char | No | Phone number |

## Development

### Module Structure
```
college_erp/
├── __init__.py           # Module initialization
├── __manifest__.py       # Module manifest
├── models/
│   ├── __init__.py
│   └── college_student.py    # Student model
├── views/
│   ├── college_student_view.xml   # Form, list, kanban views
│   └── college_erp_menus.xml      # Menu definitions
├── security/
│   └── ir.model.access.csv  # Access control lists
└── README.md            # This file
```

### Extending the Module
You can extend this module by:
- Adding new models for courses, exams, attendance, etc.
- Creating custom views and reports
- Adding automated actions and workflows

## License

This module is published under the LGPL-3 license.

## Author

Neema Mwende  
Email: neemamwende009@gmail.com  
GitHub: https://github.com/NeemaMwende

## Support

For issues or questions:
1. Check Odoo logs for error details
2. Verify the module is properly installed
3. Ensure all dependencies are met

## Version History

- **18.0.1.1** (Current)
  - Initial release
  - Student management with full address support
  - Multi-view support (form, list, kanban)
  - Access control configuration
