from django.contrib import admin

# Register your models here.
from .models import Conversazione,Channel,Message

class ConversazioneAdmin(admin.ModelAdmin):
    list_display = ['id', 'project','from_user','is_reply']

class ChannelAdmin(admin.ModelAdmin):
    list_display = ['id','admin']

class MessageAdmin(admin.ModelAdmin):
    list_display = ['id','from_user']

admin.site.register(Conversazione,ConversazioneAdmin)
admin.site.register(Channel,ChannelAdmin)
admin.site.register(Message,MessageAdmin)