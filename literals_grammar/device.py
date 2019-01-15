from tala.model.device import DddDevice, DeviceAction


class LiteralsDevice(DddDevice):
    class ShareMedia(DeviceAction):
        def perform(self, comment):
            return True
