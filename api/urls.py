# api/urls.py
from django.urls import include, path

urlpatterns = [
    path('users/', include('user.urls')),
    path('tradie/', include('tradie.urls')),
    path('projects/', include('projects.urls'))
]