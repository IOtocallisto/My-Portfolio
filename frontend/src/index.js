require('dotenv').config();
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const rateLimit = require('express-rate-limit');
const path = require('path');
const axios = require('axios');

const app = express();
const PORT = process.env.PORT || 3000;
const DJANGO_API_BASE = process.env.DJANGO_API_BASE || 'http://localhost:8000';

// Security middleware
app.use(helmet({
    contentSecurityPolicy: {
        directives: {
            defaultSrc: ["'self'"],
            styleSrc: ["'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net", "https://fonts.googleapis.com"],
            fontSrc: ["'self'", "https://fonts.gstatic.com", "https://cdn.jsdelivr.net"],
            scriptSrc: ["'self'", "https://cdn.jsdelivr.net"],
            imgSrc: ["'self'", "data:", "https:", "http:"],
        },
    },
}));

// Rate limiting
const limiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100 // limit each IP to 100 requests per windowMs
});
app.use(limiter);

// CORS
app.use(cors());

// Logging
app.use(morgan('combined'));

// Body parsing
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Static files
app.use(express.static(path.join(__dirname, 'public')));

// View engine setup
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// API client helper
const apiClient = axios.create({
    baseURL: DJANGO_API_BASE,
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
    }
});

// Error handler for API calls
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

// Routes
app.get('/', async (req, res) => {
    try {
        const response = await apiClient.get('/portfolio/api/summary/');
        const portfolioData = response.data;

        res.render('index', {
            title: 'Portfolio',
            data: portfolioData
        });
    } catch (error) {
        handleApiError(error, res, 'Failed to load portfolio data');
    }
});

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

app.get('/projects/:id', async (req, res) => {
    try {
        const response = await apiClient.get(`/portfolio/api/projects/${req.params.id}/`);
        const project = response.data;

        res.render('project-detail', {
            title: project.title,
            project: project
        });
    } catch (error) {
        handleApiError(error, res, 'Failed to load project details');
    }
});

app.get('/experience', async (req, res) => {
    try {
        const response = await apiClient.get('/portfolio/api/experience/');
        const experience = response.data.results || response.data;

        res.render('experience', {
            title: 'Experience',
            experience: experience
        });
    } catch (error) {
        handleApiError(error, res, 'Failed to load experience data');
    }
});

app.get('/skills', async (req, res) => {
    try {
        const response = await apiClient.get('/portfolio/api/skills/');
        const skills = response.data.results || response.data;

        res.render('skills', {
            title: 'Skills',
            skills: skills
        });
    } catch (error) {
        handleApiError(error, res, 'Failed to load skills data');
    }
});

app.get('/contact', async (req, res) => {
    try {
        const personalInfoResponse = await apiClient.get('/portfolio/api/personal-info/');
        const personalInfo = personalInfoResponse.data.results?.[0] || personalInfoResponse.data[0] || {};

        res.render('contact', {
            title: 'Contact',
            personalInfo: personalInfo
        });
    } catch (error) {
        handleApiError(error, res, 'Failed to load contact information');
    }
});

app.post('/contact', async (req, res) => {
    try {
        const { name, email, subject, message } = req.body;

        await apiClient.post('/portfolio/api/contact/', {
            name,
            email,
            subject,
            message
        });

        res.render('contact-success', {
            title: 'Message Sent',
            message: 'Thank you for your message! I will get back to you soon.'
        });
    } catch (error) {
        handleApiError(error, res, 'Failed to send message');
    }
});

// 404 handler
app.use((req, res) => {
    res.status(404).render('error', {
        title: 'Page Not Found',
        message: 'The page you are looking for does not exist.',
        error: {}
    });
});

// Error handler
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).render('error', {
        title: 'Server Error',
        message: 'Something went wrong!',
        error: process.env.NODE_ENV === 'development' ? err : {}
    });
});

app.listen(PORT, () => {
    console.log(`Portfolio frontend server running on http://localhost:${PORT}`);
    console.log(`Django API base URL: ${DJANGO_API_BASE}`);
});