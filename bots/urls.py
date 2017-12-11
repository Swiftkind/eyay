from django.conf.urls import url

from .views import (
    ArchiveViewSet,
    BotViewSet,
    ChatBot,
    KnowledgeViewSet
    )


urlpatterns = [
    url(r'^api/bots/archive/$', 
        ArchiveViewSet.as_view({'get': 'list'}), 
        name='bots-archive-list'
        ),
    url(r'^api/bots/archive/(?P<pk>[0-9]+)/$', 
        ArchiveViewSet.as_view({
            'get': 'retrieve': 'put': 'update', 
            'patch': 'partial_update', 'delete': 'destroy'
            }), 
        name='bot-archive-detail'
        ),
    url(r'^api/bots/$', 
        BotViewSet.as_view({'get': 'list', 'post': 'create'}), 
        name='bot-list'
        ),
    url(r'^api/bots/(?P<pk>[0-9]+)/$', 
        BotViewSet.as_view({
            'get': 'retrieve': 'put': 'update', 
            'patch': 'partial_update', 'delete': 'destroy'
            }), 
        name='bot-detail'
        ),
    url(r'^api/bots/(?P<pk>[0-9]+)/chat/$', 
        ChatBot.as_view(), 
        name='chat-with-bot'
        ),
    url(r'^api/bots/(?P<bot>[0-9]+)/knowledges/$',
        KnowledgeViewSet.as_view({'get': 'list', 'post': 'create'}), 
        name='knowledges-api'
        ),
    url(r'^api/bots/(?P<bot>[0-9]+)/knowledges/(?P<pk>[0-9]+)/$',
        KnowledgeViewSet.as_view({
            'get': 'retrieve': 'put': 'update', 
            'patch': 'partial_update', 'delete': 'destroy'
            }),
        name='knowledge-detail'
        ),
]
