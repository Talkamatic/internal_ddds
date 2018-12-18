from tala.model.device import DeviceWHQuery
import mockup_travel.device

class MockupTravelDevice(mockup_travel.device.MockupTravelDevice):
    class available_dept_city(DeviceWHQuery):
        def perform(self, dest_city):
            return []

    class num_available_dept_cities(DeviceWHQuery):
        def perform(self, dest_city_grammar_entry):
            return []

    class dept_city(DeviceWHQuery):
        def perform(self):
            return [{"name": "city_helsinki",
                     "confidence": 0.41,
                     "grammar_entry": "Helsinki"}]
