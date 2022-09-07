from django.conf import settings
from django.db import IntegrityError
from django.http.response import HttpResponse
from participant.jobs import perform_check_solve_job


def refresh(request):
    refresh_key = request.GET.get('REFRESH_KEY', '')
    category = request.GET.get('category', 'hour')

    try:
        if settings.REFRESH_KEY == refresh_key:
            failed_handles = perform_check_solve_job(category)
            return HttpResponse({'failed_handles': failed_handles}, status=200)
    except IntegrityError:
        return HttpResponse(content='동일한 데이터가 있습니다.', status=401)
    return HttpResponse(content='KEY가 정확하지 않습니다.', status=401)
