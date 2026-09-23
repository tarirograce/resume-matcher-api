from rest_framework import serializers
from .models import Resume, JobPosting, MatchResult

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['id', 'user', 'title', 'raw_text', 'file',
                  'extraction_status', 'extraction_error', 'created_at']
        read_only_fields = ['id', 'extraction_status', 'extraction_error', 'created_at']

    def validate_file(self, value):
        if value and not value.name.lower().endswith('.pdf'):
            raise serializers.ValidationError("Only PDF files are supported.")
        return value


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