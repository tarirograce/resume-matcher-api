from rest_framework.routers import DefaultRouter
from .views import ResumeViewSet, JobPostingViewSet, MatchResultViewSet

router = DefaultRouter()
router.register(r'resumes', ResumeViewSet, basename='resume')
router.register(r'job-postings', JobPostingViewSet, basename='jobposting')
router.register(r'match-results', MatchResultViewSet, basename='matchresult')

urlpatterns = router.urls