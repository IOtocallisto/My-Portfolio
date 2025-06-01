# API Reference Guide

## Overview
This document provides detailed information about the REST API endpoints provided by the Django CMS backend for the portfolio website.

## Base Configuration
- **Base URL**: `http://localhost:8000/portfolio/api/` (development)
- **Content-Type**: `application/json`
- **Authentication**: None (public API)
- **CORS**: Enabled for frontend domains

## Authentication
Currently, the API is publicly accessible without authentication. For production deployments, consider implementing:
- Token-based authentication
- API key authentication
- OAuth2 integration

## Rate Limiting
- **Development**: No rate limiting
- **Production**: Implement rate limiting based on IP address

## Response Format
All API responses follow a consistent JSON format:

### Success Response
```json
{
  "data": { /* Response data */ },
  "status": "success"
}
```

### Error Response
```json
{
  "error": "Error message",
  "status": "error",
  "code": "ERROR_CODE"
}
```

## Endpoints

### Personal Information

#### GET `/personal-info/`
Retrieve personal and professional information.

**Parameters**: None

**Response**:
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "title": "Full Stack Developer",
    "bio": "Passionate developer with expertise in modern web technologies...",
    "email": "john.doe@example.com",
    "phone": "+1 (555) 123-4567",
    "location": "San Francisco, CA",
    "linkedin_url": "https://linkedin.com/in/johndoe",
    "github_url": "https://github.com/johndoe",
    "website_url": "https://johndoe.dev",
    "profile_image_url": "http://localhost:8000/media/profiles/john_doe.jpg",
    "resume_url": "http://localhost:8000/media/resumes/john_doe_resume.pdf",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-20T14:45:00Z"
  }
]
```

**Status Codes**:
- `200`: Success
- `500`: Server error

---

### Skills

#### GET `/skills/`
Retrieve skills and expertise information.

**Query Parameters**:
- `category` (optional): Filter by skill category
  - Values: `technical`, `soft`, `language`, `tool`
- `featured` (optional): Filter featured skills
  - Values: `true`, `false`

**Examples**:
- `/skills/` - All skills
- `/skills/?category=technical` - Technical skills only
- `/skills/?featured=true` - Featured skills only
- `/skills/?category=technical&featured=true` - Featured technical skills

**Response**:
```json
[
  {
    "id": 1,
    "name": "Python",
    "category": "technical",
    "category_display": "Technical",
    "proficiency_level": 5,
    "description": "Advanced Python programming with Django, Flask, and data science libraries",
    "icon_url": "http://localhost:8000/media/skill_icons/python.png",
    "order": 1,
    "is_featured": true
  },
  {
    "id": 2,
    "name": "JavaScript",
    "category": "technical",
    "category_display": "Technical",
    "proficiency_level": 4,
    "description": "Modern JavaScript (ES6+), Node.js, React, and Vue.js",
    "icon_url": "http://localhost:8000/media/skill_icons/javascript.png",
    "order": 2,
    "is_featured": true
  }
]
```

**Proficiency Levels**:
- `1`: Beginner
- `2`: Novice
- `3`: Intermediate
- `4`: Advanced
- `5`: Expert

**Status Codes**:
- `200`: Success
- `400`: Invalid query parameters
- `500`: Server error

---

### Projects

#### GET `/projects/`
Retrieve portfolio projects.

**Query Parameters**:
- `status` (optional): Filter by project status
  - Values: `completed`, `in_progress`, `planned`
- `featured` (optional): Filter featured projects
  - Values: `true`, `false`

**Examples**:
- `/projects/` - All projects
- `/projects/?status=completed` - Completed projects only
- `/projects/?featured=true` - Featured projects only

**Response**:
```json
[
  {
    "id": 1,
    "title": "E-commerce Platform",
    "description": "Full-stack e-commerce solution with payment integration",
    "detailed_description": "A comprehensive e-commerce platform built with Django and React...",
    "status": "completed",
    "status_display": "Completed",
    "start_date": "2023-06-01",
    "end_date": "2023-09-15",
    "project_url": "https://ecommerce-demo.example.com",
    "github_url": "https://github.com/johndoe/ecommerce-platform",
    "demo_url": "https://demo.ecommerce-platform.com",
    "featured_image_url": "http://localhost:8000/media/projects/ecommerce_main.jpg",
    "technologies": [
      {
        "id": 1,
        "name": "Django",
        "category": "technical",
        "category_display": "Technical",
        "proficiency_level": 5,
        "description": "Python web framework",
        "icon_url": "http://localhost:8000/media/skill_icons/django.png",
        "order": 1,
        "is_featured": true
      }
    ],
    "images": [
      {
        "id": 1,
        "image_url": "http://localhost:8000/media/project_images/ecommerce_gallery_1.jpg",
        "caption": "Homepage with product showcase",
        "order": 1
      }
    ],
    "is_featured": true,
    "order": 1,
    "created_at": "2023-06-01T09:00:00Z",
    "updated_at": "2023-09-15T17:30:00Z"
  }
]
```

**Status Codes**:
- `200`: Success
- `400`: Invalid query parameters
- `500`: Server error

#### GET `/projects/{id}/`
Retrieve detailed information for a specific project.

**Path Parameters**:
- `id`: Project ID (integer)

**Response**: Same structure as projects list but for a single project

**Status Codes**:
- `200`: Success
- `404`: Project not found
- `500`: Server error

---

### Experience

#### GET `/experience/`
Retrieve work experience and employment history.

**Parameters**: None

**Response**:
```json
[
  {
    "id": 1,
    "company": "Tech Innovations Inc.",
    "position": "Senior Full Stack Developer",
    "description": "Led a team of 5 developers in building scalable web applications...",
    "start_date": "2022-03-01",
    "end_date": "2024-01-15",
    "is_current": false,
    "location": "San Francisco, CA",
    "company_url": "https://techinnovations.com",
    "company_logo_url": "http://localhost:8000/media/company_logos/tech_innovations.png",
    "technologies": [
      {
        "id": 1,
        "name": "Python",
        "category": "technical"
      },
      {
        "id": 2,
        "name": "React",
        "category": "technical"
      }
    ],
    "order": 1
  }
]
```

**Status Codes**:
- `200`: Success
- `500`: Server error

---

### Contact

#### POST `/contact/`
Submit a contact form message.

**Request Body**:
```json
{
  "name": "Jane Smith",
  "email": "jane.smith@example.com",
  "subject": "Project Collaboration Inquiry",
  "message": "Hi John, I came across your portfolio and I'm interested in discussing a potential collaboration on a web development project. Could we schedule a call to discuss the details?"
}
```

**Validation Rules**:
- `name`: Required, max 100 characters
- `email`: Required, valid email format
- `subject`: Required, max 200 characters
- `message`: Required, no length limit

**Response**:
```json
{
  "id": 15,
  "name": "Jane Smith",
  "email": "jane.smith@example.com",
  "subject": "Project Collaboration Inquiry",
  "message": "Hi John, I came across your portfolio...",
  "created_at": "2024-01-20T15:30:00Z"
}
```

**Status Codes**:
- `201`: Created successfully
- `400`: Validation errors
- `500`: Server error

**Error Response Example**:
```json
{
  "email": ["Enter a valid email address."],
  "name": ["This field is required."]
}
```

---

### Portfolio Summary

#### GET `/summary/`
Retrieve combined portfolio data optimized for homepage display.

**Parameters**: None

**Response**:
```json
{
  "personal_info": {
    "id": 1,
    "name": "John Doe",
    "title": "Full Stack Developer",
    "bio": "Passionate developer...",
    "email": "john.doe@example.com",
    "profile_image_url": "http://localhost:8000/media/profiles/john_doe.jpg",
    "linkedin_url": "https://linkedin.com/in/johndoe",
    "github_url": "https://github.com/johndoe",
    "resume_url": "http://localhost:8000/media/resumes/resume.pdf"
  },
  "featured_projects": [
    {
      "id": 1,
      "title": "E-commerce Platform",
      "description": "Full-stack e-commerce solution...",
      "featured_image_url": "http://localhost:8000/media/projects/ecommerce.jpg",
      "technologies": [
        {
          "id": 1,
          "name": "Django",
          "category": "technical"
        }
      ],
      "project_url": "https://demo.example.com",
      "github_url": "https://github.com/johndoe/project"
    }
  ],
  "featured_skills": [
    {
      "id": 1,
      "name": "Python",
      "category": "technical",
      "proficiency_level": 5,
      "icon_url": "http://localhost:8000/media/skill_icons/python.png"
    }
  ],
  "recent_experience": [
    {
      "id": 1,
      "company": "Tech Innovations Inc.",
      "position": "Senior Full Stack Developer",
      "start_date": "2022-03-01",
      "end_date": "2024-01-15",
      "is_current": false,
      "company_logo_url": "http://localhost:8000/media/company_logos/tech.png"
    }
  ]
}
```

**Data Limits**:
- `featured_projects`: Maximum 3 projects
- `featured_skills`: All featured skills
- `recent_experience`: Maximum 3 most recent positions

**Status Codes**:
- `200`: Success
- `500`: Server error

## Error Handling

### Common Error Codes
- `VALIDATION_ERROR`: Request data validation failed
- `NOT_FOUND`: Requested resource not found
- `SERVER_ERROR`: Internal server error
- `RATE_LIMITED`: Too many requests

### Error Response Format
```json
{
  "error": "Detailed error message",
  "code": "ERROR_CODE",
  "status": "error",
  "details": {
    "field_name": ["Field-specific error message"]
  }
}
```

## Pagination

For endpoints that return lists, pagination is implemented using Django REST Framework's PageNumberPagination:

**Query Parameters**:
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20, max: 100)

**Paginated Response Format**:
```json
{
  "count": 25,
  "next": "http://localhost:8000/portfolio/api/projects/?page=2",
  "previous": null,
  "results": [
    /* Array of objects */
  ]
}
```

## Content-Type Headers

### Request Headers
```
Content-Type: application/json
Accept: application/json
```

### Response Headers
```
Content-Type: application/json
Access-Control-Allow-Origin: http://localhost:3000
Access-Control-Allow-Credentials: true
```

## Testing the API

### Using curl
```bash
# Get personal info
curl -X GET http://localhost:8000/portfolio/api/personal-info/

# Get featured skills
curl -X GET http://localhost:8000/portfolio/api/skills/?featured=true

# Submit contact form
curl -X POST http://localhost:8000/portfolio/api/contact/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "subject": "Test Message",
    "message": "This is a test message"
  }'
```

### Using JavaScript (Frontend)
```javascript
// Get portfolio summary
const response = await fetch('http://localhost:8000/portfolio/api/summary/');
const data = await response.json();

// Submit contact form
const contactData = {
  name: 'John Doe',
  email: 'john@example.com',
  subject: 'Hello',
  message: 'Test message'
};

const response = await fetch('http://localhost:8000/portfolio/api/contact/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(contactData)
});
```

## API Versioning

Currently, the API is unversioned. For future versions, consider implementing:
- URL versioning: `/api/v1/`, `/api/v2/`
- Header versioning: `Accept: application/vnd.api+json;version=1`
- Query parameter versioning: `?version=1`

## Security Considerations

### Production Recommendations
1. **Authentication**: Implement token-based authentication
2. **Rate Limiting**: Add rate limiting per IP/user
3. **CORS**: Restrict CORS to specific domains
4. **HTTPS**: Enforce HTTPS in production
5. **Input Validation**: Validate and sanitize all inputs
6. **SQL Injection**: Use Django ORM (already implemented)
7. **XSS Protection**: Sanitize output (handled by DRF)
