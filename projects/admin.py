from django.contrib import admin
from . models import Project,Task,Note
# Register your models here.

class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']

class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']

class NoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'project']

admin.site.register(Project,ProjectAdmin)
admin.site.register(Task,TaskAdmin)
admin.site.register(Note,NoteAdmin)