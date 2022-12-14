from django.contrib import admin
from participant.models import SolveLog


@admin.register(SolveLog)
class SolveLogAdmin(admin.ModelAdmin):
    '''Admin View for SolveLog'''

    list_display = (
        'participant',
        'level',
        'solved_count',
        'partial_solved_count',
        'tried_count',
        'exp',
        'standard_date',
    )
    list_filter = (
        'participant',
        'standard_date',
    )
    search_fields = (
        'participant__boj_handle',
    )
    ordering = (
        'participant__boj_handle',
        'standard_date',
    )
