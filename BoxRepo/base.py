
class BoxStatus(object):
    def __init__(self, **kwargs):
        assert "boxID" in kwargs, "'boxID' must be set"
        self.boxID = kwargs.get("boxID")
        self.connected = kwargs.get("connected", False)
        self.inUse = kwargs.get("inUse", False)

    def __repr__(self):
        repr = ""
        repr += "boxID: {}\n".format(self.boxID)
        repr += "connected: {}\n".format(self.connected)
        repr += "inUse: {}\n".format(self.inUse)
        return repr


class BoxRepoBase(object):

    def __init__(self):
        raise NotImplementedError

    def __contains__(self, boxID):
        raise NotImplementedError

    def create(self, boxStatus):
        raise NotImplementedError

    def read(self, boxID=None, **kwargs):
        raise NotImplementedError

    def update(self, boxID, **kwargs):
        raise NotImplementedError

    def delete(self, boxID):
        raise NotImplementedError



