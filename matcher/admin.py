from django.contrib import admin
from .models import Resume, JobPosting, MatchResult

admin.site.register(Resume)
admin.site.register(JobPosting)
admin.site.register(MatchResult)
