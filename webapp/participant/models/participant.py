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
    name = models.TextField(
        null=True,
        blank=True,
        verbose_name='이름(임시)'
    )
    standard_problems_count = models.PositiveIntegerField(
        default=1,
        verbose_name='풀어야 하는 문제 수'
    )
    failed_days_count = models.PositiveIntegerField(
        default=0,
        verbose_name='문제 풀이를 실패한 날짜 수'
    )
    paied_failed_days_count = models.PositiveIntegerField(
        default=0,
        null=False,
        blank=False,
        verbose_name='정산된 실패 횟수'
    )

    class Meta:
        """Meta definition for Participant."""

        verbose_name = 'Participant'
        verbose_name_plural = 'Participants'
        db_table = 'participants'

    def __str__(self) -> str:
        return f'[{self.id}] {self.boj_handle}'

    @property
    def monthly_failed_count(self) -> int:
        return self.failed_days_count - self.paied_failed_days_count

    @property
    def money_to_pay(self) -> int:
        return 1000 * (2 ** min(self.monthly_failed_count, 5) - 1) + \
            20000 * max(0, self.monthly_failed_count - 5)
