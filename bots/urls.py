from django.conf.urls import url
from rest_framework import routers

from .views import BotViewSet


router = routers.SimpleRouter()
router.register(r'api/bots', BotViewSet)

urlpatterns = router.urls
