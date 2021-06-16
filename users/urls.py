from django.urls import path

from users.views import SignupApiView

urlpatterns = [
    path('signup/', SignupApiView.as_view(), name='user_signup'),
]
