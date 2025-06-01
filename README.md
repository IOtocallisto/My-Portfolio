# Portfolio Website with Node.js Frontend & Django CMS Backend

A modern, responsive portfolio website built with Node.js (Express.js) frontend and Django CMS backend. The frontend dynamically fetches content from Django CMS through REST API endpoints, allowing for easy content management through the Django admin interface.

## 🚀 Features

### Frontend (Node.js)
- **Express.js** server with EJS templating
- **Responsive design** using Bootstrap 5
- **Professional portfolio sections**:
  - Personal information and bio
  - Project showcase with detailed views
  - Work experience timeline
  - Skills and expertise display
  - Contact form
- **API integration** with Django CMS backend
- **Security features** (Helmet, CORS, rate limiting)
- **Error handling** and user-friendly error pages

### Backend (Django CMS)
- **Django CMS 5.0** with content management
- **REST API** endpoints for portfolio data
- **Admin interface** for content management
- **Models for**:
  - Personal information
  - Projects with images and technologies
  - Work experience
  - Skills with proficiency levels
  - Contact messages
- **File management** with Django Filer
- **CORS support** for frontend integration

## 📁 Project Structure

```
cms/
├── screencastcms/              # Django CMS Backend
│   ├── portfolio/              # Portfolio Django app
│   │   ├── models.py          # Data models
│   │   ├── serializers.py     # API serializers
│   │   ├── views.py           # API views
│   │   ├── admin.py           # Admin configuration
│   │   └── urls.py            # API URLs
│   ├── screencastcms/         # Django project settings
│   └── manage.py              # Django management script
├── views/                     # EJS templates
│   ├── partials/              # Reusable template parts
│   ├── index.ejs             # Home page
│   ├── projects.ejs          # Projects listing
│   ├── project-detail.ejs    # Project details
│   ├── experience.ejs        # Work experience
│   ├── skills.ejs            # Skills display
│   ├── contact.ejs           # Contact form
│   └── error.ejs             # Error pages
├── public/                    # Static assets
│   ├── css/style.css         # Custom styles
│   ├── js/main.js            # Frontend JavaScript
│   └── images/               # Image assets
├── index.js                  # Node.js server
├── package.json              # Node.js dependencies
└── .env                      # Environment configuration
```

## 🛠️ Installation & Setup

### Prerequisites
- **Node.js** (v16 or higher)
- **Python** (3.8 or higher)
- **pip** (Python package manager)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd cms
```

### 2. Backend Setup (Django CMS)

#### Install Python Dependencies
```bash
cd screencastcms
pip install -r requirements.in
```

#### Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

#### Create Superuser
```bash
python manage.py createsuperuser
```

#### Collect Static Files
```bash
python manage.py collectstatic
```

### 3. Frontend Setup (Node.js)

#### Install Node.js Dependencies
```bash
cd ..  # Back to root directory
npm install
```

#### Environment Configuration
Create or update the `.env` file:
```env
NODE_ENV=development
PORT=3000
DJANGO_API_BASE=http://localhost:8000
SESSION_SECRET=your-secret-key-here
```

## 🚀 Running the Application

### 1. Start Django CMS Backend
```bash
cd screencastcms
python manage.py runserver
```
The Django admin will be available at: `http://localhost:8000/admin/`

### 2. Start Node.js Frontend
In a new terminal:
```bash
npm start
# or for development with auto-reload:
npm run dev
```
The frontend will be available at: `http://localhost:3000`

## 📊 API Endpoints

The Django backend provides the following API endpoints:

- `GET /portfolio/api/summary/` - Portfolio summary data
- `GET /portfolio/api/personal-info/` - Personal information
- `GET /portfolio/api/projects/` - All projects
- `GET /portfolio/api/projects/{id}/` - Project details
- `GET /portfolio/api/experience/` - Work experience
- `GET /portfolio/api/skills/` - Skills and expertise
- `POST /portfolio/api/contact/` - Submit contact message

### Query Parameters
- `?featured=true` - Filter featured items (projects/skills)
- `?category={category}` - Filter skills by category
- `?status={status}` - Filter projects by status

## 🎨 Customization

### Adding Content
1. Access Django admin at `http://localhost:8000/admin/`
2. Add your personal information, projects, skills, and experience
3. Upload images using the Filer interface
4. Content will automatically appear on the frontend

### Styling
- Modify `public/css/style.css` for custom styles
- Update Bootstrap variables or add custom CSS
- Images and assets go in `public/images/`

### Templates
- EJS templates are in the `views/` directory
- Modify layouts in `views/partials/`
- Add new pages by creating new routes in `index.js`

## 🔧 Configuration

### Django Settings
Key settings in `screencastcms/screencastcms/settings.py`:
- `CORS_ALLOWED_ORIGINS` - Frontend URLs
- `REST_FRAMEWORK` - API configuration
- `MEDIA_ROOT` - File upload location

### Node.js Configuration
Environment variables in `.env`:
- `PORT` - Frontend server port
- `DJANGO_API_BASE` - Backend API URL
- `NODE_ENV` - Environment (development/production)

## 🚀 Deployment

### Production Considerations
1. **Security**:
   - Change Django `SECRET_KEY`
   - Set `DEBUG = False` in Django
   - Update `ALLOWED_HOSTS` in Django
   - Use environment variables for sensitive data

2. **Performance**:
   - Enable Django static file serving
   - Use a reverse proxy (nginx)
   - Implement caching
   - Optimize images

3. **Database**:
   - Use PostgreSQL or MySQL in production
   - Set up database backups

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues:
1. Check the console for error messages
2. Verify both servers are running
3. Check API connectivity
4. Review Django admin for content

## 🔗 Technologies Used

- **Frontend**: Node.js, Express.js, EJS, Bootstrap 5, Font Awesome
- **Backend**: Django 5.2, Django CMS 5.0, Django REST Framework
- **Database**: SQLite (development), PostgreSQL/MySQL (production)
- **File Management**: Django Filer
- **Security**: Helmet, CORS, Rate Limiting
