# File Structure Documentation

## Complete Project Structure

```
cms/                                    # Root project directory
├── .env                               # Environment variables for Node.js frontend
├── .gitignore                         # Git ignore rules for both frontend and backend
├── index.js                           # Main Express.js server file
├── package.json                       # Node.js dependencies and scripts
├── README.md                          # Project setup and usage instructions
├── DOCUMENTATION.md                   # Comprehensive project documentation
├── API_REFERENCE.md                   # Detailed API endpoint documentation
├── DEPLOYMENT_GUIDE.md                # Production deployment instructions
├── DEVELOPER_GUIDE.md                 # Development workflow and standards
├── FILE_STRUCTURE.md                  # This file - complete structure overview
│
├── screencastcms/                     # Django CMS Backend Directory
│   ├── .env                          # Django environment variables (optional)
│   ├── db.sqlite3                    # SQLite database file (development)
│   ├── manage.py                     # Django management command script
│   ├── requirements.in               # Python dependencies specification
│   │
│   ├── portfolio/                    # Custom Django app for portfolio functionality
│   │   ├── __init__.py              # Python package marker
│   │   ├── admin.py                 # Django admin interface configuration
│   │   ├── apps.py                  # Django app configuration
│   │   ├── models.py                # Database models (PersonalInfo, Project, Skill, etc.)
│   │   ├── serializers.py           # Django REST Framework serializers
│   │   ├── tests.py                 # Unit tests for portfolio app
│   │   ├── urls.py                  # URL routing for API endpoints
│   │   ├── views.py                 # API view classes and functions
│   │   │
│   │   ├── migrations/              # Database migration files
│   │   │   ├── __init__.py         # Python package marker
│   │   │   └── 0001_initial.py     # Initial database schema migration
│   │   │
│   │   └── management/              # Custom Django management commands
│   │       ├── __init__.py         # Python package marker
│   │       └── commands/           # Management command modules
│   │           └── __init__.py     # Python package marker
│   │
│   └── screencastcms/               # Django project settings directory
│       ├── __init__.py             # Python package marker
│       ├── asgi.py                 # ASGI configuration for async deployment
│       ├── settings.py             # Main Django configuration file
│       ├── urls.py                 # Root URL configuration
│       ├── wsgi.py                 # WSGI configuration for deployment
│       │
│       ├── static/                 # Django static files directory
│       │   └── (static files collected here in production)
│       │
│       └── templates/              # Django CMS templates
│           └── base.html           # Base template for Django CMS pages
│
├── views/                           # EJS Templates for Node.js Frontend
│   ├── contact-success.ejs         # Contact form success page template
│   ├── contact.ejs                 # Contact form page template
│   ├── error.ejs                   # Error page template (404, 500, etc.)
│   ├── experience.ejs              # Work experience timeline template
│   ├── index.ejs                   # Homepage template with portfolio summary
│   ├── layout.ejs                  # Base layout template (alternative structure)
│   ├── project-detail.ejs          # Individual project detail page template
│   ├── projects.ejs                # Projects listing page template
│   ├── skills.ejs                  # Skills showcase page template
│   │
│   └── partials/                   # Reusable template components
│       ├── footer.ejs             # Footer with scripts and closing HTML
│       └── header.ejs             # Header with navigation and HTML head
│
└── public/                         # Static Assets for Node.js Frontend
    ├── css/                        # Stylesheets
    │   └── style.css              # Main custom CSS file with responsive design
    │
    ├── js/                         # JavaScript files
    │   └── main.js                # Frontend JavaScript for interactions and animations
    │
    └── images/                     # Static image assets
        └── (placeholder for static images)
```

## File Descriptions

### Root Level Files

#### `.env`
**Purpose**: Environment configuration for Node.js frontend
**Contains**:
- `NODE_ENV`: Environment mode (development/production)
- `PORT`: Server port (default 3000)
- `DJANGO_API_BASE`: Django backend URL
- `SESSION_SECRET`: Session encryption key

#### `.gitignore`
**Purpose**: Specifies files and directories to ignore in version control
**Includes**:
- Node.js artifacts (`node_modules/`, `*.log`)
- Python artifacts (`__pycache__/`, `*.pyc`)
- Environment files (`.env`)
- Database files (`db.sqlite3`)
- IDE files (`.vscode/`, `.idea/`)

#### `index.js`
**Purpose**: Main Express.js application server
**Key Components**:
- Express app configuration with security middleware
- Route definitions for all portfolio pages
- API client setup using Axios for Django communication
- Error handling and template rendering
- Security features (Helmet, CORS, rate limiting)

#### `package.json`
**Purpose**: Node.js project configuration and dependency management
**Key Sections**:
- Project metadata (name, version, description)
- Scripts for development and production
- Dependencies (Express, EJS, Axios, security packages)
- Development dependencies (Nodemon)

### Django Backend Files

#### `screencastcms/manage.py`
**Purpose**: Django's command-line utility for administrative tasks
**Usage**:
- Database migrations: `python manage.py migrate`
- Development server: `python manage.py runserver`
- Create superuser: `python manage.py createsuperuser`
- Collect static files: `python manage.py collectstatic`

#### `screencastcms/requirements.in`
**Purpose**: Python dependency specification
**Key Dependencies**:
- Django CMS packages for content management
- Django REST Framework for API functionality
- Django CORS headers for cross-origin requests
- Django Filer for file management
- Pillow for image processing

#### `screencastcms/screencastcms/settings.py`
**Purpose**: Main Django configuration file
**Key Configurations**:
- Database settings (SQLite for development)
- Installed apps including Django CMS and portfolio app
- Middleware configuration including CORS
- REST Framework settings
- Static and media file handling
- Security settings

#### `screencastcms/screencastcms/urls.py`
**Purpose**: Root URL configuration for Django project
**URL Patterns**:
- Django admin interface
- Django CMS pages
- Portfolio API endpoints
- File management (Filer)
- Internationalization support

### Portfolio App Files

#### `screencastcms/portfolio/models.py`
**Purpose**: Database schema definition
**Models**:
- `PersonalInfo`: Personal and professional information
- `Skill`: Technical and soft skills with proficiency levels
- `Experience`: Work experience and employment history
- `Project`: Portfolio projects with technologies and images
- `ProjectImage`: Additional images for projects
- `ContactMessage`: Contact form submissions

#### `screencastcms/portfolio/serializers.py`
**Purpose**: Django REST Framework serializers for API responses
**Key Features**:
- Converts Django models to JSON format
- Handles image URL generation with request context
- Nested serialization for related models
- Custom fields for computed properties

#### `screencastcms/portfolio/views.py`
**Purpose**: API view classes and functions
**Views**:
- List views for all model types with filtering
- Detail view for individual projects
- Contact message creation view
- Portfolio summary view for homepage data

#### `screencastcms/portfolio/admin.py`
**Purpose**: Django admin interface configuration
**Features**:
- Custom admin classes for all models
- Inline editing for related models
- List displays with filtering and search
- Horizontal filter widgets for many-to-many relationships

#### `screencastcms/portfolio/urls.py`
**Purpose**: URL routing for portfolio API endpoints
**Endpoints**:
- `/api/personal-info/`: Personal information
- `/api/skills/`: Skills with filtering
- `/api/experience/`: Work experience
- `/api/projects/`: Projects with filtering
- `/api/projects/{id}/`: Project details
- `/api/contact/`: Contact form submission
- `/api/summary/`: Portfolio summary data

### Frontend Template Files

#### `views/index.ejs`
**Purpose**: Homepage template displaying portfolio summary
**Sections**:
- Hero section with personal information
- Featured skills grid
- Featured projects showcase
- Recent experience timeline
- Responsive design with Bootstrap classes

#### `views/projects.ejs`
**Purpose**: Projects listing page template
**Features**:
- Project cards with filtering capabilities
- Technology badges and status indicators
- Image galleries and external links
- Responsive grid layout

#### `views/project-detail.ejs`
**Purpose**: Individual project detail page template
**Components**:
- Detailed project information and description
- Image gallery with captions
- Technology stack display
- External links (GitHub, live demo)
- Breadcrumb navigation

#### `views/experience.ejs`
**Purpose**: Work experience timeline template
**Features**:
- Timeline layout with company logos
- Technology tags for each position
- Responsive design for mobile devices
- Current position indicators

#### `views/skills.ejs`
**Purpose**: Skills showcase page template
**Organization**:
- Categorized skill display (technical, soft, languages, tools)
- Proficiency level indicators with star ratings
- Skill icons and descriptions
- Featured skills section

#### `views/contact.ejs`
**Purpose**: Contact form page template
**Components**:
- Contact form with validation
- Personal contact information display
- Social media links
- Form submission handling

#### `views/partials/header.ejs`
**Purpose**: Header partial with navigation and HTML head
**Includes**:
- HTML5 document structure
- Bootstrap 5 CSS and Font Awesome icons
- Google Fonts (Inter typography)
- Responsive navigation bar
- Meta tags and SEO elements

#### `views/partials/footer.ejs`
**Purpose**: Footer partial with scripts and closing HTML
**Includes**:
- Bootstrap 5 JavaScript bundle
- Custom JavaScript inclusion
- Footer content with copyright
- Closing HTML tags

### Static Asset Files

#### `public/css/style.css`
**Purpose**: Main stylesheet with custom styling and responsive design
**Features**:
- CSS custom properties for consistent theming
- Bootstrap 5 integration with custom overrides
- Responsive design with mobile-first approach
- Component-specific styling (cards, timeline, navigation)
- Animation and transition effects
- Professional color scheme and typography

#### `public/js/main.js`
**Purpose**: Frontend JavaScript for interactions and enhancements
**Functionality**:
- Navigation enhancements and active link highlighting
- Contact form validation and submission handling
- Intersection Observer API for scroll animations
- Image lazy loading for performance optimization
- Smooth scrolling and back-to-top functionality
- Error handling for missing images
- Utility functions for common operations

### Database Migration Files

#### `screencastcms/portfolio/migrations/0001_initial.py`
**Purpose**: Initial database schema migration
**Creates**:
- All portfolio model tables
- Foreign key relationships
- Index definitions
- Field constraints and validations

### Documentation Files

#### `README.md`
**Purpose**: Project overview and quick setup instructions
**Sections**:
- Feature overview
- Installation steps
- Running instructions
- Basic configuration
- Technology stack

#### `DOCUMENTATION.md`
**Purpose**: Comprehensive project documentation
**Covers**:
- Complete project structure
- Architecture overview
- File-by-file descriptions
- API documentation
- Database models
- Configuration details

#### `API_REFERENCE.md`
**Purpose**: Detailed API endpoint documentation
**Includes**:
- Endpoint descriptions with examples
- Request/response formats
- Query parameters
- Error handling
- Authentication details

#### `DEPLOYMENT_GUIDE.md`
**Purpose**: Production deployment instructions
**Covers**:
- Environment setup
- Security configuration
- Performance optimization
- Cloud deployment options
- Monitoring and logging

#### `DEVELOPER_GUIDE.md`
**Purpose**: Development workflow and coding standards
**Includes**:
- Development environment setup
- Coding conventions
- Testing guidelines
- Debugging procedures
- Contribution process

## File Relationships and Dependencies

### Frontend Dependencies
```
index.js
├── views/*.ejs (EJS templates)
├── public/css/style.css (Styling)
├── public/js/main.js (Client-side JavaScript)
└── Django API (HTTP requests via Axios)
```

### Backend Dependencies
```
screencastcms/settings.py
├── portfolio/models.py (Database schema)
├── portfolio/serializers.py (API serialization)
├── portfolio/views.py (API endpoints)
├── portfolio/admin.py (Admin interface)
└── portfolio/urls.py (URL routing)
```

### Template Hierarchy
```
views/partials/header.ejs
├── views/index.ejs
├── views/projects.ejs
├── views/project-detail.ejs
├── views/experience.ejs
├── views/skills.ejs
├── views/contact.ejs
├── views/contact-success.ejs
└── views/error.ejs
views/partials/footer.ejs
```

### Static Asset Loading
```
views/partials/header.ejs
├── Bootstrap 5 CSS (CDN)
├── Font Awesome (CDN)
├── Google Fonts (CDN)
└── public/css/style.css (Custom styles)

views/partials/footer.ejs
├── Bootstrap 5 JS (CDN)
└── public/js/main.js (Custom JavaScript)
```

This file structure documentation provides a complete overview of every file and directory in the portfolio website project, explaining their purposes, relationships, and key components.
