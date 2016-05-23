#!/usr/bin/python3

from timeit import timeit

SETUP_LOCK = """
from os import urandom
from base import BoxStatus
from boxrepo import DictBoxRepoWithLock as BoxRepo
boxRepo = BoxRepo()
boxRepo.create(BoxStatus(boxID=b"012"))
for i in range(99):
    boxRepo.create(BoxStatus(boxID=urandom(3)))
"""

SETUP = """
from os import urandom
from base import BoxStatus
from boxrepo import DictBoxRepo as BoxRepo
boxRepo = BoxRepo()
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
    
    testNumber = 100000
    print("Test Number = {}".format(testNumber))
    print("Test read time")
    print("Without Lock:")
    print(timeit(stmt=READ_STMT, setup=SETUP, number=testNumber))
    print("With Lock:")
    print(timeit(stmt=READ_STMT, setup=SETUP_LOCK, number=testNumber))

    print("Test update time")
    print("Without Lock:")
    print(timeit(stmt=READ_STMT, setup=SETUP, number=testNumber))
    print("With Lock:")
    print(timeit(stmt=READ_STMT, setup=SETUP_LOCK, number=testNumber))

    print("Test delete time")
    print("Without Lock:")
    print(timeit(stmt=READ_STMT, setup=SETUP, number=testNumber))
    print("With Lock:")
    print(timeit(stmt=READ_STMT, setup=SETUP_LOCK, number=testNumber))
