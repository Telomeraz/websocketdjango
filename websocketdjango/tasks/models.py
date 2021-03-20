from django.conf import settings
from django.db import models


class Task(models.Model):

    STATUSES = (
        ("STARTED", "Started"),
        ("IN PROGRESS", "In progress"),
        ("FINISHED", "Finished"),
    )

    name = models.CharField("Task name", max_length=255, blank=True)

    status = models.CharField("Status", max_length=255, choices=STATUSES)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.status
