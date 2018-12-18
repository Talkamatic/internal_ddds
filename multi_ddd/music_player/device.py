# -*- coding: utf-8 -*-
from tala.model.device import DeviceAction, DddDevice, EntityRecognizer, DeviceWHQuery

class MusicPlayerDevice(DddDevice):
    class url_to_play(DeviceWHQuery):
        def perform(self):
            return ["mock_audio_url"]

    class MockAction(DeviceAction):
        def perform(self, common_predicate):
            return True

    class SetVolume(DeviceAction):
        def perform(self, volume):
            return True

    class MockEntityRecognizer(EntityRecognizer):
        def recognize(self, string, language):
            if string.lower() == "linkin park":
                return [{"sort": "common_sort",
                        "grammar_entry": "Linkin Park"}]
            else:
                return []
