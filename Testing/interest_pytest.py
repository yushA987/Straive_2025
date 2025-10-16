import pytest
from interest import Account, InsufficientBalanceError

@pytest.fixture
def account():
    return Account("Alice", balance=1000, annual_rate=0.05)

def test_simple_interest(account):
    intr = 1000 * 0.05
    assert account.calculate_annual_interest() == round(intr, 2)

def test_compound_interest(account):
    amt = 1000 * ((1 + 0.05/1) ** (1*2))
    assert account.calculate_compound_interest(2, 1) == round(amt, 2)

def test_compound_interest_zero_years(account):
    with pytest.raises(ValueError):
        account.calculate_compound_interest(0, 1)

def test_compound_interest_zero_balance():
    acc = Account("Bob", balance=0, annual_rate=0.05)
    # assert acc.calculate_annual_interest() == 0
    with pytest.raises(ValueError):
        acc.calculate_compound_interest(5, 1) == 0


def test_deposit_increases_balance(account):
    new_balance = account.deposit(50)
    assert new_balance == 1050
    assert account.balance == 1050


def test_deposit_zero_or_negative_raises(account):
    with pytest.raises(ValueError):
        account.deposit(0)
    with pytest.raises(ValueError):
        account.deposit(-10)


def test_withdraw_decreases_balance(account):
    new_balance = account.withdraw(30)
    assert new_balance == 970
    assert account.balance == 970


def test_withdraw_more_than_balance_raises(account):
    with pytest.raises(InsufficientBalanceError):
        account.withdraw(2000)
