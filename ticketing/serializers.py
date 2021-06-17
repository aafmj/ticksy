from django.db.models import Q
from django.utils import timezone
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from ticketing.models import Topic, Ticket, Message, Attachment, ANSWERED, WAITING_FOR_ANSWER
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


class TicketSerializer(serializers.ModelSerializer):
    text = serializers.CharField(write_only=True)
    attachments = serializers.ListField(child=serializers.FileField(), write_only=True, required=False)
    creator = UserSerializer(read_only=True)
    topic_slug = serializers.CharField(write_only=True)

    class Meta:
        model = Ticket
        fields = ['id', 'creator', 'title', 'status', 'priority', 'text', 'attachments', 'last_update', 'creation_date',
                  'tags', 'topic_slug']
        read_only_fields = ['id', 'creator', 'status']

    def create(self, validated_data):
        user = self.context['request'].user
        text = validated_data.pop('text')
        attachments = validated_data.pop('attachments', [])
        topic = get_object_or_404(Topic, slug=validated_data.pop('topic_slug'))
        validated_data['creator'] = user
        validated_data['topic'] = topic
        instance = super().create(validated_data)
        message = Message.objects.create(user=user, date=timezone.now(), text=text, ticket=instance)
        for attachment in attachments:
            Attachment.objects.create(message=message, attachmentfile=attachment)
        return instance

    def update(self, instance, validated_data):
        status = validated_data.get('status', None)
        if status:
            instance.status = status
            instance.save()
        return instance


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ['attachmentfile']


class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    attachment_set = AttachmentSerializer(read_only=True, many=True)
    attachments = serializers.ListField(child=serializers.FileField(), write_only=True, required=False)

    class Meta:
        model = Message
        fields = ['id', 'user', 'date', 'rate', 'text', 'attachment_set', 'attachments']
        read_only_fields = ['id', 'user', 'rate', 'date', 'attachment_set']

    def create(self, validated_data):
        attachments = validated_data.pop('attachments', [])
        user = self.context['request'].user
        validated_data['user'] = user
        validated_data['ticket'] = get_object_or_404(Ticket, id=self.context.get('view').kwargs.get('id'))
        instance = super().create(validated_data)
        for attachment in attachments:
            Attachment.objects.create(attachmentfile=attachment, message=instance)
        if instance.user in instance.ticket.topic.supporters.all() or instance.user == instance.ticket.topic.creator:
            instance.ticket.status = ANSWERED
        else:
            instance.ticket.status = WAITING_FOR_ANSWER
        instance.ticket.save()

        return instance
