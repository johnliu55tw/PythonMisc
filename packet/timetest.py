#!/usr/bin/python3

import timeit

initialization = """
from os import urandom
import packetutils
header = bytes.fromhex("AB02")
lengthIndex = 2
lengthOffset = 4
testData = bytes()
for i in range(1000):
    data = header
    data += bytes([30])
    data += urandom(30)
    data += packetutils.Checksum(data)
    testData += data
    """
statement = """
packetutils.FindValidPackets(testData, header, lengthIndex=lengthIndex, lengthOffset=lengthOffset)
"""

if __name__ == "__main__":
    print(timeit.timeit(stmt=statement, setup=initialization, number=1))


