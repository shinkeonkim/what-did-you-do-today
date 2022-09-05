from config.models import BaseModel
from django.db import models


class DailySolveLog(BaseModel):
    participant = models.ForeignKey(
        'participant.Participant',
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='참가자',
        related_name='daily_solve_logs'
    )
    total_solved_count = models.IntegerField(
        null=False,
        default=0,
        verbose_name='푼 문제 수'
    )
    standard_date = models.DateField(
        null=False,
        verbose_name='해당 로그의 기준 날짜'
    )
    is_success = models.BooleanField(
        default=True,
    )

    class Meta:
        """Meta definition for SolveLog."""

        verbose_name = 'DailySolveLog'
        verbose_name_plural = 'DailySolveLogs'
        db_table = 'daily_solve_logs'
        constraints = [
            models.UniqueConstraint(
                fields=['participant', 'standard_date'],
                name='unique_daily_log_by_participant',
            )
        ]
