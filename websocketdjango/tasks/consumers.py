from django.conf import settings
from asgiref.sync import async_to_sync
from channels.consumer import SyncConsumer


class TaskConsumer(SyncConsumer):

    def websocket_connect(self, event):
        self.send({
            'type': 'websocket.accept'
        })
        async_to_sync(self.channel_layer.group_add)(
            settings.TASK_CHANNEL_GROUP,
            self.channel_name,
        )

    def websocket_disconnect(self, event):
        async_to_sync(self.channel_layer.group_discard)(
            settings.TASK_CHANNEL_GROUP,
            self.channel_name,
        )

    def new_tasks(self, event):
        self.send({
            'type': 'websocket.send',
            'text': event['content'],
        })
