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
    search_fields = (
        'participant',
    )
    ordering = (
        'standard_date',
    )
