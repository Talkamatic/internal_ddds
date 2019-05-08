from tala.model.device import DddDevice, DeviceAction, DeviceWHQuery


class DatetimeDevice(DddDevice):
    class BookFlight(DeviceAction):
        def perform(self, departure_time):
            return True

    class next_arrival_time(DeviceWHQuery):
        def perform(self):
            return ["2018-04-11T22:00:00.000Z"]
