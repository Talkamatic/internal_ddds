from tala.model.device import DddDevice, EntityRecognizer, DeviceAction, Validity, DeviceWHQuery


class AndroidDevice(DddDevice):
    CONTACT_NUMBERS = {
        "John": "0701234567",
        "Lisa": "0709876543",
        "Mary": "0706574839",
        "Andy": None,
    }

    class Call(DeviceAction):
        def perform(self, selected_contact_to_call):
            def call(number):
                # TODO: Implement calling
                pass

            number = self.device.CONTACT_NUMBERS.get(selected_contact_to_call)
            call(number)
            success = True
            return success

    class ContactRecognizer(EntityRecognizer):
        def recognize_entity(self, string):
            result = []
            words = string.lower().split()
            for contact in list(self.device.CONTACT_NUMBERS.keys()):
                if contact.lower() in words:
                    recognized_entity = {"sort": "contact", "grammar_entry": contact}
                    result.append(recognized_entity)
            return result

    class PhoneNumberAvailable(Validity):
        def is_valid(self, selected_contact_to_call):
            number = self.device.CONTACT_NUMBERS.get(selected_contact_to_call)
            if number:
                return True
            return False

    class phone_number_of_contact(DeviceWHQuery):
        def perform(self, selected_contact_of_phone_number):
            number = self.device.CONTACT_NUMBERS.get(selected_contact_of_phone_number)
            number_entity = {"grammar_entry": number}
            return [number_entity]
