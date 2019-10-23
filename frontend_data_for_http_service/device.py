# -*- coding: utf-8 -*-

from tala.model.device import DddDevice, DeviceAction, DeviceWHQuery


class FrontendDataDevice(DddDevice):

    class GetMockEvent(DeviceAction):
        pass
