from tala.model.device import DddDevice, Validity, DeviceAction


class NlgVariationDevice(DddDevice):
    class ContactValidity(Validity):
        def is_valid(self, contact_to_call):
            if contact_to_call == "john":
                return True
            return False

    class ContactAndNumberTypeValidity(Validity):
        def is_valid(self, contact_to_call, number_type_to_call):
            if contact_to_call == "john" and number_type_to_call == "mobile":
                return True
            return False

    class TravelValidity(Validity):
        def is_valid(self, departure_time, destination_city):
            if departure_time == "today":
                return False
            if destination_city == "gothenburg":
                return False
            return True

    class Call(DeviceAction):
        def perform(self, contact_to_call, number_type_to_call):
            return True

    class BookTravel(DeviceAction):
        def perform(self, departure_time, destination_city):
            return True
