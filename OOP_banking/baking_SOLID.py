from abc import ABC, abstractmethod
from typing import List, Dict

# === Account Interface (ISP, DIP) ===
class Account(ABC):
    @abstractmethod
    def get_account_number(self) -> int: ...
    @abstractmethod
    def get_holder_name(self) -> str: ...
    @abstractmethod
    def deposit(self, amount: float) -> bool: ...
    @abstractmethod
    def withdraw(self, amount: float) -> bool: ...
    @abstractmethod
    def get_balance(self) -> float: ...
    @abstractmethod
    def is_active(self) -> bool: ...
    @abstractmethod
    def get_account_type(self) -> str: ...
    @abstractmethod
    def get_details(self) -> str: ...
    @abstractmethod
    def close_account(self) -> bool: ...

# === Transaction Logger (SRP) ===
class TransactionLogger:
    def __init__(self):
        self.transactions = []

    def log(self, transaction_type: str, amount: float, details: str = ""):
        self.transactions.append({
            "type": transaction_type,
            "amount": amount,
            "details": details,
        })

    def get_history(self) -> List[Dict]:
        return self.transactions.copy()

# === Base Account class (SRP, LSP) ===
class BankAccount(Account):
    _next_acc_no = 1001

    def __init__(self, acc_holder: str, balance: float = 0):
        self._acc_no = BankAccount._next_acc_no
        BankAccount._next_acc_no += 1

        self._acc_holder = acc_holder
        self._balance = balance
        self._active = True
        self._logger = TransactionLogger()

    def get_account_number(self) -> int:
        return self._acc_no

    def get_holder_name(self) -> str:
        return self._acc_holder

    def is_active(self) -> bool:
        return self._active

    def get_balance(self) -> float:
        return self._balance

    def deposit(self, amount: float) -> bool:
        if not self._active:
            return False
        if amount <= 0:
            return False
        self._balance += amount
        self._logger.log("Deposit", amount)
        return True

    def withdraw(self, amount: float) -> bool:
        if not self._active:
            return False
        if amount <= 0 or amount > self._balance:
            return False
        self._balance -= amount
        self._logger.log("Withdrawal", amount)
        return True

    def get_account_type(self) -> str:
        return self.__class__.__name__

    def get_details(self) -> str:
        status = "Active" if self._active else "Inactive"
        return (
            f"Account Number: {self._acc_no}\n"
            f"Holder: {self._acc_holder}\n"
            f"Type: {self.get_account_type()}\n"
            f"Balance: ${self._balance:.2f}\n"
            f"Status: {status}"
        )

    def close_account(self) -> bool:
        if self._balance == 0:
            self._active = False
            return True
        return False

    def get_transaction_history(self):
        return self._logger.get_history()

# === Savings Account (OCP, LSP) ===
class SavingsAccount(BankAccount):
    interest_rate = 0.04

    def apply_interest(self):
        if not self.is_active():
            return False
        interest = self.get_balance() * self.interest_rate
        self.deposit(interest)
        self._logger.log("Interest Applied", interest)
        return True

    def get_details(self) -> str:
        base = super().get_details()
        return base + f"\nInterest Rate: {self.interest_rate * 100:.2f}%"

# === Current Account with overdraft (OCP, LSP) ===
class CurrentAccount(BankAccount):
    def __init__(self, acc_holder: str, balance: float = 0, overdraft_limit: float = 500):
        super().__init__(acc_holder, balance)
        self._overdraft_limit = overdraft_limit

    def withdraw(self, amount: float) -> bool:
        if not self.is_active():
            return False
        if amount <= 0:
            return False
        if self._balance - amount < -self._overdraft_limit:
            return False
        self._balance -= amount
        self._logger.log("Withdrawal", amount)
        return True

    def get_details(self) -> str:
        base = super().get_details()
        return base + f"\nOverdraft Limit: ${self._overdraft_limit:.2f}"

# === Employee & Manager (SRP, DIP) ===
class Employee:
    def __init__(self, staff_id: str, name: str):
        self._staff_id = staff_id
        self._name = name

    def get_info(self) -> str:
        return f"Employee ID: {self._staff_id}, Name: {self._name}"

class Manager(Employee):
    def __init__(self, staff_id: str, name: str, loan_limit: float):
        super().__init__(staff_id, name)
        self._loan_limit = loan_limit

    def approve_loan(self, account: Account, amount: float) -> bool:
        if amount > self._loan_limit or amount <= 0 or not account.is_active():
            return False
        account.deposit(amount)
        # Assuming logging loan approval in transaction history
        if isinstance(account, BankAccount):
            account._logger.log("Loan Approved", amount, f"by Manager {self._name}")
        return True

# === Bank System (SRP) ===
class BankSystem:
    def __init__(self):
        self.accounts: Dict[int, Account] = {}
        self.manager = Manager("MGR001", "Mr. Sterling", 50000.00)

    def create_account(self, acc_holder: str, acc_type: str, initial_deposit: float) -> Account:
        if acc_type.lower() == "current":
            acc = CurrentAccount(acc_holder, initial_deposit)
        elif acc_type.lower() == "savings":
            acc = SavingsAccount(acc_holder, initial_deposit)
        else:
            raise ValueError("Invalid account type")

        self.accounts[acc.get_account_number()] = acc
        return acc

    def find_account(self, acc_no: int) -> Account | None:
        return self.accounts.get(acc_no)

    def list_accounts(self):
        return list(self.accounts.values())

