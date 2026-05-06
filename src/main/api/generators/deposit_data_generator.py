from random import randint


class DepositDataGenerator:
    @staticmethod
    def amount() -> int:
        return randint(1000, 9000)