import pytest
from banking_consistency import Account, InsufficientBalanceError

@pytest.fixture
def accounts():
    alice = Account("Alice", 0)
    bob = Account("Bob", 0)
    return alice, bob

def test_chained_transactions(accounts):
    alice, bob = accounts

    # alice_debit = 0
    # alice_credit = 0

    alice.deposit(2000)
    # alice_credit = alice_credit + 2000

    alice.withdraw(500)
    # alice_debit = alice_debit + 500

    alice.transfer(bob, 1000)
    # alice_debit = alice_debit + 1000

    assert alice.balance == 500
    assert bob.balance == 1000

    assert alice.total_credit == 2000
    assert alice.total_debit == 1500
    assert bob.total_debit == 0
    assert bob.total_credit == 1000
