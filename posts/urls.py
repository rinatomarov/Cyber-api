from django.urls import path
from .views import Post_view, Cat
# from .views import PredictionView


urlpatterns = [
    path('viewcat', Cat.as_view(), name='cat'),
    path('viewpost', Post_view.as_view(), name='post')
]