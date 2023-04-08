from django.contrib import admin

# Register your models here.
from .models import Meta

class MetaAdmin(admin.ModelAdmin):
    list_display = ['id', 'meta_key']

admin.site.register(Meta,MetaAdmin)