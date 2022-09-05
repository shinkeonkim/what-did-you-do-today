from django.contrib import admin
from participant.models import Participant


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    '''Admin View for Participant'''

    list_display = (
        'boj_handle',
        'failed_days_count',
    )
    search_fields = (
        'boj_handle',
        'failed_days_count',
    )
    ordering = (
        'boj_handle',
        'failed_days_count',
    )
