from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    # API endpoints
    path('api/personal-info/', views.PersonalInfoListView.as_view(), name='personal-info'),
    path('api/skills/', views.SkillListView.as_view(), name='skills'),
    path('api/experience/', views.ExperienceListView.as_view(), name='experience'),
    path('api/projects/', views.ProjectListView.as_view(), name='projects'),
    path('api/projects/<int:pk>/', views.ProjectDetailView.as_view(), name='project-detail'),
    path('api/contact/', views.ContactMessageCreateView.as_view(), name='contact'),
    path('api/summary/', views.portfolio_summary, name='portfolio-summary'),
]
