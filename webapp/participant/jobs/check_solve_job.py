from datetime import timedelta

import requests
from django.db import transaction
from django.utils.timezone import now
from participant.models import DailySolveLog, Participant, SolveLog


class CheckSolveJob:
    def __init__(self, category):
        self.category = category
        if self.category == 'hour':
            self.standard_date = now().date()
            self.previous_date = now().date() - timedelta(days=1)
        else:
            self.standard_date = now().date() - timedelta(days=1)
            self.previous_date = now().date() - timedelta(days=2)

    @transaction.atomic
    def perform(self):
        participants = [*Participant.objects.values_list('id', 'boj_handle')]

        for participant_id, handle in participants:
            self.create_solve_log(participant_id, handle)
            self.check_solve(participant_id)

    def create_solve_log(self, participant_id, handle):
        logs = requests.get(
            'https://solved.ac/api/v3/user/problem_stats',
            params={
                'handle': handle
            },
            headers={
                'Content-Type': 'application/json',
            }
        ).json()

        solve_logs = []
        total_solved_count = 0
        for log in logs:
            total_solved_count += log['solved']
            solve_logs.append(
                SolveLog(
                    participant_id=participant_id,
                    level=log['level'],
                    solved_count=log['solved'],
                    partial_solved_count=log['partial'],
                    tried_count=log['tried'],
                    exp=log['exp'],
                    standard_date=self.standard_date,
                )
            )

        SolveLog.objects.filter(participant_id=participant_id, standard_date=self.standard_date).delete()
        SolveLog.objects.bulk_create(solve_logs)
        daily_solve_log, _created = DailySolveLog.objects.get_or_create(
            participant_id=participant_id,
            standard_date=self.standard_date,
        )
        daily_solve_log.total_solved_count = total_solved_count
        daily_solve_log.save()

    def check_solve(self, participant_id):
        participant = Participant.objects.filter(pk=participant_id).first()

        previous_solve_log = DailySolveLog.objects.filter(
            participant_id=participant_id,
            standard_date=self.previous_date,
        ).first()
        today_solve_log = DailySolveLog.objects.filter(
            participant_id=participant_id,
            standard_date=self.standard_date,
        ).first()

        if participant is None or previous_solve_log is None:
            return

        today_solve_count = today_solve_log.total_solved_count - previous_solve_log.total_solved_count
        if today_solve_count < participant.standard_problems_count:
            today_solve_log.is_success = False
            if self.category == 'daily':
                # NOTE: 하루에 한번만 체크되어야 함.
                participant.failed_days_count += 1
            today_solve_log.save()
            participant.save()


def perform_check_solve_job(category: str):
    job = CheckSolveJob(category)
    job.perform()
