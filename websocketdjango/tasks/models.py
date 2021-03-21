from django.conf import settings
from django.db import models

import json
from asgiref.sync import async_to_sync
import channels.layers


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

    def save(self, *args, **kwargs):
        tasks = {
            "new_task": self.status
        }
        broadcast_tasks(tasks)
        return super(Task, self).save(*args, **kwargs)


def broadcast_tasks(tasks):
    channel_layer = channels.layers.get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        settings.TASK_CHANNEL_GROUP,
        {
            "type": 'new_tasks',
            "content": json.dumps(tasks),
        }
    )
