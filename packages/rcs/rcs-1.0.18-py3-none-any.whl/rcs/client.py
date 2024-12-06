from .base_client import PinnacleBase, AsyncPinnacleBase

from .utils import parse_inbound


class Pinnacle(PinnacleBase):

    @staticmethod
    def parse_inbound_message(
        data: dict,
    ):
        return parse_inbound(data)


class AsyncPinnacle(AsyncPinnacleBase):

    @staticmethod
    def parse_inbound_message(
        data: dict,
    ):
        return parse_inbound(data)
