from django.db import models
from filer.fields.image import FilerImageField
from filer.fields.file import FilerFileField


class PersonalInfo(models.Model):
    """Model for personal/professional information"""
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    bio = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    website_url = models.URLField(blank=True)
    profile_image = FilerImageField(
        null=True, blank=True, on_delete=models.SET_NULL,
        related_name="profile_images"
    )
    resume = FilerFileField(
        null=True, blank=True, on_delete=models.SET_NULL,
        related_name="resume_files"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Personal Information"
        verbose_name_plural = "Personal Information"

    def __str__(self):
        return self.name


class Skill(models.Model):
    """Model for skills"""
    SKILL_CATEGORIES = [
        ('technical', 'Technical'),
        ('soft', 'Soft Skills'),
        ('language', 'Languages'),
        ('tool', 'Tools & Technologies'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=SKILL_CATEGORIES)
    proficiency_level = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)],
        help_text="1-5 scale (1=Beginner, 5=Expert)"
    )
    description = models.TextField(blank=True)
    icon = FilerImageField(
        null=True, blank=True, on_delete=models.SET_NULL,
        related_name="skill_icons"
    )
    order = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['category', 'order', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class Experience(models.Model):
    """Model for work experience"""
    company = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    location = models.CharField(max_length=100, blank=True)
    company_url = models.URLField(blank=True)
    company_logo = FilerImageField(
        null=True, blank=True, on_delete=models.SET_NULL,
        related_name="company_logos"
    )
    technologies = models.ManyToManyField(Skill, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-start_date', 'order']

    def __str__(self):
        return f"{self.position} at {self.company}"


class Project(models.Model):
    """Model for portfolio projects"""
    PROJECT_STATUS = [
        ('completed', 'Completed'),
        ('in_progress', 'In Progress'),
        ('planned', 'Planned'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    detailed_description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=PROJECT_STATUS, default='completed')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    project_url = models.URLField(blank=True, help_text="Live project URL")
    github_url = models.URLField(blank=True, help_text="GitHub repository URL")
    demo_url = models.URLField(blank=True, help_text="Demo or preview URL")
    featured_image = FilerImageField(
        null=True, blank=True, on_delete=models.SET_NULL,
        related_name="project_featured_images"
    )
    technologies = models.ManyToManyField(Skill, blank=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', 'order', '-start_date']

    def __str__(self):
        return self.title


class ProjectImage(models.Model):
    """Additional images for projects"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = FilerImageField(on_delete=models.CASCADE, related_name="project_images")
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Image for {self.project.title}"


class ContactMessage(models.Model):
    """Model for contact form submissions"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"
