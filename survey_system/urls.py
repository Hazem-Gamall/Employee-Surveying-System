from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('',views.SurveyViewSet)

urlpatterns = router.urls

