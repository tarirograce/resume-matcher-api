from rest_framework import serializers
from .models import Resume, JobPosting, MatchResult

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['id', 'user', 'title', 'raw_text', 'file', 'created_at']
        read_only_fields = ['id', 'created_at']


class JobPostingSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPosting
        fields = ['id', 'user', 'title', 'company', 'raw_text', 'created_at']
        read_only_fields = ['id', 'created_at']


class MatchResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchResult
        fields = ['id', 'resume', 'job_posting', 'match_score', 'gap_analysis', 'created_at']
        read_only_fields = ['id', 'created_at']