from django.contrib import admin
from participant.models import DailySolveLog


@admin.register(DailySolveLog)
class DailySolveLogAdmin(admin.ModelAdmin):
    '''Admin View for DailySolveLog'''

    list_display = (
        'participant',
        'total_solved_count',
        'standard_date',
        'is_success',
    )
    list_filter = (
        'participant',
        'standard_date',
    )
    search_fields = (
        'participant__boj_handle',
    )
    ordering = (
        'standard_date',
    )
