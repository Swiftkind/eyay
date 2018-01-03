from allauth.account.views import confirm_email
from django.conf.urls import url, include
from django.contrib.auth.views import logout as logout_view
from .views import (
    FacebookLogin, 
    GoogleLogin, 
    UserProfileViewSet, 
    UserProfile
    )


urlpatterns = [
    url(r'^accounts/logout/$', logout_view, {'next_page': '/'}),
    url(r'^accounts/profile', UserProfile.as_view(), name='user_profile'),
    url(r'^api/auth/registration/account-confirm-email/(?P<key>[-:\w]+)/$', 
        confirm_email, 
        name="account_confirm_email"
        ),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^api/auth/', include('rest_auth.urls')),
    url(r'^api/auth/registration/', include('rest_auth.registration.urls')),
    url(r'^api/auth/facebook', FacebookLogin.as_view(), name='fb_login'),
    url(r'^api/auth/google', GoogleLogin.as_view(), name='google_login'),
    url(r'^user_profile/', UserProfileViewSet.as_view({'get': 'get', 'put': 'update'})),
]
