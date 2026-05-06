from random import randint


class TransferDataGenerator:
    @staticmethod
    def amount() -> int:
        return randint(500, 4000)

    @staticmethod
    def start_balance(transfer_amount: int) -> int:
        return randint(transfer_amount, 9000)

    @staticmethod
    def invalid_high_amount() -> int:
        return 999999