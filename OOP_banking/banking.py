next_acc = 1001

def unique_acc():
    global next_acc
    acc_no = next_acc
    next_acc += 1
    return acc_no

acc_DB = {} # kwy = account number, value = Acc object

class Bankacc:
    def __init__(self, acc_holder, balance=0):
        self.acc_no = unique_acc()
        self.acc_holder = acc_holder
        self.__balance = balance

        self.is_active = True
        self.transaction_history = []

    def log_transaction(self, type, amt, details=""):
        self.transaction_history.append({
            "type": type,
            "amt": amt,
            "details": details
        })

    def get_balance(self):
        return self.__balance

    def deposit(self, amt):
        if not self.is_active:
            print("Operation failed: acc is inactive.")
            return
        if amt > 0:
            self.__balance += amt
            self.log_transaction("Deposit", amt)
            print(f"Deposit successful. New balance: ${self.__balance:.2f}")
        else:
            print("Deposit amt must be positive.")

    def withdraw(self, amt):
        if not self.is_active:
            print("Operation failed: acc is inactive.")
            return
        if amt > 0:
            if amt <= self.__balance:
                self.__balance -= amt
                self.log_transaction("Withdrawal", amt)
                print(f"Withdrawal successful. New balance: ${self.__balance:.2f}")
                return True
            else:
                print("Insufficient funds!")
                return False
        else:
            print("Withdrawal amt must be positive.")
            return False

    def transfer(self, amt, target_acc):
        if not isinstance(target_acc, Bankacc):
            print("Transfer failed: Target is not a valid bank acc object.")
            return

        if self.withdraw(amt):
            target_acc.deposit(amt)
            self.log_transaction("Transfer Out", amt, f"to Acc {target_acc.acc_no}")
            target_acc.log_transaction("Transfer In", amt, f"from Acc {self.acc_no}")
            print(f"Transfer of ${amt:.2f} successful to acc {target_acc.acc_no}.")
        else:
            print("Transfer failed due to withdrawal restrictions.")

    def get_details(self):
        status = "Active" if self.is_active else "Inactive"
        return (
            f"--- acc Details ---\n"
            f"Holder: {self.acc_holder}\n"
            f"Number: {self.acc_no}\n"
            f"Type: {self.__class__.__name__}\n"
            f"Balance: ${self.__balance:.2f}\n"
            f"Status: {status}\n"
            # f"Created: {self.created_at.strftime('%Y-%m-%d')}\n"
        )

    def view_history(self):
        print(f"\n--- Transaction History for acc {self.acc_no} ---")
        if not self.transaction_history:
            print("No transactions recorded.")
            return
        for t in self.transaction_history:
            print(f"[{t['timestamp']}] {t['type']:<15} ${t['amt']:<10.2f} {t['details']}")
        print("------------------------------------------")

    def close_acc(self):
        if self.__balance == 0:
            self.is_active = False
            print(f"acc {self.acc_no} for {self.acc_holder} has been marked as INACTIVE.")
        else:
            print(f"acc {self.acc_no} cannot be closed. Balance must be $0.00.")

class Savingsacc(Bankacc):
    intr_rate = 0.04  # 4% annually

    def calculate_intr(self):
        if not self.is_active:
            print("Cannot apply interest to an inactive acc.")
            return

        interest = self.get_balance() * self.intr_rate
        self.deposit(interest)
        self.log_transaction("intr Applied", interest)
        print(f"Annual intr of ${interest:.2f} applied.")

    def get_details(self):
        base_details = super().get_details()
        return f"{base_details}intr Rate: {self.intr_rate * 100:.1f}%\n"

class Currentacc(Bankacc):
    def __init__(self, acc_holder, balance=0, overdraft_limit=500):
        super().__init__(acc_holder, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amt):
        if not self.is_active:
            print("Operation failed: acc is inactive.")
            return

        if amt > 0:
            current_balance = self.get_balance()
            new_balance_after_withdrawal = current_balance - amt

            if new_balance_after_withdrawal >= -self.overdraft_limit:
                self._Bankacc__balance = new_balance_after_withdrawal
                self.log_transaction("Withdrawal", amt)
                print(f"Withdrawal successful. New balance: ${self.get_balance():.2f}")
                return True
            else:
                available_to_withdraw = current_balance + self.overdraft_limit
                print(f"Overdraft Limit Exceeded. Max withdrawal remaining: ${available_to_withdraw:.2f}")
                return False
        else:
            print("Withdrawal amt must be positive.")
            return False

    def get_details(self):
        base_details = super().get_details()
        return f"{base_details}Overdraft Limit: ${self.overdraft_limit:.2f}\n"

class Employee:
    def __init__(self, staff_id, name):
        self.staff_id = staff_id
        self.name = name

    def get_info(self):
        return f"Employee ID: {self.staff_id}, Name: {self.name}"


class Manager(Employee):
    def __init__(self, staff_id, name, loan_limit):
        super().__init__(staff_id, name)
        self.loan_limit = loan_limit

    def approve_loan(self, acc, amt):
        if amt <= self.loan_limit and amt > 0 and acc.is_active:
            acc.deposit(amt)
            acc.log_transaction("Loan Approved", amt, f"by Manager {self.name}")
            print(f"\n--- LOAN APPROVED ---")
            print(f"Loan of ${amt:.2f} approved by {self.name} for acc {acc.acc_no}.")
            print(f"New Balance: ${acc.get_balance():.2f}")
            return True
        elif not acc.is_active:
            print("Loan failed: acc is inactive.")
            return False
        else:
            print(f"Loan amt ${amt:.2f} exceeds manager limit of ${self.loan_limit:.2f}.")
            return False

BANK_MANAGER = Manager("MGR001", "Mr. Sterling", 50000.00)


def search_acc(prompt="Enter acc number: "):
    try:
        acc_num = int(input(prompt))
        acc = acc_DB.get(acc_num)
        if acc:
            return acc
        else:
            print("Error: acc not found.")
            return None
    except ValueError:
        print("Error: Invalid acc number format.")
        return None


def create_new_acc():
    holder = input("Enter acc holder's full name: ")
    print("Select acc type:")
    print("  1. Current acc (Checking with Overdraft equal to 500)")
    print("  2. Savings acc (interest bearing)")
    choice = input("Enter choice (1 or 2): ")

    initial_balance = float(input("Enter initial deposit amt (0 or more): "))


    if choice == '1':
        new_acc = Currentacc(holder, initial_balance)
    elif choice == '2':
        new_acc = Savingsacc(holder, initial_balance)
    else:
        print("Invalid choice. acc creation aborted.")
        return

    acc_DB[new_acc.acc_no] = new_acc
    print("\n--- acc CREATED SUCCESSFULLY ---")
    print(f"acc Number: {new_acc.acc_no}")
    print(f"acc Type: {new_acc.__class__.__name__}")
    print(f"Initial Balance: ${new_acc.get_balance():.2f}")


def deposit_money():
    acc = search_acc()
    if acc:
        try:
            amt = float(input("Enter deposit amt: "))
            acc.deposit(amt)
        except ValueError:
            print("Invalid amt.")


def withdraw_money():
    acc = search_acc()
    if acc:
        try:
            amt = float(input("Enter withdrawal amt: "))
            acc.withdraw(amt)
        except ValueError:
            print("Invalid amt.")


def view_acc_details():
    acc = search_acc()
    if acc:
        print(acc.get_details())
        acc.view_history()


def perform_transfer():
    print("\nTRANSFER INITIATION")
    source_acc = search_acc("Enter SOURCE acc number: ")
    if not source_acc: return

    target_acc = search_acc("Enter TARGET acc number: ")
    if not target_acc: return

    if source_acc.acc_no == target_acc.acc_no:
        print("Transfer failed: Cannot transfer money to the same acc.")
        return

    amt = float(input("Enter transfer amt: "))
    source_acc.transfer(amt, target_acc)


def run_admin_actions():
    print("\nADMIN ACTIONS")
    print("1. Apply Savings interest")
    print("2. Approve Loan")

    choice = input("Enter choice (1 or 2): ")
    if choice == '1':
        acc = search_acc()
        if acc and isinstance(acc, Savingsacc):
            acc.calculate_intr()
        elif acc:
            print(f"acc {acc.acc_no} is not a Savingsacc.")
    elif choice == '2':
        acc = search_acc()
        if acc:
            try:
                print(f"Manager {BANK_MANAGER.name} limit: ${BANK_MANAGER.loan_limit:.2f}")
                amt = float(input("Enter loan amt: "))
                BANK_MANAGER.approve_loan(acc, amt)
            except ValueError:
                print("Invalid amt.")
    else:
        print("Invalid admin choice.")


def run_close_acc():
    acc = search_acc()
    if acc:
        acc.close_acc()


def list_all_accounts():
    if not acc_DB:
        print("No accounts found.")
        return

    print("\n--- All Account Details ---\n")

    # Define fixed widths for each column
    col_widths = {
        "acc_no": 8,
        "holder": 25,
        "type": 15,
        "balance": 8,
        "status": 15
    }

    # Header
    header = (
        f"{'Acc No'.ljust(col_widths['acc_no'])}"
        f"{'Holder'.ljust(col_widths['holder'])}"
        f"{'Type'.ljust(col_widths['type'])}"
        f"{'Balance'.rjust(col_widths['balance'])}  "
        f"{'Status'.ljust(col_widths['status'])}"
    )
    print(header)
    print("-" * sum(col_widths.values()))

    # Rows
    for acc in acc_DB.values():
        status = "Active" if acc.is_active else "Inactive"
        balance = acc.get_balance()
        print(
            f"{str(acc.acc_no).ljust(col_widths['acc_no'])}"
            f"{acc.acc_holder.ljust(col_widths['holder'])}"
            f"{acc.__class__.__name__.ljust(col_widths['type'])}"
            f"{balance:,.2f}".ljust(col_widths['balance']) + ""
            f"{status.ljust(col_widths['status'])}"
        )

    print("-" * sum(col_widths.values()))




def display_menu():
    print("\n--- Welcome to Python Bank System ---")
    print("1. Create New acc")
    print("2. Deposit Money")
    print("3. Withdraw Money")
    print("4. View acc Details & History")
    print("5. Perform Transfer")
    print("6. Admin / Manager Actions (interest/Loan)")
    print("7. Close acc")
    print("8. List All Accounts")
    print("9. Exit")


def main():
    acc_alice = Currentacc("Alice Johnson", 2000, 1000)
    acc_bob = Savingsacc("Bob Smith", 500)
    acc_DB[acc_alice.acc_no] = acc_alice
    acc_DB[acc_bob.acc_no] = acc_bob

    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            create_new_acc()
        elif choice == '2':
            deposit_money()
        elif choice == '3':
            withdraw_money()
        elif choice == '4':
            view_acc_details()
        elif choice == '5':
            perform_transfer()
        elif choice == '6':
            run_admin_actions()
        elif choice == '7':
            run_close_acc()
        elif choice == '8':
            list_all_accounts()
        elif choice == '9':
            print("Thank you for using the Python Bank System.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")


if __name__ == "__main__":
    main()