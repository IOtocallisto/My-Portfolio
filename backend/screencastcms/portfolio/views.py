from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from .models import PersonalInfo, Skill, Experience, Project, ContactMessage
from .serializers import (
    PersonalInfoSerializer, SkillSerializer, ExperienceSerializer,
    ProjectSerializer, ContactMessageSerializer, PortfolioSummarySerializer
)


class PersonalInfoListView(generics.ListAPIView):
    """API view to get personal information"""
    serializer_class = PersonalInfoSerializer

    def get_queryset(self):
        return PersonalInfo.objects.filter(is_active=True)


class SkillListView(generics.ListAPIView):
    """API view to get skills"""
    serializer_class = SkillSerializer

    def get_queryset(self):
        queryset = Skill.objects.all()
        category = self.request.query_params.get('category', None)
        featured = self.request.query_params.get('featured', None)

        if category:
            queryset = queryset.filter(category=category)
        if featured:
            queryset = queryset.filter(is_featured=True)

        return queryset


class ExperienceListView(generics.ListAPIView):
    """API view to get work experience"""
    serializer_class = ExperienceSerializer
    queryset = Experience.objects.all()


class ProjectListView(generics.ListAPIView):
    """API view to get projects"""
    serializer_class = ProjectSerializer

    def get_queryset(self):
        queryset = Project.objects.all()
        status_filter = self.request.query_params.get('status', None)
        featured = self.request.query_params.get('featured', None)

        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if featured:
            queryset = queryset.filter(is_featured=True)

        return queryset


class ProjectDetailView(generics.RetrieveAPIView):
    """API view to get project details"""
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()


class ContactMessageCreateView(generics.CreateAPIView):
    """API view to create contact messages"""
    serializer_class = ContactMessageSerializer
    queryset = ContactMessage.objects.all()


@api_view(['GET'])
def portfolio_summary(request):
    """API view to get portfolio summary data"""
    try:
        personal_info = PersonalInfo.objects.filter(is_active=True).first()
        featured_projects = Project.objects.filter(is_featured=True)[:3]
        featured_skills = Skill.objects.filter(is_featured=True)
        recent_experience = Experience.objects.all()[:3]

        data = {
            'personal_info': PersonalInfoSerializer(personal_info, context={'request': request}).data if personal_info else None,
            'featured_projects': ProjectSerializer(featured_projects, many=True, context={'request': request}).data,
            'featured_skills': SkillSerializer(featured_skills, many=True, context={'request': request}).data,
            'recent_experience': ExperienceSerializer(recent_experience, many=True, context={'request': request}).data,
        }

        return Response(data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
