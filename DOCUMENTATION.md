# Portfolio Website Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Project Structure](#project-structure)
3. [Architecture Overview](#architecture-overview)
4. [Backend Documentation (Django CMS)](#backend-documentation)
5. [Frontend Documentation (Node.js)](#frontend-documentation)
6. [API Documentation](#api-documentation)
7. [Database Models](#database-models)
8. [Configuration Files](#configuration-files)
9. [Templates and Static Files](#templates-and-static-files)
10. [Setup and Deployment](#setup-and-deployment)

## Project Overview

This is a modern portfolio website built with a decoupled architecture:
- **Frontend**: Node.js with Express.js server serving dynamic EJS templates
- **Backend**: Django CMS with REST API for content management
- **Database**: SQLite (development) / PostgreSQL (production)
- **Styling**: Bootstrap 5 with custom CSS
- **Features**: Responsive design, content management, contact forms, project showcase

### Key Features
- Dynamic content management through Django CMS admin
- Responsive portfolio sections (projects, experience, skills, contact)
- REST API integration between frontend and backend
- Professional UI with Bootstrap 5 and custom styling
- Image management with Django Filer
- Contact form with message storage
- SEO-friendly structure

## Project Structure

```
cms/
├── screencastcms/                    # Django CMS Backend
│   ├── portfolio/                    # Portfolio Django App
│   │   ├── migrations/               # Database migrations
│   │   │   ├── __init__.py
│   │   │   └── 0001_initial.py      # Initial portfolio models migration
│   │   ├── management/               # Django management commands
│   │   │   ├── __init__.py
│   │   │   └── commands/
│   │   │       └── __init__.py
│   │   ├── __init__.py
│   │   ├── admin.py                 # Django admin configuration
│   │   ├── apps.py                  # App configuration
│   │   ├── models.py                # Database models
│   │   ├── serializers.py           # DRF serializers
│   │   ├── tests.py                 # Unit tests
│   │   ├── urls.py                  # API URL patterns
│   │   └── views.py                 # API views
│   ├── screencastcms/               # Django Project Settings
│   │   ├── __init__.py
│   │   ├── asgi.py                  # ASGI configuration
│   │   ├── settings.py              # Django settings
│   │   ├── static/                  # Django static files
│   │   ├── templates/               # Django templates
│   │   │   └── base.html           # Base CMS template
│   │   ├── urls.py                  # Main URL configuration
│   │   └── wsgi.py                  # WSGI configuration
│   ├── db.sqlite3                   # SQLite database
│   ├── manage.py                    # Django management script
│   └── requirements.in              # Python dependencies
├── views/                           # EJS Templates (Node.js Frontend)
│   ├── partials/                    # Reusable template components
│   │   ├── header.ejs              # Header with navigation
│   │   └── footer.ejs              # Footer with scripts
│   ├── contact-success.ejs         # Contact form success page
│   ├── contact.ejs                 # Contact form page
│   ├── error.ejs                   # Error page template
│   ├── experience.ejs              # Work experience page
│   ├── index.ejs                   # Homepage template
│   ├── layout.ejs                  # Base layout (unused)
│   ├── project-detail.ejs          # Individual project page
│   ├── projects.ejs                # Projects listing page
│   └── skills.ejs                  # Skills showcase page
├── public/                          # Static Assets (Node.js Frontend)
│   ├── css/
│   │   └── style.css               # Custom CSS styles
│   ├── js/
│   │   └── main.js                 # Frontend JavaScript
│   └── images/                     # Image assets directory
├── .env                            # Environment variables
├── .gitignore                      # Git ignore rules
├── index.js                        # Node.js Express server
├── package.json                    # Node.js dependencies and scripts
└── README.md                       # Project setup instructions
```

## Architecture Overview

### System Architecture

```
┌─────────────────┐    HTTP/API     ┌──────────────────┐
│   Node.js       │ ◄──────────────► │   Django CMS     │
│   Frontend      │    Requests     │   Backend        │
│   (Port 3000)   │                 │   (Port 8000)    │
└─────────────────┘                 └──────────────────┘
         │                                     │
         │                                     │
         ▼                                     ▼
┌─────────────────┐                 ┌──────────────────┐
│   EJS Templates │                 │   SQLite/        │
│   Bootstrap UI  │                 │   PostgreSQL     │
│   Static Assets │                 │   Database       │
└─────────────────┘                 └──────────────────┘
```

### Data Flow

1. **User Request**: Browser requests page from Node.js server (port 3000)
2. **API Call**: Node.js server makes HTTP request to Django API (port 8000)
3. **Data Processing**: Django processes request, queries database, returns JSON
4. **Template Rendering**: Node.js receives data and renders EJS template
5. **Response**: Rendered HTML sent to browser with Bootstrap styling

### Communication Protocol

- **Frontend to Backend**: HTTP REST API calls using Axios
- **Data Format**: JSON for all API communications
- **Authentication**: Currently open API (can be secured with tokens)
- **CORS**: Configured to allow cross-origin requests from Node.js frontend

## Backend Documentation (Django CMS)

### Django Apps Structure

#### Core Django CMS Apps
- `cms`: Main CMS functionality
- `menus`: Navigation management
- `filer`: File and image management
- `djangocms_text`: Rich text editing
- `djangocms_frontend`: Bootstrap components

#### Custom Portfolio App
Located in `screencastcms/portfolio/`, this app handles all portfolio-specific functionality.

### Key Backend Files

#### `screencastcms/settings.py`
**Purpose**: Main Django configuration file
**Key Configurations**:
- Database settings (SQLite for development)
- Installed apps including Django CMS and custom portfolio app
- REST Framework configuration
- CORS settings for frontend integration
- Media and static file handling
- Internationalization settings

#### `portfolio/models.py`
**Purpose**: Defines database schema for portfolio content
**Models**:
- `PersonalInfo`: Personal/professional information
- `Skill`: Technical and soft skills with proficiency levels
- `Experience`: Work experience and employment history
- `Project`: Portfolio projects with technologies and images
- `ProjectImage`: Additional images for projects
- `ContactMessage`: Contact form submissions

#### `portfolio/serializers.py`
**Purpose**: Django REST Framework serializers for API responses
**Key Features**:
- Converts Django model instances to JSON
- Handles image URL generation with request context
- Nested serialization for related models (technologies, images)
- Custom fields for display values and computed properties

#### `portfolio/views.py`
**Purpose**: API view classes and functions
**Views**:
- `PersonalInfoListView`: Get personal information
- `SkillListView`: Get skills with filtering options
- `ExperienceListView`: Get work experience
- `ProjectListView`: Get projects with filtering
- `ProjectDetailView`: Get individual project details
- `ContactMessageCreateView`: Handle contact form submissions
- `portfolio_summary`: Combined summary data for homepage

#### `portfolio/admin.py`
**Purpose**: Django admin interface configuration
**Features**:
- Custom admin classes for all models
- Inline editing for project images
- List displays with filtering and search
- Horizontal filter widgets for many-to-many relationships

### Database Models Relationships

```
PersonalInfo (1:1 with User)
    │
    └── No direct relationships

Skill (Many-to-Many with Project and Experience)
    ├── Project.technologies ──► Skill
    └── Experience.technologies ──► Skill

Project (One-to-Many with ProjectImage)
    ├── ProjectImage.project ──► Project
    └── Project.technologies ──► Skill (M2M)

Experience
    └── Experience.technologies ──► Skill (M2M)

ContactMessage
    └── No relationships (standalone)
```

## Frontend Documentation (Node.js)

### Express.js Server Structure

#### `index.js`
**Purpose**: Main Express.js application server
**Key Components**:
- Express app configuration with security middleware
- Route definitions for all portfolio pages
- API client setup using Axios
- Error handling for API failures
- Template rendering with EJS

**Dependencies**:
- `express`: Web framework
- `axios`: HTTP client for API calls
- `helmet`: Security middleware
- `cors`: Cross-origin resource sharing
- `morgan`: HTTP request logging
- `express-rate-limit`: Rate limiting protection

**Routes**:
- `GET /`: Homepage with portfolio summary
- `GET /projects`: Projects listing page
- `GET /projects/:id`: Individual project details
- `GET /experience`: Work experience page
- `GET /skills`: Skills showcase page
- `GET /contact`: Contact form page
- `POST /contact`: Contact form submission

#### API Client Configuration
```javascript
const apiClient = axios.create({
    baseURL: DJANGO_API_BASE,
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
    }
});
```

### Security Features

#### Helmet.js Configuration
- Content Security Policy (CSP)
- XSS Protection
- Frame options
- HSTS headers

#### Rate Limiting
- 100 requests per 15-minute window per IP
- Prevents abuse and DoS attacks

#### CORS Configuration
- Allows requests from Django backend
- Configurable origins for different environments

## API Documentation

### Base URL
- Development: `http://localhost:8000/portfolio/api/`
- Production: `https://yourdomain.com/portfolio/api/`

### Endpoints

#### GET `/personal-info/`
**Purpose**: Retrieve personal/professional information
**Response**:
```json
[{
    "id": 1,
    "name": "John Doe",
    "title": "Full Stack Developer",
    "bio": "Passionate developer with 5+ years experience...",
    "email": "john@example.com",
    "phone": "+1234567890",
    "location": "San Francisco, CA",
    "linkedin_url": "https://linkedin.com/in/johndoe",
    "github_url": "https://github.com/johndoe",
    "website_url": "https://johndoe.com",
    "profile_image_url": "http://localhost:8000/media/profile.jpg",
    "resume_url": "http://localhost:8000/media/resume.pdf",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
}]
```

#### GET `/skills/`
**Purpose**: Retrieve skills and expertise
**Query Parameters**:
- `category`: Filter by skill category (technical, soft, language, tool)
- `featured`: Filter featured skills (true/false)

**Response**:
```json
[{
    "id": 1,
    "name": "Python",
    "category": "technical",
    "category_display": "Technical",
    "proficiency_level": 5,
    "description": "Advanced Python programming...",
    "icon_url": "http://localhost:8000/media/python-icon.png",
    "order": 1,
    "is_featured": true
}]
```

#### GET `/projects/`
**Purpose**: Retrieve portfolio projects
**Query Parameters**:
- `status`: Filter by project status (completed, in_progress, planned)
- `featured`: Filter featured projects (true/false)

**Response**:
```json
[{
    "id": 1,
    "title": "E-commerce Platform",
    "description": "Full-stack e-commerce solution...",
    "detailed_description": "Detailed project description...",
    "status": "completed",
    "status_display": "Completed",
    "start_date": "2024-01-01",
    "end_date": "2024-03-01",
    "project_url": "https://example-ecommerce.com",
    "github_url": "https://github.com/johndoe/ecommerce",
    "demo_url": "https://demo.example-ecommerce.com",
    "featured_image_url": "http://localhost:8000/media/project1.jpg",
    "technologies": [
        {
            "id": 1,
            "name": "Django",
            "category": "technical"
        }
    ],
    "images": [
        {
            "id": 1,
            "image_url": "http://localhost:8000/media/project1-gallery1.jpg",
            "caption": "Homepage screenshot",
            "order": 1
        }
    ],
    "is_featured": true,
    "order": 1,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
}]
```

#### GET `/projects/{id}/`
**Purpose**: Retrieve detailed information for a specific project
**Response**: Same as projects list but for single project

#### GET `/experience/`
**Purpose**: Retrieve work experience
**Response**:
```json
[{
    "id": 1,
    "company": "Tech Corp",
    "position": "Senior Developer",
    "description": "Led development team of 5 engineers...",
    "start_date": "2022-01-01",
    "end_date": "2024-01-01",
    "is_current": false,
    "location": "San Francisco, CA",
    "company_url": "https://techcorp.com",
    "company_logo_url": "http://localhost:8000/media/techcorp-logo.png",
    "technologies": [
        {
            "id": 1,
            "name": "Python",
            "category": "technical"
        }
    ],
    "order": 1
}]
```

#### POST `/contact/`
**Purpose**: Submit contact form message
**Request Body**:
```json
{
    "name": "Jane Smith",
    "email": "jane@example.com",
    "subject": "Project Inquiry",
    "message": "I'd like to discuss a potential project..."
}
```
**Response**:
```json
{
    "id": 1,
    "name": "Jane Smith",
    "email": "jane@example.com",
    "subject": "Project Inquiry",
    "message": "I'd like to discuss a potential project...",
    "created_at": "2024-01-01T00:00:00Z"
}
```

#### GET `/summary/`
**Purpose**: Get combined portfolio data for homepage
**Response**:
```json
{
    "personal_info": { /* PersonalInfo object */ },
    "featured_projects": [ /* Array of featured projects */ ],
    "featured_skills": [ /* Array of featured skills */ ],
    "recent_experience": [ /* Array of recent experience */ ]
}
```

### Error Responses

All endpoints return consistent error responses:

```json
{
    "error": "Error message description"
}
```

Common HTTP status codes:
- `200`: Success
- `400`: Bad Request (validation errors)
- `404`: Not Found
- `500`: Internal Server Error

## Database Models

### PersonalInfo Model
**Purpose**: Store personal and professional information
**Fields**:
- `name`: CharField(100) - Full name
- `title`: CharField(200) - Professional title
- `bio`: TextField - Biography/description
- `email`: EmailField - Contact email
- `phone`: CharField(20) - Phone number (optional)
- `location`: CharField(100) - Location (optional)
- `linkedin_url`: URLField - LinkedIn profile (optional)
- `github_url`: URLField - GitHub profile (optional)
- `website_url`: URLField - Personal website (optional)
- `profile_image`: FilerImageField - Profile photo (optional)
- `resume`: FilerFileField - Resume file (optional)
- `created_at`: DateTimeField - Creation timestamp
- `updated_at`: DateTimeField - Last update timestamp
- `is_active`: BooleanField - Active status

### Skill Model
**Purpose**: Store skills and expertise information
**Fields**:
- `name`: CharField(100) - Skill name
- `category`: CharField(20) - Category (technical, soft, language, tool)
- `proficiency_level`: IntegerField(1-5) - Skill level
- `description`: TextField - Skill description (optional)
- `icon`: FilerImageField - Skill icon (optional)
- `order`: PositiveIntegerField - Display order
- `is_featured`: BooleanField - Featured on homepage

**Choices**:
```python
SKILL_CATEGORIES = [
    ('technical', 'Technical'),
    ('soft', 'Soft Skills'),
    ('language', 'Languages'),
    ('tool', 'Tools & Technologies'),
]
```

### Experience Model
**Purpose**: Store work experience and employment history
**Fields**:
- `company`: CharField(200) - Company name
- `position`: CharField(200) - Job title
- `description`: TextField - Job description
- `start_date`: DateField - Employment start date
- `end_date`: DateField - Employment end date (optional)
- `is_current`: BooleanField - Current position flag
- `location`: CharField(100) - Work location (optional)
- `company_url`: URLField - Company website (optional)
- `company_logo`: FilerImageField - Company logo (optional)
- `technologies`: ManyToManyField(Skill) - Technologies used
- `order`: PositiveIntegerField - Display order

### Project Model
**Purpose**: Store portfolio projects
**Fields**:
- `title`: CharField(200) - Project title
- `description`: TextField - Short description
- `detailed_description`: TextField - Detailed description (optional)
- `status`: CharField(20) - Project status
- `start_date`: DateField - Project start date
- `end_date`: DateField - Project end date (optional)
- `project_url`: URLField - Live project URL (optional)
- `github_url`: URLField - GitHub repository (optional)
- `demo_url`: URLField - Demo URL (optional)
- `featured_image`: FilerImageField - Main project image (optional)
- `technologies`: ManyToManyField(Skill) - Technologies used
- `is_featured`: BooleanField - Featured on homepage
- `order`: PositiveIntegerField - Display order
- `created_at`: DateTimeField - Creation timestamp
- `updated_at`: DateTimeField - Last update timestamp

**Status Choices**:
```python
PROJECT_STATUS = [
    ('completed', 'Completed'),
    ('in_progress', 'In Progress'),
    ('planned', 'Planned'),
]
```

### ProjectImage Model
**Purpose**: Store additional images for projects
**Fields**:
- `project`: ForeignKey(Project) - Related project
- `image`: FilerImageField - Image file
- `caption`: CharField(200) - Image caption (optional)
- `order`: PositiveIntegerField - Display order

### ContactMessage Model
**Purpose**: Store contact form submissions
**Fields**:
- `name`: CharField(100) - Sender name
- `email`: EmailField - Sender email
- `subject`: CharField(200) - Message subject
- `message`: TextField - Message content
- `created_at`: DateTimeField - Submission timestamp
- `is_read`: BooleanField - Read status for admin

## Configuration Files

### package.json
**Purpose**: Node.js project configuration and dependencies
**Key Sections**:

```json
{
  "name": "portfolio-frontend",
  "version": "1.0.0",
  "description": "Node.js frontend for portfolio website with Django CMS backend",
  "main": "index.js",
  "scripts": {
    "start": "node index.js",
    "dev": "nodemon index.js",
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "dependencies": {
    "express": "^4.18.2",
    "ejs": "^3.1.9",
    "axios": "^1.6.0",
    "cors": "^2.8.5",
    "dotenv": "^16.3.1",
    "express-rate-limit": "^7.1.5",
    "helmet": "^7.1.0",
    "morgan": "^1.10.0"
  },
  "devDependencies": {
    "nodemon": "^3.0.1"
  }
}
```

**Dependencies Explained**:
- `express`: Web application framework
- `ejs`: Embedded JavaScript templating
- `axios`: Promise-based HTTP client
- `cors`: Cross-Origin Resource Sharing middleware
- `dotenv`: Environment variable loader
- `express-rate-limit`: Rate limiting middleware
- `helmet`: Security middleware collection
- `morgan`: HTTP request logger
- `nodemon`: Development auto-restart utility

### .env
**Purpose**: Environment variables configuration
**Variables**:
```env
NODE_ENV=development          # Environment (development/production)
PORT=3000                    # Node.js server port
DJANGO_API_BASE=http://localhost:8000  # Django API base URL
SESSION_SECRET=your-secret-key-here    # Session encryption key
```

### requirements.in
**Purpose**: Python dependencies for Django backend
**Dependencies**:
```
djangocms-versioning         # CMS versioning support
djangocms-alias             # Content aliasing
djangocms-frontend>=2.0.0a1 # Bootstrap frontend components
django-filer                # File management
djangocms-text              # Rich text editing
django-fsm<3                # Finite state machine
djangorestframework         # REST API framework
django-cors-headers         # CORS support
Pillow                      # Image processing
```

### Django Settings Key Configurations

#### Database Configuration
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

#### REST Framework Configuration
```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}
```

#### CORS Configuration
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = DEBUG  # Only in development
```

#### Media Files Configuration
```python
MEDIA_URL = "media/"
MEDIA_ROOT = str(BASE_DIR.parent / "media")
```

## Templates and Static Files

### EJS Templates Structure

#### Template Hierarchy
```
views/
├── partials/
│   ├── header.ejs          # Navigation and HTML head
│   └── footer.ejs          # Footer and closing scripts
├── index.ejs               # Homepage template
├── projects.ejs            # Projects listing
├── project-detail.ejs      # Individual project page
├── experience.ejs          # Work experience timeline
├── skills.ejs              # Skills showcase
├── contact.ejs             # Contact form
├── contact-success.ejs     # Contact success page
└── error.ejs               # Error page template
```

#### Template Features

**Header Partial (`partials/header.ejs`)**:
- HTML5 document structure
- Bootstrap 5 CSS and Font Awesome icons
- Google Fonts (Inter)
- Responsive navigation bar
- Custom CSS inclusion

**Footer Partial (`partials/footer.ejs`)**:
- Bootstrap 5 JavaScript
- Custom JavaScript inclusion
- Footer content with copyright

**Homepage Template (`index.ejs`)**:
- Hero section with personal information
- Featured skills grid
- Featured projects carousel
- Recent experience timeline
- Responsive design with Bootstrap classes

**Projects Template (`projects.ejs`)**:
- Project cards with filtering
- Technology badges
- Status indicators
- Image galleries
- Responsive grid layout

**Project Detail Template (`project-detail.ejs`)**:
- Detailed project information
- Image gallery
- Technology stack display
- External links (GitHub, live demo)
- Breadcrumb navigation

**Experience Template (`experience.ejs`)**:
- Timeline layout
- Company logos
- Technology tags
- Responsive design for mobile

**Skills Template (`skills.ejs`)**:
- Categorized skill display
- Proficiency level indicators
- Skill icons
- Featured skills section

**Contact Template (`contact.ejs`)**:
- Contact form with validation
- Personal contact information
- Social media links
- Form submission handling

### CSS Styles (`public/css/style.css`)

#### CSS Architecture
```css
/* CSS Custom Properties */
:root {
    --primary-color: #0d6efd;
    --secondary-color: #6c757d;
    /* ... other color variables */
}

/* Base Styles */
body { /* Global typography and spacing */ }

/* Navigation */
.navbar-brand { /* Brand styling */ }
.navbar-nav .nav-link { /* Navigation links */ }

/* Hero Section */
.hero-section { /* Homepage hero styling */ }
.profile-image { /* Profile image styling */ }

/* Components */
.card { /* Card component styling */ }
.project-card { /* Project-specific card styling */ }
.skill-card { /* Skill card styling */ }

/* Timeline */
.timeline { /* Experience timeline */ }
.timeline-item { /* Timeline item styling */ }

/* Responsive Design */
@media (max-width: 768px) { /* Tablet styles */ }
@media (max-width: 576px) { /* Mobile styles */ }
```

#### Key CSS Features
- CSS Custom Properties for consistent theming
- Responsive design with mobile-first approach
- Bootstrap 5 integration with custom overrides
- Smooth animations and transitions
- Professional color scheme
- Typography optimization with Inter font

### JavaScript (`public/js/main.js`)

#### JavaScript Architecture
```javascript
// Main initialization
document.addEventListener('DOMContentLoaded', function() {
    initNavigation();
    initContactForm();
    initAnimations();
    initImageLazyLoading();
});

// Navigation functionality
function initNavigation() { /* Active link highlighting, scroll effects */ }

// Contact form handling
function initContactForm() { /* Form validation, submission handling */ }

// Animation initialization
function initAnimations() { /* Intersection Observer for fade-in effects */ }

// Image lazy loading
function initImageLazyLoading() { /* Performance optimization */ }

// Utility functions
const utils = {
    formatDate: function(dateString) { /* Date formatting */ },
    truncateText: function(text, maxLength) { /* Text truncation */ },
    debounce: function(func, wait) { /* Function debouncing */ }
};
```

#### JavaScript Features
- Modern ES6+ syntax
- Intersection Observer API for animations
- Form validation and submission handling
- Image lazy loading for performance
- Responsive navigation enhancements
- Error handling for missing images
- Back-to-top functionality
- Smooth scrolling for anchor links

## Setup and Deployment

### Development Setup

#### Prerequisites
- Node.js 16+ and npm 8+
- Python 3.8+ and pip
- Git for version control

#### Installation Steps
1. **Clone Repository**
   ```bash
   git clone <repository-url>
   cd cms
   ```

2. **Backend Setup**
   ```bash
   cd screencastcms
   pip install -r requirements.in
   python manage.py migrate
   python manage.py createsuperuser
   ```

3. **Frontend Setup**
   ```bash
   cd ..
   npm install
   ```

4. **Environment Configuration**
   ```bash
   # Create .env file with required variables
   NODE_ENV=development
   PORT=3000
   DJANGO_API_BASE=http://localhost:8000
   ```

#### Running the Application
1. **Start Django Backend**
   ```bash
   cd screencastcms
   python manage.py runserver
   ```

2. **Start Node.js Frontend**
   ```bash
   npm start  # or npm run dev for development
   ```

3. **Access Applications**
   - Frontend: http://localhost:3000
   - Django Admin: http://localhost:8000/admin/
   - API: http://localhost:8000/portfolio/api/

### Production Deployment

#### Environment Variables
```env
NODE_ENV=production
PORT=80
DJANGO_API_BASE=https://api.yourdomain.com
SESSION_SECRET=secure-random-key
```

#### Django Production Settings
- Set `DEBUG = False`
- Configure `ALLOWED_HOSTS`
- Use PostgreSQL database
- Set up static file serving
- Configure secure secret keys

#### Security Considerations
- Enable HTTPS
- Configure CSP headers
- Set up rate limiting
- Use environment variables for secrets
- Regular security updates

#### Performance Optimization
- Enable gzip compression
- Set up CDN for static assets
- Database query optimization
- Image optimization
- Caching strategies

This documentation provides a comprehensive overview of the portfolio website architecture, codebase structure, and deployment procedures. Each component is designed to work together seamlessly while maintaining clear separation of concerns between the frontend and backend systems.
