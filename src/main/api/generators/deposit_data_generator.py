from random import randint


class DepositDataGenerator:
    @staticmethod
    def amount() -> int:
        return randint(1000, 9000)

    @staticmethod
    def invalid_low_amount() -> int:
        return randint(1, 999)