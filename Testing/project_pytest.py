import pytest
from project import Account

def calculate_emi(principal, annual_rate, years):
    r = annual_rate / 12
    n = years * 12
    emi = (principal * r * (1 + r)**n) / ((1 + r)**n - 1)
    return round(emi, 2)

@pytest.fixture
def accounts():
    alice = Account("Alice", 20000, annual_rate=0.06)
    bob = Account("Bob", 20000, annual_rate=0.06)
    charlie = Account("Charlie", 20000, annual_rate=0.06)
    return [alice, bob, charlie]

def test_yearly_transactions_and_transaction_count(accounts):
    for acc in accounts:
        for _ in range(12):
            acc.deposit(500)
        acc.apply_annual_interest()
        acc.withdraw(3000)

    expected_final_balance = 24560
    for acc in accounts:
        assert round(acc.balance, 2) == expected_final_balance
        assert len(acc.transaction_history) == 15

def test_zero_interest_rate():
    acc = Account("ZeroInterest", 10000, annual_rate=0.0)
    acc.deposit(1000)
    acc.apply_annual_interest()
    expected_balance = 11000
    assert acc.balance == expected_balance

def test_negative_interest_rate():
    acc = Account("Penalty", 10000, annual_rate=-0.01)
    acc.apply_annual_interest()
    expected_balance = 10000 * (1 - 0.01)
    assert round(acc.balance, 2) == round(expected_balance, 2)

def test_loan_emis_for_alice_bob_charlie():
    principal = 10000
    annual_rate = 0.05

    # Alice: 1 year loan
    alice_emi = calculate_emi(principal, annual_rate, 1)
    expected_alice_emi = 8560.75
    assert alice_emi == expected_alice_emi

    # Bob: 5 year loan
    bob_emi = calculate_emi(principal, annual_rate, 5)
    expected_bob_emi = 1887.12
    assert bob_emi == expected_bob_emi

    # Charlie: 30 year loan
    charlie_emi = calculate_emi(principal, annual_rate, 30)
    expected_charlie_emi = 536.82
    assert charlie_emi == expected_charlie_emi

    assert alice_emi > bob_emi > charlie_emi
