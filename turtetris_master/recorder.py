import os
import json
import time
import copy
from random import randrange

STORAGE = "/usr/share/turtetris"
MAX_RECORDS = 100


def recorded_minimum():
    "Returns tupple with minimal recorded scores and its respective file"
    if not os.path.isdir(STORAGE):
        return False
    records = os.listdir(STORAGE)
    if len(records) < MAX_RECORDS:
        return False
    smin = 0
    min_file = None
    for record in records:
        with open(os.path.join(STORAGE, record)) as file:
            score = int(file.readline())
            if not min_file or smin > score:
                smin = score
                min_file = record
    return (smin, min_file)


class Recorder:
    "Game recorder"

    def __init__(self, matrix):
        self._matrix = matrix
        self._init_state = matrix.copy_matrix()
        self._prev_state = matrix.copy_matrix()
        self._changes = list()
        self._times = list()
        self._start_time = time.time()

    def tick(self):
        "Store one tick"
        change = self._matrix.matrix_diff(self._prev_state)
        if change:
            self._changes.append(change)
            self._times.append(time.time() - self._start_time)
        self._prev_state = self._matrix.copy_matrix()

    def store(self, score):
        "Store this recording to permanent storage"
        rmin = recorded_minimum()
        if rmin and rmin[0] > score:
            return  # Don't store this one
        if not os.path.isdir(STORAGE):
            os.makedirs(STORAGE)
        data = {
            "init": self._init_state,
            "changes": self._changes,
            "times": self._times
            }
        with open(os.path.join(STORAGE, str(int(time.time()))), 'w') as file:
            file.write(str(score) + '\n')
            file.write(json.dumps(data))
        if rmin:  # If we have some marked as minimal then remove it
            os.remove(os.path.join(STORAGE, rmin[1]))


class Replayer:
    "Game records loader and replayer"
    def __init__(self, matrix):
        self._matrix = matrix
        self._changes = None
        self._times = None

        replayes = os.listdir(STORAGE)
        if len(replayes) > 0:
            reply = replayes[randrange(len(replayes))]
            with open(os.path.join(STORAGE, reply)) as file:
                file.readline()
                data = json.loads(file.read())
                self._changes = copy.deepcopy(data['changes'])
                self._times = copy.deepcopy(data['times'])
                self._matrix.set_matrix(data['init'])
                self._matrix.display()

        self._start_time = time.time()
        self._index = 0

    def tick(self):
        "Run recorded tick"
        if not self._changes:
            return False
        while self._index < len(self._times) and \
                (time.time() -
                 self._start_time -
                 self._times[self._index]) >= 0:
            self._matrix.matrix_apply_diff(self._changes[self._index])
            self._matrix.display()
            self._index += 1
        return self._index < len(self._times)  # edit when we have no more
