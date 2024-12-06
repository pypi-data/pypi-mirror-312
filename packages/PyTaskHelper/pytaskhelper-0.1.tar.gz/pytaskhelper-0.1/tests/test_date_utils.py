from PyTaskHelper.date_utils import human_readable_time_delta
from datetime import datetime, timedelta

def test_human_readable_time_delta():
    past = datetime.now() - timedelta(days=1)
    assert "1 days ago" in human_readable_time_delta(past)
