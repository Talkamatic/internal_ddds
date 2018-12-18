from tala.model.device import DddDevice, DeviceAction, DeviceWHQuery, Validity


class RasaTimeDevice(DddDevice):
    class BookFlight(DeviceAction):
        def perform(self, departure_time, return_time):
            return True
