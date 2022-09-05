from django.urls import path

from .views import refresh

urlpatterns = [
    path('refresh/', refresh),
]
