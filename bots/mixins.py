from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import get_object_or_404, redirect

from .models import Bot


class UserIsOwnerMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        bot = get_object_or_404(Bot, pk=self.kwargs['pk'])
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        elif request.user != bot.creator:
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)
