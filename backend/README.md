# Portfolio Backend

Django CMS backend application providing REST API for the portfolio website.

## 🚀 Quick Start

```bash
# Navigate to Django project
cd screencastcms

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver 8001
```

## 📁 Structure

```
backend/
└── screencastcms/           # Django project
    ├── portfolio/           # Portfolio Django app
    │   ├── models.py       # Data models
    │   ├── serializers.py  # API serializers
    │   ├── views.py        # API views
    │   ├── admin.py        # Admin configuration
    │   └── urls.py         # API URLs
    ├── screencastcms/      # Django project settings
    │   ├── settings.py     # Configuration
    │   ├── urls.py         # URL routing
    │   └── wsgi.py         # WSGI application
    ├── manage.py           # Django management
    ├── requirements.txt    # Python dependencies
    └── db.sqlite3          # SQLite database
```

## 🔧 Configuration

Key settings in `screencastcms/settings.py`:

- `CORS_ALLOWED_ORIGINS` - Frontend URLs
- `REST_FRAMEWORK` - API configuration  
- `MEDIA_ROOT` - File upload location
- `ALLOWED_HOSTS` - Allowed hostnames

## 📡 API Endpoints

- `GET /portfolio/api/summary/` - Portfolio summary
- `GET /portfolio/api/personal-info/` - Personal information
- `GET /portfolio/api/projects/` - All projects
- `GET /portfolio/api/projects/{id}/` - Project details
- `GET /portfolio/api/experience/` - Work experience
- `GET /portfolio/api/skills/` - Skills and expertise
- `POST /portfolio/api/contact/` - Submit contact message

## 🎨 Features

- **Django CMS 5.0** with content management
- **REST API** endpoints for portfolio data
- **Admin interface** for content management
- **Models for** personal info, projects, experience, skills
- **File management** with Django Filer
- **CORS support** for frontend integration

## 🛠️ Development

```bash
# Install dependencies
pip install -r requirements.txt

# Database setup
python manage.py makemigrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Start server
python manage.py runserver 8001
```

## 📦 Dependencies

- **Django**: Web framework
- **django-cms**: Content management system
- **djangorestframework**: REST API framework
- **django-cors-headers**: CORS support
- **django-filer**: File management
- **Pillow**: Image processing

## 🔐 Admin Access

Access the Django admin at: `http://localhost:8001/admin/`

Use the superuser credentials created during setup to manage:
- Personal information
- Projects and portfolios
- Work experience
- Skills and expertise
- Contact messages
