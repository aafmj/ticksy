from django.urls import path

from users.views import SignupApiView, SigninApiView

urlpatterns = [
    path('signup/', SignupApiView.as_view(), name='user_signup'),
    path('signin/', SigninApiView.as_view(), name='user_signin'),
]
