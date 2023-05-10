from datetime import datetime
import pytz


def time_vn_now():
    current_time = datetime.now()
    VN_TZ = pytz.timezone('Asia/Ho_Chi_Minh')
    current_time = current_time.astimezone(VN_TZ)
    return current_time


def day_now():
    current_time = datetime.now()
    VN_TZ = pytz.timezone('Asia/Ho_Chi_Minh')
    current_time = current_time.astimezone(VN_TZ).strftime('%d-%m-%Y')
    return current_time


def time_now():
    current_time = datetime.now()
    VN_TZ = pytz.timezone('Asia/Ho_Chi_Minh')
    current_time = current_time.astimezone(VN_TZ).strftime('%H:%M:%S')
    return current_time
