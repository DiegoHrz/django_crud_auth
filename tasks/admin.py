from django.contrib import admin
from .models import Task

#para añadir todos los atributos del modelo en el panel incluso los que no veo al inicio porque ya tienen valor x defecto
class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created",)

# Register your models here.
admin.site.register(Task, TaskAdmin)