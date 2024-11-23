from abc import ABC, abstractmethod


class ICallRepository(ABC):

    @abstractmethod
    def insert_call():
        raise NotImplementedError

    @abstractmethod
    def get_call():
        raise NotImplementedError

    @abstractmethod
    def update_call():
        raise NotImplementedError

    @abstractmethod
    def get_billing():
        raise NotImplementedError
