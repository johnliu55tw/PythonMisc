#!/usr/bin/python3

from timeit import timeit

SETUP = """
from os import urandom
from base import BoxStatus
from boxrepo import DictBoxRepo
boxRepo = DictBoxRepo()
boxRepo.create(BoxStatus(boxID=b"012"))
for i in range(99):
    boxRepo.create(BoxStatus(boxID=urandom(3)))
"""

READ_STMT = """
boxRepo.read(boxID=b"012")
"""

UPDATE_STMT = """
boxRepo.update(boxID=b"012", connected=True, inUse=False)
"""

DELETE_STMT = """
boxRepo.delete(boxID=b"012")
"""

if __name__ == "__main__":
    print("Test read time")
    print(timeit(stmt=READ_STMT, setup=SETUP, number=10000))

    print("Test update time")
    print(timeit(stmt=READ_STMT, setup=SETUP, number=10000))

    print("Test delete time")
    print(timeit(stmt=READ_STMT, setup=SETUP, number=10000))
