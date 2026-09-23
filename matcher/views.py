from django.db import transaction
from rest_framework import viewsets, permissions
from .models import Resume, JobPosting, MatchResult
from .serializers import ResumeSerializer, JobPostingSerializer, MatchResultSerializer
from .tasks import extract_resume_text


class ResumeViewSet(viewsets.ModelViewSet):
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        if serializer.validated_data.get('file'):
            resume = serializer.save(user=self.request.user,
                                     extraction_status=Resume.ExtractionStatus.PENDING)
            self._queue_extraction(resume)
        else:
            serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        if serializer.validated_data.get('file'):
            resume = serializer.save(extraction_status=Resume.ExtractionStatus.PENDING,
                                     extraction_error='')
            self._queue_extraction(resume)
        else:
            serializer.save()

    def _queue_extraction(self, resume):
        # Wait until the row is committed so the worker is guaranteed to find it
        transaction.on_commit(lambda: extract_resume_text.delay(resume.id))


class JobPostingViewSet(viewsets.ModelViewSet):
    serializer_class = JobPostingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return JobPosting.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MatchResultViewSet(viewsets.ModelViewSet):
    serializer_class = MatchResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MatchResult.objects.filter(resume__user=self.request.user)