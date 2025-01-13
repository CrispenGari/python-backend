from django.db import models
from django.utils import timezone
class Todo(models.Model):
    title = models.CharField(max_length=50, null=False)
    created_at = models.DateTimeField(default=timezone.now)
    completed = models.BooleanField(default=False, null=False)

    def __str__(self) -> str:
        return self.title

    def to_json(self):
        return {
            'id': self.id, 'title': self.title,
            'created_at': self.created_at, 'completed': self.completed
        }