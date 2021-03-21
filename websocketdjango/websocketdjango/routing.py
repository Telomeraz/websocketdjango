from django.urls import path
from django.conf.urls import url

from channels.routing import ProtocolTypeRouter, URLRouter
from tasks.consumers import TaskConsumer

application = ProtocolTypeRouter({
    "websocket": URLRouter([
        path("tasks/", TaskConsumer()),
    ]),
})
