# This file uses encoding: utf8
from tdm.testing.mocked_frontend_device import MockedFrontendDevice


class MockedFrontendDevice(MockedFrontendDevice):
    def receive_event(self, event):
        device_query = event.get_content()
        name = device_query['name']
        if device_query['type'] == "DeviceAction":
            if name == "UpdateClockSoftware":
                return True
        elif device_query['type'] == "DeviceWHQuery":
            if name == "greenwich_mean_time":
                return ["12:00"]
