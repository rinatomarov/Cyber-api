from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^user/', include('users.urls')),
    url(r'^post/', include('posts.urls')),
    url(r'^pred/', include('prediction.urls')),
    url(r'^log/', include('log_analyze.urls')),
]
