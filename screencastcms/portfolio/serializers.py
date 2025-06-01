from rest_framework import serializers
from .models import PersonalInfo, Skill, Experience, Project, ProjectImage, ContactMessage


class SkillSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    icon_url = serializers.SerializerMethodField()

    class Meta:
        model = Skill
        fields = ['id', 'name', 'category', 'category_display', 'proficiency_level', 
                 'description', 'icon_url', 'order', 'is_featured']

    def get_icon_url(self, obj):
        if obj.icon:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.icon.url)
            return obj.icon.url
        return None


class ProjectImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProjectImage
        fields = ['id', 'image_url', 'caption', 'order']

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class ProjectSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    featured_image_url = serializers.SerializerMethodField()
    technologies = SkillSerializer(many=True, read_only=True)
    images = ProjectImageSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'detailed_description', 'status', 
                 'status_display', 'start_date', 'end_date', 'project_url', 
                 'github_url', 'demo_url', 'featured_image_url', 'technologies', 
                 'images', 'is_featured', 'order', 'created_at', 'updated_at']

    def get_featured_image_url(self, obj):
        if obj.featured_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.featured_image.url)
            return obj.featured_image.url
        return None


class ExperienceSerializer(serializers.ModelSerializer):
    company_logo_url = serializers.SerializerMethodField()
    technologies = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = Experience
        fields = ['id', 'company', 'position', 'description', 'start_date', 
                 'end_date', 'is_current', 'location', 'company_url', 
                 'company_logo_url', 'technologies', 'order']

    def get_company_logo_url(self, obj):
        if obj.company_logo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.company_logo.url)
            return obj.company_logo.url
        return None


class PersonalInfoSerializer(serializers.ModelSerializer):
    profile_image_url = serializers.SerializerMethodField()
    resume_url = serializers.SerializerMethodField()

    class Meta:
        model = PersonalInfo
        fields = ['id', 'name', 'title', 'bio', 'email', 'phone', 'location', 
                 'linkedin_url', 'github_url', 'website_url', 'profile_image_url', 
                 'resume_url', 'created_at', 'updated_at']

    def get_profile_image_url(self, obj):
        if obj.profile_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.profile_image.url)
            return obj.profile_image.url
        return None

    def get_resume_url(self, obj):
        if obj.resume:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.resume.url)
            return obj.resume.url
        return None


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'subject', 'message', 'created_at']
        read_only_fields = ['id', 'created_at']


class PortfolioSummarySerializer(serializers.Serializer):
    """Serializer for portfolio summary data"""
    personal_info = PersonalInfoSerializer(read_only=True)
    featured_projects = ProjectSerializer(many=True, read_only=True)
    featured_skills = SkillSerializer(many=True, read_only=True)
    recent_experience = ExperienceSerializer(many=True, read_only=True)
