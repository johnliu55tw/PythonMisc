#!/usr/bin/env python3
import unittest
import sys
sys.path.append("../")

import packetutils


class Test_packetutils(unittest.TestCase):

    def setUp(self):
        self.rawData = b"";
        self.correctData = list()
        correctFlag = False
        with open("testData", "r") as f:
            while True:
                line = f.readline().strip()

                if line == "":
                    break
                elif line.startswith("# CorrectData"):
                    correctFlag = True
                elif line.startswith("#"):
                    correctFlag = False
                else:
                    data = bytes.fromhex(line)
                    self.rawData += data
                    if correctFlag:
                        self.correctData.append(data)

    def test_packetutils(self):
        print("raw:", self.rawData[40:60].hex())
        self.assertEqual(self.correctData,
                         packetutils.FindValidPackets(
                             self.rawData,
                             b"snp",
                             lengthIndex=4,
                             lengthOffset=6,
                             ChksumIncludeHeader=True)[0])

if __name__ == "__main__":
    unittest.main()
