from django.contrib import admin
from .models import Topic, Ticket, Message, Attachment


class AttachInline(admin.TabularInline):
    model = Attachment
    extra = 1


class MessageInline(admin.StackedInline):
    model = Message
    extra = 1
    show_change_link = True


class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'creator')
    search_fields = ['title', 'description', 'slug', 'creator']
    list_filter = []
    filter_horizontal = ['supporters']
    autocomplete_fields = ['creator']


class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_status_display', 'get_priority_display', 'last_update')
    search_fields = ['title', 'creator']
    list_filter = ['status', 'priority', 'creation_date', 'last_update', 'topic']
    readonly_fields = ['creation_date', 'last_update']
    inlines = [MessageInline]
    autocomplete_fields = ['creator', 'topic']


class MessageAdmin(admin.ModelAdmin):
    list_display = ('get_short_text', 'user', 'ticket', 'rate')
    search_fields = ['text', 'user']
    list_filter = ['date', 'rate']
    inlines = [AttachInline]
    readonly_fields = ['date']
    autocomplete_fields = ['user', 'ticket']


# class AttachmentAdmin(admin.ModelAdmin):
#     list_display  = ('message', 'file')
#     list_filter   = []

admin.site.register(Topic, TopicAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Attachment)
# admin.site.register(Attachment, AttachmentAdmin)
