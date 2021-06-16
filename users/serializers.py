import datetime

from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from users.models import User, IDENTIFIED, Identity, REQUESTED


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label='ایمیل',
        write_only=True
    )
    password1 = serializers.CharField(
        label="رمز عبور ۱",
        min_length=6,
        write_only=True,
        help_text="رمز عبور باید حداقل ۶ رقمی باشد"
    )
    password2 = serializers.CharField(
        label="رمز عبور ۲",
        min_length=6,
        write_only=True,
        help_text="رمز عبور باید حداقل ۶ رقمی باشد"
    )
    token = serializers.CharField(
        label="توکن",
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')

        if email and password1 and password2 and (password1 == password2):
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password1)
            if user:
                msg = "کاربر با این مشخصات وجود دارد!"
                raise serializers.ValidationError(msg, code='conflict')
        else:
            msg = "اطلاعات باید کامل و به درستی وارد شود"
            raise serializers.ValidationError(msg, code='authorization')

        return attrs

    def create(self, validated_data):
        """ Create and return a new `user` instance, given the validated data. """
        email = validated_data['email']
        password = validated_data['password1']

        user = User.objects.create_user(email, password)
        return user


class SigninSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label="ایمیل",
        write_only=True
    )
    password = serializers.CharField(
        label="رمز عبور",
        min_length=6,
        write_only=True,
        help_text="رمز عبور باید حداقل ۶ رقمی باشد"
    )
    token = serializers.CharField(
        label="توکن",
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):

    is_identified = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email',
                  'code', 'avatar', 'date_joined', 'is_identified']

    def get_is_identified(self, obj):
        if not hasattr(obj, 'identity'):
            return False
        return obj.identity.status == IDENTIFIED


class UserIdentitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Identity
        fields = ['identifier_image', 'request_time', 'expire_time', 'status']
        read_only_fields = ['request_time', 'expire_time', 'status']

    def update(self, instance, validated_data):
        super(UserIdentitySerializer, self).update(instance, validated_data)
        instance.request_time = datetime.datetime.now()
        instance.expire_time = None
        instance.status = REQUESTED
        instance.save()
        return instance
