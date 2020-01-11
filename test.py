import unittest
from threading import Thread

from constants import FILE_NAME, FILE_PATH
from main import KVDS


class TestKVDS(unittest.TestCase):
    def test_create(self):
        kvds = KVDS(filename=FILE_NAME, filepath=FILE_PATH)

        # creating thread
        t1 = Thread(target=kvds.create, args=('Virat', 'Mumbai', 300))
        t2 = Thread(target=kvds.create, args=('Dhoni', 'Chennai', 300))
        t3 = Thread(target=kvds.create, args=('Raina', 'Chennai', 300))

        # starting thread
        t1.start()
        t2.start()
        t3.start()


if __name__ == "__main__":
    unittest.main()
