from email.mime import base
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('',views.SurveyViewSet, basename='survey-list')
urlpatterns = router.urls

