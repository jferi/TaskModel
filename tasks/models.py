from django.db import models


class TaskModel(models.Model):
    status_choices = [
        ('completed', 'Already completed'),
        ('pending', 'Still pending'),
        ('in_progress', 'In Progress'),
        ('expired', 'Expired'),
        ('canceled', 'Canceled'),
    ]

    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=status_choices, default='pending')

    def __str__(self):
        return self.title
