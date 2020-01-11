import time

FILE_NAME = 'dataStore.json'
FILE_PATH = None
BASE_OBJECT = []
MAX_FILE_SIZE = 1000  # In bytes


def epoch_time_stamp(timestamp):
    # Retun epoch time stamp
    epoch = time.mktime(timestamp.timetuple())
    return int(epoch)
