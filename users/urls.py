from django.urls import path

from users.views import SignupApiView, SigninApiView, UserInfoApiView, IdentityApiView

urlpatterns = [
    path('signup/', SignupApiView.as_view(), name='user_signup'),
    path('signin/', SigninApiView.as_view(), name='user_signin'),
    path('profile/', UserInfoApiView.as_view(), name='user_info'),
    path('identity/', IdentityApiView.as_view(), name='user_identity'),
]
