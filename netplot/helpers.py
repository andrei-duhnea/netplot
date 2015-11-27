from datetime import datetime
import time

def unique_tenchar():
    return str(int((time.time() + 0.5) * 1000))[-10:]

def timestamp_string():
    return datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M')
