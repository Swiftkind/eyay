from django.conf.urls import url, include
from .views import FacebookLogin, GoogleLogin
from django.conf.urls import url
from .views import UserProfile


urlpatterns = [
    url(r'^accounts/', include('allauth.urls')),
    url(r'^api/auth/', include('rest_auth.urls')),
    url(r'^api/auth/registration/', include('rest_auth.registration.urls')),
    url(r'^api/auth/facebook', FacebookLogin.as_view(), name='fb_login'),
    url(r'^api/auth/google', GoogleLogin.as_view(), name='google_login'),
    url(r'^user_profile/', UserProfile.as_view({'get': 'get', 'put': 'update'})),
]