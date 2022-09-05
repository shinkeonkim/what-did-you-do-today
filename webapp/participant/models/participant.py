from config.models import BaseModel
from django.db import models


class Participant(BaseModel):
    user = models.OneToOneField(
        'user.User',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='유저',
        related_name='participant'
    )
    boj_handle = models.TextField(
        null=False,
        blank=False,
        verbose_name='BOJ 핸들'
    )
    standard_problems_count = models.PositiveIntegerField(
        default=1,
        verbose_name='풀어야 하는 문제 수'
    )
    failed_days_count = models.PositiveIntegerField(
        default=0,
        verbose_name='문제 풀이를 실패한 날짜 수'
    )

    class Meta:
        """Meta definition for Participant."""

        verbose_name = 'Participant'
        verbose_name_plural = 'Participants'
        db_table = 'participants'

    def __str__(self) -> str:
        return f'[{self.id}] {self.boj_handle}'
