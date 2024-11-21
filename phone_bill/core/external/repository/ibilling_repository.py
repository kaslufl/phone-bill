from abc import ABC, abstractmethod


class IBillingRepository(ABC):
    
    @abstractmethod
    def get_billing_periods():
        raise NotImplementedError
