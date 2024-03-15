from rest_framework.response import Response
from rest_framework import viewsets, status, filters
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from .models import TaskModel
from .serializers import TaskSerializer
from .task_analysis import generate_suggestions


class TaskViewSet(viewsets.ModelViewSet):
    """
     ViewSet for viewing and editing task instances.

     Provides 'list', 'create', 'retrieve', 'update', and 'destroy' actions by default.
     Filtering and ordering of task instances are supported.
     """
    queryset = TaskModel.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'due_date']
    ordering_fields = ['due_date', 'creation_date']


class TaskSuggestionView(APIView):
    """
    APIView for generating task suggestions.

    Analyzes completed tasks and suggests follow-up actions or related tasks based on common keywords.
    """
    def get(self, request, *args, **kwargs):
        """
        Handles GET requests to retrieve task suggestions.

        Returns:
            Response: Contains a list of suggested actions or related tasks.
        """
        suggestions = generate_suggestions()
        return Response({"suggestions": suggestions})
