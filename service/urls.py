from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from service.views import CreateUserView, LoginView, ValidationView, ClassificationViewSet, JobViewSet, \
    JobApplicationViewSet, ApplicationAcceptView, UserRatingViewSet, ProfileUpdateView, ChangePasswordView

app_name = 'service'

router = DefaultRouter()
router.register(r'classifications', ClassificationViewSet)
router.register(r'jobs', JobViewSet)
router.register(r'applications', JobApplicationViewSet)
router.register(r'ratings', UserRatingViewSet)

urlpatterns = router.urls

urlpatterns += [
    url(r'^user/register/', view=CreateUserView.as_view()),
    url(r'^user/login/', view=LoginView.as_view()),
    url(r'^user/validation/', view=ValidationView.as_view()),
    url(r'^applications-accept/', view=ApplicationAcceptView.as_view()),
    url(r'^profile-update/', view=ProfileUpdateView.as_view()),
    url(r'^user/change-password/', view=ChangePasswordView.as_view())
]
