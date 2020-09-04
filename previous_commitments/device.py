from tala.model.device import DddDevice, DeviceWHQuery


class PreviousCommitmentsDevice(DddDevice):


    class monthly_payment(DeviceWHQuery):
        def perform(self, interest_rate, mortgage_time, mortgage_sum):
            return [2000]
