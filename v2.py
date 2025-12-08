from datetime import datetime, timedelta

def timestamp_to_vn(ts):
    """Chuyển Unix timestamp sang giờ Việt Nam bằng cách trừ 7h."""
    try:
        dt = datetime.fromtimestamp(ts) - timedelta(hours=7)
        return dt
    except:
        return datetime.now()
ts = 1764758290
dt_vn = timestamp_to_vn(ts)
print(dt_vn.strftime("%Y-%m-%d %H:%M:%S"))
