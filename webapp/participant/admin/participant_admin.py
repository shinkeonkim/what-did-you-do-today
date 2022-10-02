from django.contrib import admin
from participant.jobs.check_solve_job import perform_check_solve_job
from participant.models import DailySolveLog, Participant, SolveLog


def reset(self, request, queryset):
    SolveLog.objects.all().delete()
    DailySolveLog.objects.all().delete()
    Participant.objects.all().update(failed_days_count=0)
    perform_check_solve_job('daily')
    perform_check_solve_job('hour')


def refresh_daily(self, request, queryset):
    perform_check_solve_job('daily')


def refresh_hour(self, request, queryset):
    perform_check_solve_job('hour')


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    '''Admin View for Participant'''
    actions = [reset, refresh_daily, refresh_hour]

    list_display = (
        'boj_handle',
        'failed_days_count',
        'name',
        'paied_failed_days_count',
    )
    search_fields = (
        'boj_handle',
        'failed_days_count',
    )
    ordering = (
        'boj_handle',
        'failed_days_count',
    )
