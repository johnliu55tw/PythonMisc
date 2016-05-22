#!/usr/bin/python3

import sqlite3
from base import BoxStatus
from base import BoxRepoBase

class DictBoxRepo(BoxRepoBase):

    def __init__(self):
        self.db = dict()

    def __contains__(self, boxID):
        return boxID in self.db

    def create(self, boxStatus):
        if boxStatus.boxID in self:
            raise ValueError("boxID already exist")

        self.db[boxStatus.boxID] = boxStatus

    def read(self, *, boxID=None, connected=None, inUse=None):
        ret = list()
        if boxID is not None:
            try:
                ret.append(self.db[boxID])
                return ret
            except KeyError:
                raise ValueError("boxID not exist")

        else:
            if connected is None and inUse is None:
                for boxStatus in self.db.values():
                    ret.append(boxStatus)
                return ret
            
            else:
                for boxStatus in self.db.values():
                    flag = True

                    if connected is not None:
                        flag = flag and (connected == boxStatus.connected)
                    if inUse is not None:
                        flag = flag and (inUse == boxStatus.inUse)

                    if flag is True:
                        ret.append(boxStatus)

                return ret

    def update(self, *, boxID, connected=None, inUse=None):
        try:
            if connected is not None:
                self.db[boxID].connected = connected

            if inUse is not None:
                self.db[boxID].inUse = inUse
        except KeyError:
            raise ValueError("boxID not exist")
    
    def delete(self, boxID):
        try:
            del self.db[boxID]
        except KeyError:
            raise ValueError("boxID not exist")


class SqliteBoxRepo(BoxRepoBase):

    def __init__(self, dbAddr, schema="./boxrepo.sql"):
        self.db = sqlite3.connect(dbAddr)
        with open(schema) as f:
            self.db.executescript(f.read())

    def __contains__(self, boxID):
        cur = self.db.execute("SELECT boxID FROM boxes")
        cur.row_factory = lambda cur, row: row[0]
        boxIDs = cur.fetchall()
        return boxID in boxIDs

    def create(self, boxStatus):
        try:
            boxID = boxStatus.boxID.hex().upper()
            connected = 1 if boxStatus.connected is True else 0
            inUse = 1 if boxStatus.inUse is True else 0
            self.db.execute("INSERT INTO boxes VALUES(?, ? ,?)",
                    (boxID, connected, inUse))
            self.db.commit()

        except IntegrityError:
            raise ValueError("boxID already exist")

    def read(self, *, boxID=None, connected=None, inUse=None):
        # row factory function to build up the BoxStatus 
        def makeBoxStatus(cur, row):
            return BoxStatus(
                    boxID=bytes.fromhex(row[0]),
                    connected=True if row[1] == 1 else False,
                    inUse=True if row[2] == 1 else False)

        if boxID is not None:
            cur = self.db.execute("SELECT * FROM boxes WHERE boxID = ?",
                    (boxID.hex().upper(), ))
            cur.row_factory = makeBoxStatus
            ret = cur.fetchall()
            if len(ret) == 0:
                raise ValueError("boxID not exist")
            else:
                return ret

        else:
            query = ""
            if connected is None and inUse is None:
                query = "SELECT * FROM boxes"
            
            else:
                query = "SELECT * FROM boxes WHERE "
                conditions = list()
                if connected is not None:
                    conditions.append("connected = {}".format(
                        "1" if connected is True else "0"))

                if inUse is not None:
                    conditions.append("inUse = {}".format(
                        "1" if inUse is True else "0"))

                queries += " AND ".join(conditions)

            cur = self.db.execute(query)
            cur.row_factory = makeBoxStatus
            ret = cur.fetchall()
            return ret

    def update(self, *, boxID, connected=None, inUse=None):
        try:
            if connected is not None:
                self.db[boxID].connected = connected

            if inUse is not None:
                self.db[boxID].inUse = inUse
        except KeyError:
            raise ValueError("boxID not exist")
    
    def delete(self, boxID):
        try:
            del self.db[boxID]
        except KeyError:
            raise ValueError("boxID not exist")
