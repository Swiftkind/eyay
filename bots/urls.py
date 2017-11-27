from django.conf.urls import url

from .views import BotListCreateView, BotRetrieveUpdateDestroyView


urlpatterns = [
    url(r'^api/bots/$', BotListCreateView.as_view(), name='bots-api'),
    url(r'^api/bots/(?P<pk>[0-9]+)/$', BotRetrieveUpdateDestroyView.as_view(), name='bot-detail')
]
