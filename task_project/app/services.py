# app/services.py
from datetime import timedelta
from django.db import transaction
from django.db.models import F
from .models import Task

@transaction.atomic
def shift_following_tasks(*, project_id: int, threshold_date, diff_days: int, include_self=True):
    """
    threshold_date 以降のタスクを diff_days 日まとめてシフトする。
    include_self=True のときは threshold_date 当日のタスクも含む。
    diff_days は負値でもOK（前倒し）
    """
    if diff_days == 0:
        return 0

    flt = {
        'project_id': project_id,
        'planned_date__gte' if include_self else 'planned_date__gt': threshold_date
    }
    qs = Task.objects.filter(**flt)
    updated = qs.update(planned_date=F('planned_date') + timedelta(days=diff_days))
    return updated
