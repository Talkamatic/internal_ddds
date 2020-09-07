# -*- coding: utf-8 -*-
from tala.model.device import DeviceAction, DddDevice, EntityRecognizer


class NavigationDevice(DddDevice):
    class NavigateToDestination(DeviceAction):
        def perform(self):
            return True

    class MockAction(DeviceAction):
        def perform(self, common_predicate):
            return True

    class SetDepartureDay(DeviceAction):
        def perform(self, departure_day):
            return True

    class MockEntityRecognizer(EntityRecognizer):
        def recognize(self, string, language):
            if string.lower() == "johanneberg":
                return [{"sort": "common_sort", "grammar_entry": "johanneberg"}]
            else:
                return []
