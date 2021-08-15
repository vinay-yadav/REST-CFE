from django.contrib import admin
from .models import Status
from .forms import StatusForm


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    # list_display = ['__str__', 'content', 'image']
    list_display = ['user', 'content', 'image']
    form = StatusForm
