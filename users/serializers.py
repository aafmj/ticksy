from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from users.models import User


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
