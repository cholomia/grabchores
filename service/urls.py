from django.conf.urls import url
from rest_framework.routers import DefaultRouter


from service.views import CreateUserView, LoginView, ValidationView

app_name = 'service'

router = DefaultRouter()

urlpatterns = router.urls

urlpatterns += [
    url(r'^user/register/', view=CreateUserView.as_view()),
    url(r'^user/login/', view=LoginView.as_view()),
    url(r'^user/validation/', view=ValidationView.as_view()),

]


