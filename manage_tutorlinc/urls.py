from rest_framework import routers
from . views import TeacherViewSet, SubjectViewSet, AddressViewSet, VerificationViewSet, InquiryViewSet, CommentViewSet

router=routers.DefaultRouter()

router.register('teachers', TeacherViewSet, basename='teacher')
router.register('subjects', SubjectViewSet, basename='subject')
router.register('addresses', AddressViewSet, basename='address')
router.register('verifications', VerificationViewSet, basename='verification')
router.register('inquiries', InquiryViewSet, basename='inquiry')
router.register('comments', CommentViewSet, basename='comment')
# router.register('teachers-search', CombinedTeacherView, basename='search')

urlpatterns = router.urls