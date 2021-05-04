from django.urls import path, include
from rest_framework import routers
from .views import UploadViewSet, ReturnFile

router = routers.DefaultRouter()
router.register(r'upload', UploadViewSet, basename="upload")

# Wire up our API using automatic URL routing.
urlpatterns = [
    path('', include(router.urls)),
    path('get_file/', ReturnFile.as_view(), name='file'),
]

