"""
URL configuration for nutriplan_django project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/foods/', include('foods.urls')),
    path('api/gamification/', include('gamification.urls')),
    path('api/users/', include('users.urls')),
    path('api/community/', include('community.urls')),
]

