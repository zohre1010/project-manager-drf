from django.contrib import admin
from django.contrib.auth import get_user_model
from accounts_app.models import OtpCode

USER = get_user_model()


@admin.register(USER)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'phone_number', 'full_name']

admin.site.register(OtpCode)