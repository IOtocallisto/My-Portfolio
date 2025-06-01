# Developer Guide

## Overview
This guide provides detailed information for developers working on the portfolio website, including development workflows, coding standards, testing procedures, and contribution guidelines.

## Table of Contents
1. [Development Environment Setup](#development-environment-setup)
2. [Project Architecture](#project-architecture)
3. [Coding Standards](#coding-standards)
4. [Development Workflow](#development-workflow)
5. [Testing Guidelines](#testing-guidelines)
6. [Debugging and Troubleshooting](#debugging-and-troubleshooting)
7. [Contributing Guidelines](#contributing-guidelines)
8. [Code Review Process](#code-review-process)

## Development Environment Setup

### Prerequisites
- **Node.js**: Version 16+ with npm 8+
- **Python**: Version 3.8+ with pip
- **Git**: Latest version
- **Code Editor**: VS Code (recommended) with extensions
- **Database**: SQLite (development) / PostgreSQL (production)

### Recommended VS Code Extensions
```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.flake8",
    "ms-python.black-formatter",
    "bradlc.vscode-tailwindcss",
    "esbenp.prettier-vscode",
    "ms-vscode.vscode-json",
    "ms-python.isort",
    "ms-vscode.vscode-eslint"
  ]
}
```

### Environment Configuration

#### Backend (.env for Django)
```bash
# screencastcms/.env
DEBUG=True
SECRET_KEY=dev-secret-key-change-in-production
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOW_ALL_ORIGINS=True
```

#### Frontend (.env for Node.js)
```bash
# .env
NODE_ENV=development
PORT=3000
DJANGO_API_BASE=http://localhost:8000
SESSION_SECRET=dev-session-secret
```

### Development Setup Script
Create `setup-dev.sh`:
```bash
#!/bin/bash
set -e

echo "Setting up Portfolio Website Development Environment..."

# Backend setup
echo "Setting up Django backend..."
cd screencastcms
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.in
python manage.py migrate
echo "Creating superuser (skip if exists)..."
python manage.py createsuperuser --noinput --username admin --email admin@example.com || true
cd ..

# Frontend setup
echo "Setting up Node.js frontend..."
npm install

echo "Setup complete!"
echo "Start backend: cd screencastcms && source venv/bin/activate && python manage.py runserver"
echo "Start frontend: npm run dev"
```

## Project Architecture

### Directory Structure Overview
```
cms/
├── screencastcms/           # Django Backend
│   ├── portfolio/           # Portfolio app
│   │   ├── models.py       # Data models
│   │   ├── views.py        # API views
│   │   ├── serializers.py  # DRF serializers
│   │   ├── admin.py        # Admin interface
│   │   └── urls.py         # URL routing
│   └── screencastcms/      # Django settings
├── views/                  # EJS templates
├── public/                 # Static assets
├── index.js               # Express server
└── package.json           # Node.js config
```

### Data Flow Architecture
```
Browser Request
    ↓
Express.js Server (Node.js)
    ↓
API Request (Axios)
    ↓
Django REST API
    ↓
Database (SQLite/PostgreSQL)
    ↓
JSON Response
    ↓
EJS Template Rendering
    ↓
HTML Response to Browser
```

### Component Relationships
```
Frontend Components:
- Express.js Routes → EJS Templates → Static Assets
- API Client (Axios) → Django REST API

Backend Components:
- Django Models → DRF Serializers → API Views
- Django Admin → Content Management
- Django Filer → File Management
```

## Coding Standards

### Python (Django Backend)

#### Code Style
- **Formatter**: Black with line length 88
- **Linter**: Flake8 with Django plugin
- **Import Sorting**: isort
- **Type Hints**: Use where beneficial

#### Django Conventions
```python
# models.py - Model naming
class PersonalInfo(models.Model):  # PascalCase
    name = models.CharField(max_length=100)  # snake_case fields
    
    class Meta:
        verbose_name = "Personal Information"
        verbose_name_plural = "Personal Information"

# views.py - View naming
class PersonalInfoListView(generics.ListAPIView):  # PascalCase + descriptive suffix
    serializer_class = PersonalInfoSerializer
    
    def get_queryset(self):  # snake_case methods
        return PersonalInfo.objects.filter(is_active=True)

# serializers.py - Serializer naming
class PersonalInfoSerializer(serializers.ModelSerializer):  # PascalCase + Serializer suffix
    profile_image_url = serializers.SerializerMethodField()  # snake_case fields
    
    def get_profile_image_url(self, obj):  # get_ prefix for SerializerMethodField
        # Implementation
        pass
```

#### Documentation Standards
```python
class Project(models.Model):
    """
    Model representing a portfolio project.
    
    Attributes:
        title: Project title (max 200 chars)
        description: Short project description
        status: Current project status (completed/in_progress/planned)
        technologies: Many-to-many relationship with Skill model
    """
    title = models.CharField(max_length=200, help_text="Project title")
    
    def __str__(self):
        """Return string representation of the project."""
        return self.title
```

### JavaScript (Node.js Frontend)

#### Code Style
- **Formatter**: Prettier
- **Linter**: ESLint with recommended rules
- **Style**: Modern ES6+ syntax

#### Naming Conventions
```javascript
// Variables and functions - camelCase
const apiClient = axios.create({...});
const portfolioData = await fetchPortfolioData();

// Constants - UPPER_SNAKE_CASE
const DJANGO_API_BASE = process.env.DJANGO_API_BASE;
const DEFAULT_PORT = 3000;

// Classes - PascalCase (if used)
class ApiClient {
    constructor(baseURL) {
        this.baseURL = baseURL;
    }
}

// File names - kebab-case
// project-detail.ejs, contact-form.js
```

#### Error Handling
```javascript
// API calls with proper error handling
const handleApiError = (error, res, defaultMessage = 'An error occurred') => {
    console.error('API Error:', error.message);
    
    if (error.response) {
        console.error('Response data:', error.response.data);
        console.error('Response status:', error.response.status);
    }
    
    res.status(500).render('error', { 
        message: defaultMessage,
        error: process.env.NODE_ENV === 'development' ? error : {}
    });
};

// Route with error handling
app.get('/projects', async (req, res) => {
    try {
        const response = await apiClient.get('/portfolio/api/projects/');
        const projects = response.data.results || response.data;
        
        res.render('projects', { 
            title: 'Projects',
            projects: projects
        });
    } catch (error) {
        handleApiError(error, res, 'Failed to load projects');
    }
});
```

### CSS/SCSS Standards

#### Organization
```css
/* 1. CSS Custom Properties */
:root {
    --primary-color: #0d6efd;
    --secondary-color: #6c757d;
}

/* 2. Base Styles */
body {
    font-family: 'Inter', sans-serif;
}

/* 3. Layout Components */
.hero-section { /* ... */ }
.navbar { /* ... */ }

/* 4. UI Components */
.card { /* ... */ }
.btn { /* ... */ }

/* 5. Utilities */
.text-gradient { /* ... */ }

/* 6. Responsive Design */
@media (max-width: 768px) { /* ... */ }
```

#### Naming Convention (BEM-inspired)
```css
/* Block */
.project-card { }

/* Element */
.project-card__image { }
.project-card__title { }
.project-card__description { }

/* Modifier */
.project-card--featured { }
.project-card--large { }
```

## Development Workflow

### Git Workflow

#### Branch Naming
```bash
# Feature branches
feature/add-project-filtering
feature/improve-contact-form

# Bug fixes
bugfix/fix-mobile-navigation
bugfix/api-error-handling

# Hotfixes
hotfix/security-patch
hotfix/critical-bug-fix

# Release branches
release/v1.2.0
```

#### Commit Messages
```bash
# Format: type(scope): description
feat(api): add project filtering endpoint
fix(frontend): resolve mobile navigation issue
docs(readme): update installation instructions
style(css): improve responsive design
refactor(models): optimize database queries
test(api): add unit tests for contact form
```

### Development Process

#### 1. Starting New Feature
```bash
# Create and switch to feature branch
git checkout -b feature/new-feature-name

# Make changes and commit regularly
git add .
git commit -m "feat(scope): implement feature component"

# Push to remote
git push origin feature/new-feature-name
```

#### 2. Backend Development
```bash
# Activate virtual environment
cd screencastcms
source venv/bin/activate

# Install new dependencies
pip install new-package
pip freeze > requirements.in

# Create migrations for model changes
python manage.py makemigrations
python manage.py migrate

# Run development server
python manage.py runserver
```

#### 3. Frontend Development
```bash
# Install new dependencies
npm install new-package

# Run development server with auto-reload
npm run dev

# Build for production testing
npm run build
```

#### 4. Testing Changes
```bash
# Backend tests
cd screencastcms
python manage.py test

# Frontend tests (if implemented)
npm test

# Manual testing
# - Test all affected pages
# - Verify API endpoints
# - Check responsive design
# - Validate forms
```

### Database Migrations

#### Creating Migrations
```bash
# After model changes
python manage.py makemigrations portfolio

# Review migration file
cat portfolio/migrations/0002_add_new_field.py

# Apply migrations
python manage.py migrate

# Check migration status
python manage.py showmigrations
```

#### Migration Best Practices
```python
# Good migration example
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('portfolio', '0001_initial'),
    ]
    
    operations = [
        migrations.AddField(
            model_name='project',
            name='priority',
            field=models.IntegerField(default=0, help_text="Project priority for ordering"),
        ),
    ]
```

### API Development

#### Adding New Endpoints
1. **Define Model** (if needed)
2. **Create Serializer**
3. **Implement View**
4. **Add URL Pattern**
5. **Update Frontend**
6. **Test Endpoint**

#### Example: Adding Project Categories
```python
# 1. models.py
class ProjectCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

# 2. serializers.py
class ProjectCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCategory
        fields = ['id', 'name', 'slug', 'description']

# 3. views.py
class ProjectCategoryListView(generics.ListAPIView):
    serializer_class = ProjectCategorySerializer
    queryset = ProjectCategory.objects.all()

# 4. urls.py
urlpatterns = [
    # ... existing patterns
    path('api/project-categories/', views.ProjectCategoryListView.as_view(), name='project-categories'),
]

# 5. Frontend (index.js)
app.get('/categories', async (req, res) => {
    try {
        const response = await apiClient.get('/portfolio/api/project-categories/');
        const categories = response.data;
        
        res.render('categories', { 
            title: 'Project Categories',
            categories: categories
        });
    } catch (error) {
        handleApiError(error, res, 'Failed to load categories');
    }
});
```

## Testing Guidelines

### Backend Testing (Django)

#### Unit Tests
```python
# portfolio/tests.py
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import PersonalInfo, Project, Skill

class PersonalInfoModelTest(TestCase):
    def setUp(self):
        self.personal_info = PersonalInfo.objects.create(
            name="Test User",
            title="Test Developer",
            bio="Test bio",
            email="test@example.com"
        )
    
    def test_string_representation(self):
        self.assertEqual(str(self.personal_info), "Test User")
    
    def test_email_validation(self):
        self.assertTrue(self.personal_info.email)

class ProjectAPITest(APITestCase):
    def setUp(self):
        self.skill = Skill.objects.create(
            name="Python",
            category="technical",
            proficiency_level=5
        )
        self.project = Project.objects.create(
            title="Test Project",
            description="Test description",
            status="completed",
            start_date="2024-01-01"
        )
        self.project.technologies.add(self.skill)
    
    def test_get_projects(self):
        url = reverse('portfolio:projects')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Project')
    
    def test_filter_featured_projects(self):
        self.project.is_featured = True
        self.project.save()
        
        url = reverse('portfolio:projects')
        response = self.client.get(url, {'featured': 'true'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
```

#### Running Tests
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test portfolio

# Run specific test class
python manage.py test portfolio.tests.ProjectAPITest

# Run with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

### Frontend Testing

#### Manual Testing Checklist
```markdown
## Page Load Tests
- [ ] Homepage loads with portfolio summary
- [ ] Projects page displays all projects
- [ ] Individual project pages load correctly
- [ ] Experience page shows timeline
- [ ] Skills page displays categorized skills
- [ ] Contact page loads form

## Functionality Tests
- [ ] Navigation works on all pages
- [ ] Contact form submits successfully
- [ ] Project filtering works (if implemented)
- [ ] Responsive design on mobile/tablet
- [ ] Images load correctly
- [ ] External links open in new tabs

## API Integration Tests
- [ ] All API endpoints return data
- [ ] Error handling displays user-friendly messages
- [ ] Loading states work properly
- [ ] Data displays correctly in templates
```

#### Automated Testing (Future Implementation)
```javascript
// Example with Jest and Supertest
const request = require('supertest');
const app = require('../index');

describe('Frontend Routes', () => {
    test('GET / should return homepage', async () => {
        const response = await request(app).get('/');
        expect(response.status).toBe(200);
        expect(response.text).toContain('Portfolio');
    });
    
    test('GET /projects should return projects page', async () => {
        const response = await request(app).get('/projects');
        expect(response.status).toBe(200);
        expect(response.text).toContain('Projects');
    });
});
```

## Debugging and Troubleshooting

### Common Issues and Solutions

#### Backend Issues

**Issue**: Django server won't start
```bash
# Check for migration issues
python manage.py showmigrations
python manage.py migrate

# Check for syntax errors
python manage.py check

# Check for port conflicts
lsof -i :8000
```

**Issue**: API returns 500 errors
```python
# Enable debug mode temporarily
DEBUG = True

# Check Django logs
tail -f /var/log/django/debug.log

# Add logging to views
import logging
logger = logging.getLogger(__name__)

def my_view(request):
    logger.info(f"Processing request: {request.path}")
    try:
        # Your code here
        pass
    except Exception as e:
        logger.error(f"Error in my_view: {str(e)}")
        raise
```

#### Frontend Issues

**Issue**: Node.js server crashes
```bash
# Check for syntax errors
node --check index.js

# Run with debugging
DEBUG=* npm start

# Check for port conflicts
lsof -i :3000
```

**Issue**: API calls fail
```javascript
// Add detailed error logging
const handleApiError = (error, res, defaultMessage) => {
    console.error('Full error object:', error);
    console.error('Error config:', error.config);
    console.error('Error request:', error.request);
    console.error('Error response:', error.response);
    
    // Rest of error handling
};
```

### Debugging Tools

#### Backend Debugging
```python
# Django Debug Toolbar (development)
pip install django-debug-toolbar

# settings.py
if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    INTERNAL_IPS = ['127.0.0.1']

# Python debugger
import pdb; pdb.set_trace()  # Set breakpoint

# Django shell for testing
python manage.py shell
>>> from portfolio.models import Project
>>> Project.objects.all()
```

#### Frontend Debugging
```javascript
// Console debugging
console.log('Debug info:', { variable, anotherVariable });
console.error('Error occurred:', error);
console.table(arrayOfObjects);

// Node.js debugger
debugger; // Set breakpoint

// Environment-specific logging
if (process.env.NODE_ENV === 'development') {
    console.log('Development debug info:', data);
}
```

### Performance Debugging

#### Database Query Optimization
```python
# Django Debug Toolbar shows query count
# Optimize with select_related and prefetch_related

# Before (N+1 queries)
projects = Project.objects.all()
for project in projects:
    print(project.technologies.all())  # Additional query per project

# After (2 queries total)
projects = Project.objects.prefetch_related('technologies').all()
for project in projects:
    print(project.technologies.all())  # No additional queries
```

#### Frontend Performance
```javascript
// Measure API response times
const startTime = Date.now();
const response = await apiClient.get('/portfolio/api/projects/');
const endTime = Date.now();
console.log(`API call took ${endTime - startTime}ms`);

// Monitor memory usage
console.log('Memory usage:', process.memoryUsage());
```

## Contributing Guidelines

### Code Contribution Process

1. **Fork Repository** (for external contributors)
2. **Create Feature Branch**
3. **Implement Changes**
4. **Write Tests**
5. **Update Documentation**
6. **Submit Pull Request**

### Pull Request Template
```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Manual testing completed
- [ ] Cross-browser testing (if frontend changes)

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No console errors or warnings
```

### Documentation Standards

#### Code Comments
```python
# Good comments explain WHY, not WHAT
def calculate_project_score(project):
    """
    Calculate project relevance score for homepage display.
    
    Uses a weighted algorithm considering:
    - Project completion status (40%)
    - Technology stack relevance (30%)
    - Recency (20%)
    - User engagement metrics (10%)
    
    Args:
        project (Project): Project instance to score
        
    Returns:
        float: Score between 0.0 and 1.0
    """
    # Weight recent projects higher to show current skills
    recency_weight = calculate_recency_weight(project.end_date)
    
    # Implementation details...
```

#### API Documentation
```python
class ProjectListView(generics.ListAPIView):
    """
    List all projects with optional filtering.
    
    Query Parameters:
        status (str): Filter by project status (completed, in_progress, planned)
        featured (bool): Filter featured projects only
        technology (str): Filter by technology name
        
    Returns:
        200: List of projects matching criteria
        400: Invalid query parameters
        500: Server error
        
    Example:
        GET /api/projects/?status=completed&featured=true
    """
```

## Code Review Process

### Review Checklist

#### General
- [ ] Code follows project conventions
- [ ] No obvious bugs or security issues
- [ ] Performance considerations addressed
- [ ] Error handling implemented
- [ ] Documentation updated

#### Backend Specific
- [ ] Database migrations are safe
- [ ] API endpoints follow REST conventions
- [ ] Serializers handle edge cases
- [ ] Admin interface works correctly
- [ ] Tests cover new functionality

#### Frontend Specific
- [ ] Responsive design works
- [ ] Cross-browser compatibility
- [ ] Accessibility considerations
- [ ] Error states handled gracefully
- [ ] Loading states implemented

### Review Guidelines

#### For Reviewers
1. **Be Constructive**: Provide specific, actionable feedback
2. **Ask Questions**: If something is unclear, ask for clarification
3. **Suggest Improvements**: Offer alternative approaches when appropriate
4. **Test Changes**: Pull and test the branch locally
5. **Check Documentation**: Ensure changes are properly documented

#### For Authors
1. **Respond Promptly**: Address feedback in a timely manner
2. **Explain Decisions**: Provide context for implementation choices
3. **Update Based on Feedback**: Make requested changes or discuss alternatives
4. **Test Thoroughly**: Ensure all feedback has been addressed
5. **Update Documentation**: Keep docs in sync with code changes

This developer guide provides comprehensive information for working effectively on the portfolio website project, ensuring code quality, maintainability, and team collaboration.
