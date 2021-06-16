from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import permissions, generics, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from users.models import User
from users.serializers import SignupSerializer, SigninSerializer, UserSerializer


class SignupApiView(generics.CreateAPIView):
    """
    Create a new user with given data and return its token.
    """
    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]  # just for intention be more explicit

    @extend_schema(
        summary="Create a new user",
        responses={
            201: OpenApiResponse(response=SignupSerializer,
                                 description='Created.'),
            400: OpenApiResponse(description='bad request, user exist or yout have to make sure you fill the '
                                             'necessary fields correctly'),
        },
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        user = User.objects.get(email=serializer.validated_data['email'])
        token, created = Token.objects.get_or_create(user=user)
        data = {
            'token': token.key
        }
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class SigninApiView(generics.GenericAPIView):
    permissions = [permissions.AllowAny]  # just for intention be more explicit
    serializer_class = SigninSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class UserInfoApiView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
