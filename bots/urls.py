from django.conf.urls import url

from .views import (
    ArchiveViewSet,
    BotViewSet,
    KnowledgeViewSet,
    ChatBot,
    ChatBotAppView,
    IndexView,
    AddChatBotView,
    BotDetailView,
    MyBots,
    ArchivedBots,
    Chatbox
    )


urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^bots/$', MyBots.as_view(), name='bots'),
    url(r'^bots/archive/$', ArchivedBots.as_view(), name='bots_archive'),
    url(r'^bots/add/$', AddChatBotView.as_view(), name='addbot'),
    url(r'^bots/(?P<pk>[0-9]+)/$', BotDetailView.as_view(), name='botdetails'),
    url(r'^bots/(?P<pk>[0-9]+)/chat/$', ChatBotAppView.as_view(), name='chat'),
    url(r'^api/bots/get_chatbox/$', Chatbox.as_view(), name='get_chatbox'),
    url(r'^api/bots/archive/$', 
        ArchiveViewSet.as_view({'get': 'list'}), 
        name='bots-archive-list'
        ),
    url(r'^api/bots/archive/(?P<pk>[0-9]+)/$', 
        ArchiveViewSet.as_view({
            'get': 'retrieve', 'put': 'update', 
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
            'get': 'retrieve', 'put': 'update', 
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
            'get': 'retrieve', 'put': 'update', 
            'patch': 'partial_update', 'delete': 'destroy'
            }),
        name='knowledge-detail'
        ),
]
