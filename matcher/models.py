from django.db import models
from django.contrib.auth.models import User

class Resume(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    title = models.CharField(max_length=255)
    raw_text = models.TextField(blank=True)
    file = models.FileField(upload_to='resumes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.user.username})"

    
class JobPosting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_postings')
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255, blank=True)
    raw_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} at {self.company}"
    
class MatchResult(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='match_results')
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='match_results')
    match_score = models.FloatField()
    gap_analysis = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.resume.title} vs {self.job_posting.title}: {self.match_score}"
