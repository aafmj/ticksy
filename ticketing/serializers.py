from django.db.models import Q
from django.utils import timezone
from rest_framework import serializers

from ticketing.models import Topic
from users.models import IDENTIFIED, User
from users.serializers import UserSerializer

CREATOR = '1'
SUPPORTER = '2'


class TopicSerializer(serializers.ModelSerializer):
    supporters_ids = serializers.PrimaryKeyRelatedField(source='supporters', queryset=User.objects.filter(
        Q(identity__status=IDENTIFIED) & (
                Q(identity__expire_time__isnull=True) | Q(identity__expire_time__gt=timezone.now()))),
                                                        write_only=True, many=True, required=False)
    role = serializers.SerializerMethodField()
    creator = UserSerializer(read_only=True)
    supporters = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Topic
        fields = ['id', 'creator', 'role', 'title', 'description', 'slug', 'avatar', 'supporters',
                  'supporters_ids']
        read_only_fields = ['id', 'creator', 'role', 'is_active', 'url', 'supporters']

    def get_role(self, obj):
        if self.context['request'].user == obj.creator:
            return CREATOR
        return SUPPORTER

    def validate_supporters_ids(self, value):
        supporters = value
        user = self.context['request'].user
        if user in supporters:
            supporters.remove(user)
        return supporters

    # def create(self, validated_data):
    #     instance = super().create(validated_data)
    #     user = self.context['request'].user
    #     instance.creator = user
    #     instance.save()
    #     return instance