from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet

from . import views


router = DefaultRouter()
router.register(r'tasks', TaskViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('suggestions/', views.TaskSuggestionView.as_view()),
]
