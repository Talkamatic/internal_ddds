from tala.model.device import DeviceAction
import mockup_travel.device

class MockupTravelDevice(mockup_travel.device.MockupTravelDevice):
    class CancelReservation(DeviceAction):
        def perform(self):
            self.failure_reason = "no_reservation_exists"
            return False
