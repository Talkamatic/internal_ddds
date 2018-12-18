import hello_world.device


class HelloWorldDevice(hello_world.device.HelloWorldDevice):
    def __init__(self):
        super(self.__class__, self).__init__()
        self._ringing = True

