import time

def get_timestamp(format="%H:%M:%S"):
    return time.strftime(format, time.localtime())

def is_valid_log_level(level, valid_levels):
    return level.upper() in valid_levels