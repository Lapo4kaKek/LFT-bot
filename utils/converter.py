from eth_utils import from_wei, to_wei
from datetime import datetime

class Converter:
    @staticmethod
    def hex_to_big(hex_value: str) -> int:
        """Конвертирует шестнадцатеричное значение в десятичное."""
        return int(hex_value, 16)


    @staticmethod
    def wei_to_eth(wei_value: int) -> float:
        """Конвертирует значение из wei в Ether."""
        return from_wei(wei_value, 'ether')

    @staticmethod
    def eth_to_wei(eth_value: float) -> int:
        """Конвертирует значение из Ether в wei."""
        return to_wei(eth_value, 'ether')

    @staticmethod
    def hex_to_eth(hex_value: str) -> float:
        """Конвертирует шестнадцатеричное значение сразу в Ether."""
        wei_value = Converter.hex_to_big(hex_value)
        return Converter.wei_to_eth(wei_value)

    def format_time_to_datetime(timestamp_str):
        return datetime.fromtimestamp(int(timestamp_str) / 1000)

