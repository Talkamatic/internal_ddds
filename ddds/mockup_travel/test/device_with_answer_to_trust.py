from tala.model.device import DeviceWHQuery
import mockup_travel.device


class MockupTravelDevice(mockup_travel.device.MockupTravelDevice):
    class dept_city(DeviceWHQuery):
        def perform(self):
            return [{"name": "city_helsinki", "confidence": 1.0, "grammar_entry": "Helsinki"}]
