from uuid import uuid4
from multiprocessing import Process
from zmq.eventloop import ioloop, zmqstream
import zmq

"""
    Base class for all zmq-socket-event-driven process. It provides the interface
    for setting up the callback function with a zmq socket or an address. It    
    could also add a PeriodicCallback function which acts like an interval
    timer.
"""
class ZMQEventProcess(Process):

    def __init__(self):
        super().__init__()
        self.ctx = None
        self.loop = None

        self.alarms = dict()

        self.timeoutValue = None
        self.timeoutCallback = None
        self.timeoutAlarmUUID = None

        self.lastRecvTime = None

    def _contextSetup(self):
        self.ctx = zmq.Context()
        self.loop = ioloop.ZMQIOLoop()
        self.loop.make_current()
        self.lastRecvTime = self.loop.time()
    
    # The fucntion wrapper to wrap the stream callback function,
    # in order to update the lastRecvTime.
    def _updateLastRecvTime(self, callback):
        def callbackWrapper(msg):
            self.lastRecvTime = self.loop.time()
            callback(msg)
        return callbackWrapper
    
    # The fucntion to check whether the timeout is reached.
    def _checkTimeout(self):
        now = self.loop.time()
        diff = (now - self.lastRecvTime) * 1000
        if diff >= self.timeoutValue:
            self.lastRecvTime = now
            self.resetAlarm(self.timeoutAlarmUUID, interval=self.timeoutValue)
            self.timeoutCallback()
        else:
            self.resetAlarm(self.timeoutAlarmUUID, interval=(self.timeoutValue - diff))

    """
        Must be overriding by the child class to register the socket and
        callback funcion
    """
    def setup(self):
        raise NotImplementedError

    """
        Register an nterval timer callback.
        The return value is an UUID which can be used to unregister the alarm.
    """
    def registerAlarm(self, interval, callback, UUID=None):
        if UUID is None:
            UUID = uuid4()

        if UUID in self.alarms:
            raise KeyError("Alarm UUID already exist")

        self.alarms[UUID] = ioloop.PeriodicCallback(callback, interval)
        self.alarms[UUID].start()
        return UUID

    def unregisterAlarm(self, UUID):
        self.alarms[UUID].stop()
        del self.alarms[UUID]

    def resetAlarm(self, UUID, interval=None, callback=None):
        # Retrieve the original interval and callback function if needed
        if interval is None:
            interval = self.alarms[UUID].callback_time
        if callback is None:
            callback = self.alarms[UUID].callback
        
        # Reset the alarm, using the original UUID
        self.unregisterAlarm(UUID)
        self.registerAlarm(interval, callback, UUID=UUID)

    """
        Register timeout callback
    """
    def registerTimeout(self, timeout, callback):
        self.timeoutValue = timeout
        self.timeoutCallback = callback
        self.timeoutAlarmUUID = self.registerAlarm(timeout, self._checkTimeout)

    """
        Create a zmq socket.
    """
    def socket(self, address, type, *,
            sockopt=dict(),
            bind=False):

        sock = self.ctx.socket(type)
        sock.setsockopt(zmq.LINGER, 0)

        for opt, value in sockopt.items():
            sock.setsockopt(opt, value)

        if bind:
            sock.bind(address)
        else:
            sock.connect(address)

        return sock

    """
        Register an zmq address with type to a callback function.
        This method returns a zmqstream.
    """
    def registerSocket(self, zmqSocket, callback=None):
        stream = zmqstream.ZMQStream(zmqSocket, self.loop)
        if callback is not None:
            callback = self._updateLastRecvTime(callback)
            stream.on_recv(callback)

        return stream
    
    """
        Register an zmq address with type to a callback function.
        This method returns a zmqstream.
    """
    def register(self, address, type, *,
            callback=None, 
            sockopt=dict(),
            bind=False):

        sock = self.socket(address, type, sockopt=sockopt, bind=bind)

        return self.registerSocket(sock, callback)

    """
        Run!
        Note that the class inherit from this class does not have to implement this
        method, just overriding the setup() method.
    """
    def run(self):

        self._contextSetup()
        self.setup()
        self.loop.start()

    def stop(self):
        self.loop.stop()
        self.ctx.destroy()


"""
    Base class for Raw Repo Store
"""
class RawStore(object):

    def __init__(self):
        raise NotImplementedError

    def __call__(self, dataTuples):
        self._store(dataTuples)

    def _store(self, dataTuples):
        raise NotImplementedError


"""
    Addresses of ZMQ sockets
"""
class ZMQAddress(object):
    BOX_ADAPTER_PUB = "ipc:///tmp/box-adapter-pub.ipc"
    BOX_ADAPTER_SUB = "ipc:///tmp/box-adapter-sub.ipc"
    BOX_MGMT_ROUTER = "ipc:///tmp/box-mgmt-router.ipc"
    BOX_MGMT_REP = "ipc:///tmp/box-mgmt-rep.ipc"
    BOX_DISCOVERY_PUB = "ipc:///tmp/box-discovery-pub.ipc"
    RAW_REPO_SUB = "ipc:///tmp/raw-repo-sub.ipc"
    EVT_SVC_SUB = "ipc:///tmp/evt-svc-sub.ipc"
