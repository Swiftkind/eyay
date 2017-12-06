from django.conf.urls import url

from .views import (
    ArchiveListView,
    ArchiveRUDView,
    BotListCreateView, 
    BotRUDView,
    ChatBot,
    KnowledgeListCreateView,
    KnowledgeRUDView,
    )


urlpatterns = [
    url(r'^api/bots/$', BotListCreateView.as_view(), name='bot-list'),
    url(r'^api/bots/(?P<pk>[0-9]+)/$', BotRUDView.as_view(), name='bot-detail'),
    url(r'^api/bots/(?P<pk>[0-9]+)/chat/$', ChatBot.as_view(), name='chat-with-bot'),
    url(r'^api/bots/archive/$', ArchiveListView.as_view(), name='bots-archive-list'),
    url(r'^api/bots/archive/(?P<pk>[0-9]+)/$', ArchiveRUDView.as_view(), 
        name='bot-archive-detail'),
    url(r'^api/bots/(?P<pk>[0-9]+)/knowledges/$',
        KnowledgeListCreateView.as_view(), name='knowledges-api'),
    url(r'^api/bots/(?P<bot>[0-9]+)/knowledges/(?P<pk>[0-9]+)/$',
        KnowledgeRUDView.as_view(), name='knowledge-detail'),
]
