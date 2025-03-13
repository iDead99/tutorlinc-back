from rest_framework import routers
from . views import UserViewset

router=routers.DefaultRouter()

router.register('users', UserViewset, basename='user')

urlpatterns = router.urls