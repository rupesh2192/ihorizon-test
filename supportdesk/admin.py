from django.contrib import admin
# Register your models here.
from django.contrib.admin import ModelAdmin

from supportdesk.models import Request


class CustomAdmin(ModelAdmin):
    exclude = ["deleted_on", "created_on"]


@admin.register(Request)
class RequestAdmin(CustomAdmin):
    list_display = ("summary", "status", "is_high_priority", "assigned_to", "created_by", "created_on")
    list_editable = ["status", "assigned_to"]
