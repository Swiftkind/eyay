from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from users import views

urlpatterns = [
	url(r'^(?P<pk>[0-9]+)/$', views.ViewUserDetail.as_view()),
	url(r'^edit_user/(?P<pk>[0-9]+)/$', views.ViewUserDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)