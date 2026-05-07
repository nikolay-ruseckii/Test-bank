from random import randint


class CreditDataGenerator:
    @staticmethod
    def amount() -> int:
        return randint(5000, 15000)

    @staticmethod
    def term_months() -> int:
        return randint(6, 24)