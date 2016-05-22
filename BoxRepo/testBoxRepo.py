#!/usr/bin/python3

import unittest
import boxrepo
from base import BoxStatus

class TestBoxRepo(unittest.TestCase):

    def setUp(self):
        self.boxRepo = boxrepo.DictBoxRepo()
        self.boxRepo.create(
                BoxStatus(boxID=b"\x00\x01\x02"))
        self.boxRepo.create(
                BoxStatus(
                        boxID=b"\x01\x02\x03",
                        connected=False,
                        inUse=False))
        self.boxRepo.create(
                BoxStatus(
                        boxID=b"\x02\x03\x04",
                        connected=True,
                        inUse=False))
        self.boxRepo.create(
                BoxStatus(
                        boxID=b"\x03\x04\x05",
                        connected=False,
                        inUse=True))
        self.boxRepo.create(
                BoxStatus(
                        boxID=b"\x04\x05\x06",
                        connected=True,
                        inUse=True))
        self.boxRepo.create(
                BoxStatus(
                        boxID=b"\x05\x06\x07",
                        connected=True,
                        inUse=True))

    def tearDown(self):
        del self.boxRepo
    
    def test_createExistID(self):
        with self.assertRaises(ValueError, msg="boxID already exist"):
            self.boxRepo.create(BoxStatus(boxID=b"\x00\x01\x02"))

    def test_readFromBoxID(self):
        status = self.boxRepo.read(boxID=b"\x00\x01\x02")[0]
        self.assertEqual(status.boxID, b"\x00\x01\x02")
        self.assertEqual(status.connected, False)
        self.assertEqual(status.inUse, False)

    def test_readAll(self):
        result = self.boxRepo.read()
        boxIDset = set(boxStatus.boxID for boxStatus in result)
        self.assertEqual(boxIDset,
            set([b"\x00\x01\x02",
                b"\x01\x02\x03",
                b"\x02\x03\x04",
                b"\x03\x04\x05",
                b"\x04\x05\x06",
                b"\x05\x06\x07"]))

    def test_readByConditions(self):
        result = self.boxRepo.read(connected=True)
        boxIDset = set(boxStatus.boxID for boxStatus in result)
        self.assertEqual(boxIDset,
            set([b"\x02\x03\x04", b"\x04\x05\x06", b"\x05\x06\x07"]))
        for boxStatus in result:
            self.assertTrue(boxStatus.connected)

        result = self.boxRepo.read(inUse=True)
        boxIDset = set(boxStatus.boxID for boxStatus in result)
        self.assertEqual(boxIDset,
            set([b"\x03\x04\x05", b"\x04\x05\x06", b"\x05\x06\x07"]))
        for boxStatus in result:
            self.assertTrue(boxStatus.inUse)
        
        result = self.boxRepo.read(connected=True, inUse=True)
        boxIDset = set(boxStatus.boxID for boxStatus in result)
        self.assertEqual(boxIDset,
            set([b"\x04\x05\x06", b"\x05\x06\x07"]))
        for boxStatus in result:
            self.assertTrue(boxStatus.connected)
            self.assertTrue(boxStatus.inUse)

        result = self.boxRepo.read(connected=True, inUse=False)
        boxIDset = set(boxStatus.boxID for boxStatus in result)
        self.assertEqual(boxIDset,
            set([b"\x02\x03\x04"]))
        for boxStatus in result:
            self.assertTrue(boxStatus.connected)
            self.assertFalse(boxStatus.inUse)

        result = self.boxRepo.read(connected=False, inUse=True)
        boxIDset = set(boxStatus.boxID for boxStatus in result)
        self.assertEqual(boxIDset,
            set([b"\x03\x04\x05"]))
        for boxStatus in result:
            self.assertFalse(boxStatus.connected)
            self.assertTrue(boxStatus.inUse)

        result = self.boxRepo.read(connected=False, inUse=False)
        boxIDset = set(boxStatus.boxID for boxStatus in result)
        self.assertEqual(boxIDset,
            set([b"\x00\x01\x02", b"\x01\x02\x03"]))
        for boxStatus in result:
            self.assertFalse(boxStatus.connected)
            self.assertFalse(boxStatus.inUse)

    def test_updateNotExistID(self):
        with self.assertRaises(ValueError, msg="boxID not exist"):
            self.boxRepo.update(boxID=b"\xFF\x01\x02", connected=True)

    def test_update(self):
        self.boxRepo.update(boxID=b"\x00\x01\x02", connected=True)
        status = self.boxRepo.read(boxID=b"\x00\x01\x02")[0]
        self.assertTrue(status.connected)
        self.assertFalse(status.inUse)

        self.boxRepo.update(boxID=b"\x01\x02\x03", connected=True, inUse=True)
        status = self.boxRepo.read(boxID=b"\x01\x02\x03")[0]
        self.assertTrue(status.connected)
        self.assertTrue(status.inUse)

        self.boxRepo.update(boxID=b"\x02\x03\x04", inUse=True)
        status = self.boxRepo.read(boxID=b"\x02\x03\x04")[0]
        self.assertTrue(status.connected)
        self.assertTrue(status.inUse)

    def test_deleteNotExistID(self):
        with self.assertRaises(ValueError, msg="boxID not exist"):
            self.boxRepo.delete(boxID=b"\xFF\x01\x02")

    def test_delete(self):
        self.boxRepo.delete(boxID=b"\x00\x01\x02")
        with self.assertRaises(ValueError, msg="boxID not exist"):
            self.boxRepo.read(boxID=b"\x00\x01\x02")


if __name__ == "__main__":
    unittest.main()
