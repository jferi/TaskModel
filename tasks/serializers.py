from django.utils import timezone
from rest_framework import serializers
from .models import TaskModel


class TaskSerializer(serializers.ModelSerializer):
    """
        Serializer for TaskModel objects, providing serialization and validation for task data.

        The serializer ensures that:
        - The title is not empty upon task creation.
        - The due date is not set in the past.
        - Task status transitions adhere to predefined rules.
        """
    due_date = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S', required=False, allow_null=True)

    class Meta:
        model = TaskModel  # Define the model associated with this serializer
        fields = '__all__'  # Include all fields from the model in the serialization
        read_only_fields = ['creation_date']  # Make creation_date read-only

    def validate(self, data):
        """
        Validates that the title is provided for new task creation.
        """
        if not self.instance:  # creation
            title = data.get('title', '').strip()
            if not title:
                raise serializers.ValidationError({"title": "Title is required."})
        return data

    def validate_due_date(self, value):
        """
        Validate due_date field in TaskModel for update and create operations based on current time zone.
        """
        if value and value < timezone.now():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value

    def validate_status(self, value):
        """
        Validate status field in TaskModel for update operations based on previous statuses.
        """
        if self.instance:
            current_status = self.instance.status
            if current_status == 'completed' and value not in ['completed', 'in_progress']:
                raise serializers.ValidationError("Completed tasks can only remain completed or move to in progress.")
            elif current_status == 'in_progress' and value not in ['completed', 'in_progress']:
                raise serializers.ValidationError(
                    "In-progress tasks can only be set to completed or remain in progress.")
            elif current_status == 'pending' and value == 'expired':
                raise serializers.ValidationError("Pending tasks cannot be directly set to expired.")
        return value
