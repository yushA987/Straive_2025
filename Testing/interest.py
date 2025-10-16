class InsufficientBalanceError(Exception):
    pass


class Account:
    def __init__(self, owner, balance=0, annual_rate=0.05):
        self.owner = owner
        self.balance = balance
        self.annual_rate = annual_rate

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientBalanceError("Not enough balance")
        self.balance -= amount
        return self.balance

    def calculate_annual_interest(self):
        return round(self.balance*self.annual_rate, 2)

    def calculate_compound_interest(self, years, compounding_frequency=1):
        P = self.balance
        r = self.annual_rate
        n = compounding_frequency
        t = years
        if t == 0:
            raise ValueError("The year must not be zero")
        if P == 0:
            raise ValueError("Compound Interest cannot be applied when balance is zero")

        A = P*((1 + r/n) ** (n*t))
        return round(A, 2)