from abc import ABC,abstractmethod
from multipledispatch import dispatch

class Bank_Management:
    Total_balance=0
    Total_Loan=0
    Loan_feature=True
    Bank_Rupt=True
    Loged_in=False

    def __init__(self,name,Bank_code,password):
        self.name=name
        self.bank_code=Bank_code
        self.Bank_password=password

    def Loan_Feature_off(self):
        Bank_Management.Loan_feature=False
    
    def Loan_Feature_on(self):
        Bank_Management.Loan_feature=True

    @classmethod
    def bankrupt(cls):
        cls.Bank_Rupt=False

    def __repr__(self):
        print("\t\t ________________________________________")
        print("\t\t|                                        |")
        print(f"\t\t|       {self.name}       |")
        print("\t\t|________________________________________|")
        return ""

class Account(ABC):
    Bank_Account={}
    acc_num=100
    def __init__(self,name,email,phone,Bank_code,address,acctype,password):
        self.name=name
        self.phone=phone
        self.email=email
        self.password=password
        self.Bank_Code=Bank_code
        self.address=address
        self.acctype=acctype
        self.balance=0
        self.Loan=0
        self.transaction_history=[]
        self.log_in=False
        Account.acc_num+=1
        self.account_number=str(f"{self.Bank_Code}{self.acctype}{Account.acc_num}")
        Account.Bank_Account[self.account_number]=self

    def LogIn_Account(self,entered_account_number):
        for account_Number, account_Details in Account.Bank_Account.items():
            if entered_account_number in account_Number:
                self.log_in = True
                return True
        return False

    def LogIn_Password(self,entered_password):
        for account_Number, account_Details in Account.Bank_Account.items():
            if entered_password ==account_Details.password:
                self.log_in = True
                return True
        return False
    
    def Logout(self):
        if self.log_in==True:
            self.log_in=False
            print("\n\tSuccessfully Logout!!")

    def deposit(self,amount):
        if Bank_Management.Bank_Rupt:
            if amount>=0:
                self.balance+=amount
                Bank_Management.Total_balance+=amount
                print(f"\n\tDeposited {amount}. New balance: ${self.balance}")
                self.transaction_history.append(f"\tDeposited History Amount: {amount}")
            else:
                print("\n\tInvalid deposit amount!!\n")
        else:
            print(f"\n\tYou can not deposit!! Your account has been bankrupt.\n")

    def Withdraw(self,amount):
        if Bank_Management.Bank_Rupt:
            if amount>=0 and amount<self.balance:
                self.balance-=amount
                Bank_Management.Total_balance -=amount
                print(f"\tWithdraw {amount}. New Balance: ${self.balance}")
                self.transaction_history.append(f"\tWithdraw Amount: {amount}")

            elif amount>self.balance:
                print("\n\tWithdrawal amount exceeded\n")
            else:
                print("\n\tInvalid withdrawal amount")
        else:
            print("\n\tYou Can not Withdraw!! Your account has been bankrupt.\n")

    def check_available_balance(self):
        print(f"\n\tYour Balance is: {self.balance}")
    
    def check_transaction_history(self):
        if len(self.transaction_history)>0:
            for transaction in self.transaction_history:
                print(transaction)
        else:
            print(f"\n\tNo transaction yet.\n")

    def Loan_amount(self,amount):
        if self.Loan<2 and Bank_Management.Loan_feature:
            self.balance+=amount
            Bank_Management.Total_Loan+=amount
            self.transaction_history.append(f"\tLoan Amount: {amount}")
            self.Loan+=1
            print(f"\tLoan Successfully!!")
        elif not Bank_Management.Loan_feature:
            print("\n\tThe bank does not give any loan now!!")
        else:
            print("\n\tYou took a loan twice!!\n")
    
    def Transfer_money(self, recipient_number, amount):
        recipient_account = Account.Bank_Account.get(recipient_number)
        if recipient_account:
            if amount <= self.balance:
                self.balance -= amount
                recipient_account.balance += amount
                self.transaction_history.append(f"\tTransferred: {amount} To {recipient_number}")
                recipient_account.transaction_history.append(f"\tReceived: {amount} From {self.name}")
                print("\n\tTransfer Successful!!")
            else:
                print("\n\tBalance exceeded!!")
        else:
            print("\n\tRecipient account not found!")


    @dispatch(str)
    def change_info(self,password):
        self.password=password
        print(f"\n\tSuccessfuly Changed!!")

    @abstractmethod
    def show_info(self):
        pass

class SavingsAccount(Account):
    def __init__(self, name, email, phone, Bank_code, address, acctype, password,intarest):
        super().__init__(name, email, phone, Bank_code, address, acctype, password)
        self.intarestRate=intarest

    def Intarest(self):
        intarest=self.balance*(float(self.intarestRate)/100)
        print(f"\n\tYour Intarest Rate is: {self.intarestRate}\n")
        self.deposit(intarest)
        self.transaction_history.append(f"\tIntarest: {intarest}")

    def show_info(self):
        print("\t _______________________")
        print("\t|                       |")
        print(f"\t|      {self.account_number}        |")
        print("\t|_______________________|\n")

        print(f"\tName: {self.name}\n\tEmail: {self.email}\n\tPhone: {self.phone}\n")
        print(f"\tAddress: {self.address}\n\tAccount Tpye: Savings Account\n")
        print(f"\tIntarest Rate: {self.intarestRate}\n\tCurrent Balance: {self.balance}")
        print(f"\tTotal Loan: {self.Loan}\n\tPassword: {self.password}")

class CurrentAccount(Account):
    def __init__(self, name, email, phone, Bank_code, address, acctype, password,limit):
        super().__init__(name, email, phone, Bank_code, address, acctype, password)
        self.limit=int(limit)
    
    def withdraw(self, amount):
        if Bank_Management.Bank_Rupt==True:
            if amount > 0 and (self.balance - amount) >= -self.limit:
                self.balance -= amount
                Bank_Management.Total_balance -=amount
                print(f"\n\tWithdrew $ {amount}. New balance: ${self.balance}")
                self.transaction_history.append(f"\tWithdraw Amount: {amount}")
            else:
                print("\n\tInvalid withdrawal amount or overdraft limit reached")
        else:
            print("\n\tYou Can not Withdraw!! Your account has been bankrupt.\n")

    def show_info(self):
        print("\t _______________________")
        print("\t|                       |")
        print(f"\t|      {self.account_number}        |")
        print("\t|_______________________|\n")

        print(f"\tName: {self.name}\n\tEmail: {self.email}\n\tPhone: {self.phone}")
        print(f"\tAddress: {self.address}\n\tAccount Tpye: Current Account")
        print(f"\tPassword: {self.password}\n\tCurrent Balance: {self.balance}")
        print(f"\tTotal Loan: {self.Loan}")

class Admin(Bank_Management):
    def __init__(self, name,bank_code,password):
        super().__init__(name,bank_code,password)
    
    def Delete_Account(self,account_Number,confirm):
        if len(Account.Bank_Account)>0:
            for acc_number, account_details in Account.Bank_Account.items():
                if account_Number==acc_number:
                    print(f"\n\tName: {account_details.name}")
                    print(f"\tEmail: {account_details.email}")
                    print(f"\tPhone: {account_details.phone}")
                    print(f"\tAddress: {account_details.address}\n")
                    if confirm=="yes":
                        if acc_number in Account.Bank_Account:
                            del Account.Bank_Account[acc_number]
                            print(f"\t{acc_number} account Number is permanenly Delete!!\n")
                            return
                    else:
                        print("\n\tThe account has not been deleted yet!!\n")
                else:
                    print("\n\tInvaild Number! Please, Enter currect Account Number.\n")
        else:
            print("\n\tThere is no account in the bank.\n")

    def show_all_Account(self):
        print(f"\n\tTotal Account: {len(Account.Bank_Account)}\n")
        for acc_number,acc_details in Account.Bank_Account.items():
            print("\t _______________________")
            print("\t|                       |")
            print(f"\t|      {acc_number}        |")
            print("\t|_______________________|\n")
            print(f"\tName: {acc_details.name}\n\tEmail: {acc_details.email}\n\tPhone Number: {acc_details.phone}\n\tAddress: {acc_details.address}")
            print(f"\tPassword: {acc_details.password}\n\tBalance: {acc_details.balance}")

    def show_Bank_Balance(self):
        print(f"\n\tTotal Balance of Bank: {self.Total_balance}\n")
    
    def show_Total_Loan(self):
        print(f"\n\tTotal Loan of Bank: {self.Total_Loan}\n")
    
    def bankrupt_account(self,account_number):
        account_Number=Account.Bank_Account.get(account_number)
        if account_Number:
            Bank_Management.bankrupt()
            print(f"\n\tAccount {account_number} has been bankrupted.")
        else:
            print("\n\tAccount not found!!")

    @dispatch(str,str)
    def change_info(self,change_type,change):
        for key,account_details in Account.Bank_Account.items():
            if change_type=="name":
                account_details.name=change
            elif change_type=="email":
                account_details.email=change
            elif change_type=="phone":
                account_details.phone=change
            else:
                print("\n\tNot change yet")
            
    def logIn_bankCode(self,Bank_code):
        if Bank_code==self.bank_code:
            self.Loged_in=True
            return True
        else:
            return False
        
    def LogIn_Password(self,password):
        if password==self.Bank_password:
            self.Loged_in=True
            return True
        else:
            return False
        
    def logout(self):
        if self.Loged_in==True:
            self.Loged_in=False
            print("\n\tYou are Log Out now!!")

                    #Bank name, bank code ,bank password
admin=Admin("Islami Bank Bangladesh Ltd","admin","admin")
print(admin)
current_account=None
while(True):
    print("\n\t1.Admin")
    print("\t2.User")
    print("\t3.Exit")
    num=input("\n\tChoose Option: ")
    if num=="1":
        bank_Code=input("\n\tBank Code(admin): ")
        if admin.logIn_bankCode(bank_Code):
            bank_password=input("\n\tPassword(admin): ")
            if admin.LogIn_Password(bank_password):
                while admin.Loged_in:
                    print("\n\t1.Create User Account")
                    print("\t2.Delete Account")
                    print("\t3.Total Balance")
                    print("\t4.Total Loan")
                    print("\t5.Check All User")
                    print("\t6.Confirm Loan")
                    print("\t7.Change User Info")
                    print("\t8.Account Bankrupt")
                    print("\t9.Log out")

                    choose=input("\n\tChoose Your Option: ")
                    if choose=="1":
                        name=input("\n\tName: ")
                        email=input("\tEmail: ")
                        phn=input("\tPhone Number: ")
                        address=input("\tAddress: ")
                        password=input("\tPassword: ")
                        acctype=input("\tAccount Type(SV/CR): ")
                        if acctype=="SV":
                            intarest=input("\tIntarest Rate: ")
                            current_account=SavingsAccount(name,email,phn,"IBBL",address,acctype,password,intarest)
                            print("\n\tAccount Create Successfully!!")
                        elif acctype=="CR":
                            limit=input("\tLimit: ")
                            current_account=CurrentAccount(name,email,phn,"IBBL",address,acctype,password,limit)
                            print("\n\tAccount Create Successfully!!")
                        else:
                            print("\n\tInvaild Key!!\n")
                    elif choose=="2":
                        acc_number=input("\n\tEnter Your Bank Number: ")
                        confirm=input("\n\tConfirm Delete Account(yes/no): ")
                        admin.Delete_Account(acc_number,confirm)
                    elif choose=="3":
                        admin.show_Bank_Balance()
                    elif choose=="4":
                        admin.show_Total_Loan()
                    elif choose=="5":
                        admin.show_all_Account()
                    elif choose=="6":
                        loan_apply=input("\n\tLoan Feature(ON/OFF): ")
                        if loan_apply=="ON":
                            admin.Loan_Feature_on()
                            print("\n\tSuccessfully ON!!")
                        elif loan_apply=="OFF":
                            admin.Loan_Feature_off()
                            print("\n\tSuccessfully OFF!!")
                        else:
                            print("\n\tPlease Currect Key!!")
                    elif choose=="7":
                        change_type=input("\n\tDo you want to change?(name or email or phne): ")
                        change=input("\n\tEnter Your New Info: ")
                        admin.change_info(change_type,change)
                    elif choose=="8":
                        bank_account_num=input("\n\tPlease Enter Account Number: ")
                        admin.bankrupt_account(bank_account_num)
                    elif choose=="9":
                        admin.logout()
                    else:
                        print("\n\tPlease Press the correct key!!")
            else:
                print("\n\tWrong Password\n")
        else:
            print("\n\tWrong Code\n")
    elif num=="2":
        account_Number=input("\n\tAccount Number: ")
        if account_Number in Account.Bank_Account:
            current_account=Account.Bank_Account[account_Number]
            if current_account.LogIn_Account(account_Number):
                account_password=input("\n\tAccount Password: ")
                if current_account.LogIn_Password(account_password):
                    print(f"\n\tWelcome {current_account.name}")
                    while current_account.log_in:
                        print("\n\t1.Deposit")
                        print("\t2.Withdraw")
                        print("\t3.Balance Check")
                        print("\t4.Balance Transfer")
                        print("\t5.Transection History")
                        print("\t6.Change Password")
                        print("\t7.Apply Intarest")
                        print("\t8.Apply Loan")
                        print("\t9.Show Information")
                        print("\t10.Log Out")

                        choose1 = input("\n\tChoose Your Option: ")
                        if choose1 == "1":
                            amount = int(input("\n\tAmount: "))
                            current_account.deposit(amount)
                        elif choose1 == "2":
                            amount = int(input("\n\tAmount: "))
                            if current_account.acctype=="SV":
                                current_account.Withdraw(amount)
                                    
                            elif current_account.acctype=="CR":
                                current_account.withdraw(amount)
                                
                        elif choose1 == "3":
                            current_account.check_available_balance()
                        elif choose1 == "4":
                            recipient_number = input("\n\tEnter recipient's account number: ")
                            amount = int(input("\n\tEnter amount to transfer: "))
                            if recipient_number in Account.Bank_Account:
                                current_account.Transfer_money(recipient_number, amount)
                            else:
                                print("\n\tRecipient account not found!")
                        elif choose1 == "5":
                            current_account.check_transaction_history()
                        elif choose1 == "6":
                            new_password = input("\n\tEnter new password: ")
                            current_account.change_info(new_password)
                        elif choose1=="7":
                                if current_account.acctype=="SV":
                                    current_account.Intarest()

                                elif current_account.acctype=="CR":
                                    print("\n\tThis service is not for you!!")
                            
                        elif choose1 == "8":
                            loan_amount = int(input("\n\tEnter loan amount: "))
                            current_account.Loan_amount(loan_amount)
                        elif choose1=="9":
                            current_account.show_info()
                        elif choose1 == "10":
                            current_account.Logout()
                            current_account=None
                            break
                        else:
                            print("\n\tPlease press the correct key!!")
                    else:
                        print("\n\tWrong Password")
            else:
                print("\n\tWrong Account")
        else:
            print("\n\tNo Account Create yet now.")
    elif num=="3":
        print("\n\tThanks For Visiting!!")
        break
    else:
        print("\n\tPlease Press the correct key!!")