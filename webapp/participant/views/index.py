from datetime import timedelta

from django.shortcuts import render
from django.utils.timezone import now
from participant.models import DailySolveLog, Participant, SolveLog

ABSTRACT_LEVEL_COUNT = 7
LEVEL_COUNT = 31


def level_handler(level):
    if level == 0:
        return level
    else:
        return (level - 1) // 5 + 1


def index(request):
    participants = Participant.objects.all()
    today_solve_logs = DailySolveLog.objects.filter(standard_date=now().date())
    yesterday_daily_solve_log_hash = get_daily_solve_log_hash(days=1)
    yesterday_solve_log_hash = get_solve_log_hash(days=1)
    solve_logs = SolveLog.objects.filter(standard_date=now().date())

    if len(today_solve_logs) == 0:
        # NOTE: 자정 시간에 갱신중인 경우
        today_solve_logs = DailySolveLog.objects.filter(standard_date=now().date() - timedelta(days=1))
        yesterday_daily_solve_log_hash = get_daily_solve_log_hash(days=2)
        yesterday_solve_log_hash = get_solve_log_hash(days=2)
        solve_logs = SolveLog.objects.filter(standard_date=now().date() - timedelta(days=1))

    daily_logs = {}

    for participant in participants:
        daily_logs[participant.id] = {
            'handle': participant.boj_handle,
            'total_solved_count': 0,
            'solved_count': [0] * ABSTRACT_LEVEL_COUNT,
            'is_success': False,
            'standard_problems_count': participant.standard_problems_count
        }

    for today_solve_log in today_solve_logs:
        participant_id = today_solve_log.participant_id
        yesterday_total_solved_count = yesterday_daily_solve_log_hash[participant_id]
        daily_logs[participant_id]['total_solved_count'] = today_solve_log.total_solved_count - yesterday_total_solved_count
        daily_logs[participant_id]['is_success'] = today_solve_log.is_success

    for solve_log in solve_logs:
        level = solve_log.level
        participant_id = solve_log.participant_id
        yesterday_solved_count = yesterday_solve_log_hash[participant_id][level]
        daily_logs[participant_id]['solved_count'][level_handler(level)] += solve_log.solved_count - yesterday_solved_count

    return render(request, 'index.html', {'daily_logs': [*daily_logs.items()], 'participants': participants})


def get_solve_log_hash(days=0):
    ret = {}

    participants = Participant.objects.all()
    solve_logs = SolveLog.objects.filter(standard_date=now().date() - timedelta(days=days))

    for participant in participants:
        ret[participant.id] = [0] * LEVEL_COUNT

    for solve_log in solve_logs:
        ret[solve_log.participant_id][solve_log.level] = solve_log.solved_count

    return ret


def get_daily_solve_log_hash(days=0):
    ret = {}

    daily_solve_logs = DailySolveLog.objects.filter(standard_date=now().date() - timedelta(days=days))

    for daily_solve_log in daily_solve_logs:
        ret[daily_solve_log.participant_id] = daily_solve_log.total_solved_count

    return ret
