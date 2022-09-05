from config.models import BaseModel
from django.db import models


class SolveLog(BaseModel):
    participant = models.ForeignKey(
        'participant.Participant',
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='참가자',
        related_name='solve_logs'
    )
    level = models.IntegerField(
        null=False,
        default=0,
        verbose_name='문제 레벨'
    )
    solved_count = models.IntegerField(
        null=False,
        default=0,
        verbose_name='해당 문제 레벨에서 푼 문제 수'
    )
    partial_solved_count = models.IntegerField(
        null=False,
        default=0,
        verbose_name='해당 문제 레벨에서 부분 성공한 문제 수'
    )
    tried_count = models.IntegerField(
        null=False,
        default=0,
        verbose_name='해당 문제 레벨 시도 횟수'
    )
    exp = models.IntegerField(
        null=False,
        default=0,
        verbose_name='해당 문제 레벨에서 얻은 경험치'
    )
    standard_date = models.DateField(
        null=False,
        verbose_name='해당 로그의 기준 날짜'
    )

    class Meta:
        """Meta definition for SolveLog."""

        verbose_name = 'SolveLog'
        verbose_name_plural = 'SolveLogs'
        db_table = 'solve_logs'
        constraints = [
            models.UniqueConstraint(
                fields=['participant', 'level', 'standard_date'],
                name='unique_date_level_log_by_participant',
            )
        ]
