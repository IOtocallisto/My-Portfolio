# Deployment Guide

## Overview
This guide covers deployment strategies for the Node.js portfolio frontend and Django CMS backend in various environments.

## Table of Contents
1. [Development Environment](#development-environment)
2. [Production Environment](#production-environment)
3. [Docker Deployment](#docker-deployment)
4. [Cloud Deployment](#cloud-deployment)
5. [Security Configuration](#security-configuration)
6. [Performance Optimization](#performance-optimization)
7. [Monitoring and Logging](#monitoring-and-logging)

## Development Environment

### Prerequisites
- Node.js 16+ and npm 8+
- Python 3.8+ and pip
- Git
- SQLite (included with Python)

### Quick Start
```bash
# Clone repository
git clone <repository-url>
cd cms

# Backend setup
cd screencastcms
pip install -r requirements.in
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver &

# Frontend setup
cd ..
npm install
npm run dev
```

### Development URLs
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/portfolio/api/
- Django Admin: http://localhost:8000/admin/

## Production Environment

### System Requirements
- **OS**: Ubuntu 20.04+ / CentOS 8+ / Amazon Linux 2
- **Memory**: Minimum 2GB RAM (4GB+ recommended)
- **Storage**: 20GB+ available space
- **Network**: Public IP with ports 80/443 open

### Production Dependencies
```bash
# System packages (Ubuntu/Debian)
sudo apt update
sudo apt install -y python3 python3-pip python3-venv nodejs npm nginx postgresql postgresql-contrib redis-server

# System packages (CentOS/RHEL)
sudo yum update
sudo yum install -y python3 python3-pip nodejs npm nginx postgresql postgresql-server redis
```

### Database Setup (PostgreSQL)
```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE DATABASE portfolio_db;
CREATE USER portfolio_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE portfolio_db TO portfolio_user;
\q
```

### Backend Production Setup

#### 1. Environment Configuration
```bash
# Create production environment file
cat > screencastcms/.env << EOF
DEBUG=False
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=postgresql://portfolio_user:secure_password@localhost/portfolio_db
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
MEDIA_ROOT=/var/www/portfolio/media
STATIC_ROOT=/var/www/portfolio/static
EOF
```

#### 2. Django Production Settings
Create `screencastcms/screencastcms/production_settings.py`:
```python
from .settings import *
import os
from pathlib import Path

# Security settings
DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'portfolio_db',
        'USER': 'portfolio_user',
        'PASSWORD': 'secure_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Static and media files
STATIC_ROOT = '/var/www/portfolio/static'
MEDIA_ROOT = '/var/www/portfolio/media'

# Security headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# HTTPS settings (when using SSL)
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/portfolio/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

#### 3. Deploy Django Backend
```bash
# Create application directory
sudo mkdir -p /var/www/portfolio
sudo chown $USER:$USER /var/www/portfolio

# Copy application files
cp -r screencastcms /var/www/portfolio/

# Install dependencies
cd /var/www/portfolio/screencastcms
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.in
pip install gunicorn psycopg2-binary

# Run migrations
python manage.py migrate --settings=screencastcms.production_settings
python manage.py collectstatic --settings=screencastcms.production_settings

# Create superuser
python manage.py createsuperuser --settings=screencastcms.production_settings
```

#### 4. Gunicorn Configuration
Create `/var/www/portfolio/screencastcms/gunicorn.conf.py`:
```python
bind = "127.0.0.1:8000"
workers = 3
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2
preload_app = True
```

#### 5. Systemd Service
Create `/etc/systemd/system/portfolio-backend.service`:
```ini
[Unit]
Description=Portfolio Django Backend
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/portfolio/screencastcms
Environment=DJANGO_SETTINGS_MODULE=screencastcms.production_settings
ExecStart=/var/www/portfolio/screencastcms/venv/bin/gunicorn screencastcms.wsgi:application -c gunicorn.conf.py
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
```

### Frontend Production Setup

#### 1. Environment Configuration
```bash
# Create production environment file
cat > .env.production << EOF
NODE_ENV=production
PORT=3001
DJANGO_API_BASE=https://api.yourdomain.com
SESSION_SECRET=your-session-secret-here
EOF
```

#### 2. Production Dependencies
```bash
# Install production dependencies
npm ci --only=production

# Install PM2 for process management
npm install -g pm2
```

#### 3. PM2 Configuration
Create `ecosystem.config.js`:
```javascript
module.exports = {
  apps: [{
    name: 'portfolio-frontend',
    script: 'index.js',
    instances: 'max',
    exec_mode: 'cluster',
    env: {
      NODE_ENV: 'development'
    },
    env_production: {
      NODE_ENV: 'production',
      PORT: 3001,
      DJANGO_API_BASE: 'https://api.yourdomain.com'
    },
    error_file: '/var/log/portfolio/frontend-error.log',
    out_file: '/var/log/portfolio/frontend-out.log',
    log_file: '/var/log/portfolio/frontend.log',
    time: true
  }]
};
```

#### 4. Deploy Frontend
```bash
# Copy frontend files
sudo mkdir -p /var/www/portfolio-frontend
sudo chown $USER:$USER /var/www/portfolio-frontend
cp -r . /var/www/portfolio-frontend/

# Start with PM2
cd /var/www/portfolio-frontend
pm2 start ecosystem.config.js --env production
pm2 save
pm2 startup
```

### Nginx Configuration

#### 1. Main Configuration
Create `/etc/nginx/sites-available/portfolio`:
```nginx
# Frontend server
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    # SSL configuration
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
    
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;
    
    # Frontend proxy
    location / {
        proxy_pass http://127.0.0.1:3001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
    
    # Static files
    location /static/ {
        alias /var/www/portfolio-frontend/public/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}

# Backend API server
server {
    listen 80;
    server_name api.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.yourdomain.com;
    
    # SSL configuration
    ssl_certificate /etc/letsencrypt/live/api.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.yourdomain.com/privkey.pem;
    
    # API proxy
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Django static files
    location /static/ {
        alias /var/www/portfolio/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Django media files
    location /media/ {
        alias /var/www/portfolio/media/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

#### 2. Enable Site
```bash
sudo ln -s /etc/nginx/sites-available/portfolio /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### SSL Certificate (Let's Encrypt)
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificates
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
sudo certbot --nginx -d api.yourdomain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

## Docker Deployment

### Docker Compose Configuration
Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: portfolio_db
      POSTGRES_USER: portfolio_user
      POSTGRES_PASSWORD: secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - portfolio_network

  redis:
    image: redis:6-alpine
    networks:
      - portfolio_network

  backend:
    build: ./screencastcms
    environment:
      - DEBUG=False
      - DATABASE_URL=postgresql://portfolio_user:secure_password@db:5432/portfolio_db
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    volumes:
      - media_files:/app/media
      - static_files:/app/static
    networks:
      - portfolio_network

  frontend:
    build: .
    environment:
      - NODE_ENV=production
      - DJANGO_API_BASE=http://backend:8000
    depends_on:
      - backend
    ports:
      - "3000:3000"
    networks:
      - portfolio_network

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_files:/var/www/static
      - media_files:/var/www/media
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - frontend
      - backend
    networks:
      - portfolio_network

volumes:
  postgres_data:
  media_files:
  static_files:

networks:
  portfolio_network:
    driver: bridge
```

### Backend Dockerfile
Create `screencastcms/Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.in .
RUN pip install -r requirements.in gunicorn psycopg2-binary

# Copy application
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput --settings=screencastcms.production_settings

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "screencastcms.wsgi:application"]
```

### Frontend Dockerfile
Create `Dockerfile`:
```dockerfile
FROM node:16-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci --only=production

# Copy application
COPY . .

EXPOSE 3000

CMD ["npm", "start"]
```

### Deploy with Docker
```bash
# Build and start services
docker-compose up -d

# Run migrations
docker-compose exec backend python manage.py migrate

# Create superuser
docker-compose exec backend python manage.py createsuperuser
```

## Cloud Deployment

### AWS Deployment

#### Using Elastic Beanstalk
1. **Prepare Application**
   ```bash
   # Create .ebextensions directory
   mkdir .ebextensions
   
   # Create configuration files
   cat > .ebextensions/01_packages.config << EOF
   packages:
     yum:
       postgresql-devel: []
   EOF
   ```

2. **Deploy Backend**
   ```bash
   # Install EB CLI
   pip install awsebcli
   
   # Initialize and deploy
   cd screencastcms
   eb init
   eb create portfolio-backend
   eb deploy
   ```

3. **Deploy Frontend**
   ```bash
   cd ..
   eb init
   eb create portfolio-frontend
   eb deploy
   ```

#### Using ECS (Elastic Container Service)
1. **Build and push Docker images**
2. **Create ECS cluster**
3. **Define task definitions**
4. **Create services**
5. **Configure load balancer**

### Google Cloud Platform

#### Using App Engine
1. **Backend (app.yaml)**
   ```yaml
   runtime: python39
   
   env_variables:
     DEBUG: "False"
     DATABASE_URL: "postgresql://user:pass@/db?host=/cloudsql/project:region:instance"
   
   beta_settings:
     cloud_sql_instances: project:region:instance
   ```

2. **Frontend (app.yaml)**
   ```yaml
   runtime: nodejs16
   
   env_variables:
     NODE_ENV: "production"
     DJANGO_API_BASE: "https://backend-dot-project.appspot.com"
   ```

### Heroku Deployment

#### Backend
```bash
# Create Heroku app
heroku create portfolio-backend

# Add PostgreSQL addon
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-secret-key

# Deploy
git push heroku main
heroku run python manage.py migrate
```

#### Frontend
```bash
# Create Heroku app
heroku create portfolio-frontend

# Set environment variables
heroku config:set NODE_ENV=production
heroku config:set DJANGO_API_BASE=https://portfolio-backend.herokuapp.com

# Deploy
git push heroku main
```

## Security Configuration

### Environment Variables
```bash
# Backend security
SECRET_KEY=your-super-secret-django-key
DATABASE_URL=postgresql://user:pass@host:port/db
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Frontend security
SESSION_SECRET=your-session-secret
NODE_ENV=production

# API keys (if needed)
SENDGRID_API_KEY=your-sendgrid-key
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
```

### Security Headers
```nginx
# Nginx security headers
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header X-Content-Type-Options "nosniff" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' cdn.jsdelivr.net fonts.googleapis.com; font-src 'self' fonts.gstatic.com cdn.jsdelivr.net; img-src 'self' data: https:;" always;
```

### Firewall Configuration
```bash
# UFW (Ubuntu)
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable

# Fail2ban
sudo apt install fail2ban
sudo systemctl enable fail2ban
```

## Performance Optimization

### Database Optimization
```python
# Django settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': {
            'MAX_CONNS': 20,
            'CONN_MAX_AGE': 600,
        }
    }
}

# Connection pooling
DATABASES['default']['OPTIONS']['CONN_MAX_AGE'] = 600
```

### Caching
```python
# Redis caching
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Cache middleware
MIDDLEWARE = [
    'django.middleware.cache.UpdateCacheMiddleware',
    # ... other middleware
    'django.middleware.cache.FetchFromCacheMiddleware',
]
```

### CDN Configuration
```nginx
# CloudFlare or AWS CloudFront
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
    add_header Vary Accept-Encoding;
}
```

## Monitoring and Logging

### Application Monitoring
```python
# Django logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/portfolio/django.log',
            'maxBytes': 1024*1024*15,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['file'],
    },
}
```

### Health Checks
```python
# Django health check endpoint
from django.http import JsonResponse
from django.db import connection

def health_check(request):
    try:
        # Check database
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        return JsonResponse({'status': 'healthy'})
    except Exception as e:
        return JsonResponse({'status': 'unhealthy', 'error': str(e)}, status=500)
```

### Process Monitoring
```bash
# PM2 monitoring
pm2 monit

# System monitoring with htop
sudo apt install htop
htop

# Log monitoring
sudo tail -f /var/log/portfolio/*.log
```

This deployment guide provides comprehensive instructions for deploying the portfolio website in various environments, from development to production cloud deployments.
