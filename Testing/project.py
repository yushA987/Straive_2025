class Account:
    def __init__(self, owner, balance=0, annual_rate=0):
        self.owner = owner
        self.balance = balance
        self.annual_rate = annual_rate
        self.transaction_history = [(balance, "Initial Balance")]

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self.balance += amount
        self.transaction_history.append((self.balance, f"Deposit {amount}"))
        return self.balance

    def withdraw(self, amount):
        if amount > self.balance:
            raise Exception("Insufficient balance")
        self.balance -= amount
        self.transaction_history.append((self.balance, f"Withdraw {amount}"))
        return self.balance

    def apply_annual_interest(self):
        interest = self.balance * self.annual_rate
        self.balance += interest
        self.transaction_history.append((self.balance, f"Interest Applied {interest:.2f}"))
        return self.balance