import pytest
from baking import Account, InsufficientBalanceError


@pytest.fixture
def account():
    return Account("Alice", 100)

@pytest.fixture
def target_account():
    return Account("Bob", 50)


def test_deposit_increases_balance(account):
    new_balance = account.deposit(50)
    assert new_balance == 150
    assert account.balance == 150


def test_deposit_zero_or_negative_raises(account):
    with pytest.raises(ValueError):
        account.deposit(0)
    with pytest.raises(ValueError):
        account.deposit(-10)


def test_withdraw_decreases_balance(account):
    new_balance = account.withdraw(30)
    assert new_balance == 70
    assert account.balance == 70


def test_withdraw_more_than_balance_raises(account):
    with pytest.raises(InsufficientBalanceError):
        account.withdraw(200)


def test_transfer_reduces_source_and_increases_target(account, target_account):
    source_balance, target_balance = account.transfer(target_account, 40)
    assert source_balance == 60
    assert target_balance == 90
    assert account.balance == 60
    assert target_account.balance == 90


def test_transfer_fails_if_insufficient_funds(account, target_account):
    original_source_balance = account.balance
    original_target_balance = target_account.balance

    with pytest.raises(InsufficientBalanceError):
        account.transfer(target_account, 200)

    assert account.balance == original_source_balance
    assert target_account.balance == original_target_balance
