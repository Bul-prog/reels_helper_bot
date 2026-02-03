from datetime import datetime

from config import FREE_DAILY_LIMIT, PRO_DAILY_LIMIT
from db import update_usage, reset_daily_usage


def check_and_use_limit(user):
    user_id, is_sub, sub_until, daily_used, last_reset = user

    now = datetime.utcnow()
    last_reset_dt = datetime.fromisoformat(last_reset)

    if now.date() != last_reset_dt.date():
        daily_used = 0
        reset_daily_usage(user_id, now.isoformat())

    limit = PRO_DAILY_LIMIT if is_sub else FREE_DAILY_LIMIT

    if daily_used >= limit:
        return False, daily_used, limit

    update_usage(user_id, daily_used + 1)

    return True, daily_used + 1, limit
