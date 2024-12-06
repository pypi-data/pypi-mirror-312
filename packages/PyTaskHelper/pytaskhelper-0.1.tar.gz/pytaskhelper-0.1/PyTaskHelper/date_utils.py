from datetime import datetime, timedelta

def human_readable_time_delta(past_date):
    """Convert a datetime object to a human-readable time delta."""
    now = datetime.now()
    delta = now - past_date
    if delta.days > 0:
        return f"{delta.days} days ago"
    elif delta.seconds // 3600 > 0:
        return f"{delta.seconds // 3600} hours ago"
    elif delta.seconds // 60 > 0:
        return f"{delta.seconds // 60} minutes ago"
    else:
        return "just now"
