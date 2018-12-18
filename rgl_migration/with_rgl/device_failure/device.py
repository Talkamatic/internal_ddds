from tala.model.device import DddDevice, EntityRecognizer, DeviceAction


class DeviceFailureDevice(DddDevice):
    class Start(DeviceAction):
        def perform(self):
            return False

    class DeviceFailureRecognizer(EntityRecognizer):
        """Entity recognizer for DeviceFailure"""

        def recognize_entity(self, utterance):
            """Recognize entities in a user utterance.

            This method is responsible for finding all dynamic entities in the utterance. Its accuracy affects the
            behaviour of the dialogue system.

            Since the search is conducted during runtime, particular care should be taken to ensure that the method is
            accurate, robust and has sufficient performance.

            Args:
                utterance (str): The utterance to be searched. For example 'call John'.

            Returns:
                list of dicts: Given the example utterance "call John", the following entity could be returned
                [
                    {
                        "sort": "contact",       # The sort must be declared in the ontology.
                        "grammar_entry": "John", # The grammar entry as it occurred in 'utterance'.
                        "name": "contact_john",  # [optional] Should be a globally unique identifier. Must never be
                                                 # found as is in a user utterance. Use for example the form Sort_ID
                                                 # (e.g. contact_john).
                    },
                ]
            """
            return []
