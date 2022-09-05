from datetime import timedelta

import requests
from django.db import transaction
from django.utils.timezone import now
from participant.models import DailySolveLog, Participant, SolveLog


class CheckSolveJob:
    def __init__(self):
        self.standard_date = now() - timedelta(days=1)
        self.previous_date = now() - timedelta(days=2)

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

        SolveLog.objects.bulk_create(solve_logs)
        DailySolveLog.objects.create(
            participant_id=participant_id,
            total_solved_count=total_solved_count,
            standard_date=self.standard_date,
        )

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
            participant.failed_days_count += 1
            today_solve_log.save()
            participant.save()
