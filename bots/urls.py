from django.conf.urls import url

from .views import (
    BotListCreateView,
    BotRetrieveUpdateDestroyView,
    KnowledgeListCreateView,
    KnowledgeRetrieveUpdateDestroyView
    )


urlpatterns = [
    url(r'^api/bots/$', BotListCreateView.as_view(), name='bots-api'),
    url(r'^api/bots/(?P<pk>[0-9]+)/$', BotRetrieveUpdateDestroyView.as_view(), name='bot-detail'),
    url(r'^api/bots/(?P<pk>[0-9]+)/knowledges/$',
        KnowledgeListCreateView.as_view(), name='knowledges-api'),
    url(r'^api/bots/(?P<bot>[0-9]+)/knowledges/(?P<pk>[0-9]+)/$',
        KnowledgeRetrieveUpdateDestroyView.as_view(), name='knowledge-detail')
]
