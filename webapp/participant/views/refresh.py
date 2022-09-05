from django.conf import settings
from django.db import IntegrityError
from django.http.response import HttpResponse
from django.shortcuts import render
from participant.jobs import perform_check_solve_job


def refresh(request):
    try:
        if settings.REFRESH_KEY == request.GET.get('REFRESH_KEY', ''):
            perform_check_solve_job()
            return HttpResponse(status=200)
    except IntegrityError:
        return HttpResponse(content='동일한 데이터가 있습니다.', status=401)
    return HttpResponse(content='KEY가 정확하지 않습니다.', status=401)


def index(request):
    return render(request, 'index.html')
