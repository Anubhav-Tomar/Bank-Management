import json
import random
import string
import re
from pathlib import Path
import streamlit as st

class Bank:

    database = Path(__file__).parent / 'data.json'
    data = []
    try:
        if Path(database).exists():
          with open(database, 'r') as fs:
            data = json.loads(fs.read())

        else:
            print("No such file exist")

    except Exception as err:
        print(f"An error occured as {err}")

    # Updates the database with new account information
    @classmethod
    def __update(cls):
        with open(Bank.database, 'w')as fs:
            fs.write(json.dumps(Bank.data))

    # Generate account number
    @classmethod
    def __generateAccount(cls):
        char = random.choices(string.ascii_letters, k=3)
        number = random.choices(string.digits, k=3)
        specialChar = random.choices("!@#$%^&*", k=1)

        id = char + number + specialChar
        random.shuffle(id)
        return "".join(id)

    # Create a new account
    def CreateAccount(self):

        try:
            name = input("Enter your name:").strip()
            if not name:
                print("Name cannot be empty")
                return
            
            age = int(input("Enter your age:"))
            if not age:
                print("Age cannot be empty")
                return
            elif age < 18 or age > 100:
                print("Your are not eligible to create an account")
                return

            email = input("Enter your email: ").strip()
            if not email:
                print("Email cannot be empty")
                return
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(pattern, email):
                print("Invalid email format")
                return

            pin = input("Enter your 4 digit pin:").strip()
            if not pin:
                print("Pin cannot be empty")
                return
            if not pin.isdigit() or len(pin) != 4:
                print("PIN must contain exactly 4 digits")
                return
            
        except ValueError:
            print("Invalid input, please enter a valid age and pin")
            return

        info = {
            "name": name,
            "age": age,
            "email": email,
            "pin": pin,
            "accountNo": Bank.__generateAccount(),
            "balance": 0
        }

        print("Account created successfully")

        for i in info:
            if i == "pin":
                print("pin: ****")
            else:
                print(f"{i}: {info[i]}")

        print("Please remember your account number and pin for future use")

        Bank.data.append(info)
        Bank.__update()

    # Deposit money into the account
    def depositMoney(self):
        accountNo = input("Enter your account number: ").strip()
        pin = input("Enter your 4 digit pin: ").strip()
        
        for i in Bank.data:
            if i['accountNo'] == accountNo and i['pin'] == pin:
                try:
                    amount = int(input("Enter the amount to deposit: "))
                except ValueError:
                    print("Invalid amount, please enter numbers only")
                    return

                if amount <= 0 or amount > 100000:
                    print("Invalid amount, please enter upto 1,00,000")
                    return
                
                else:
                    i['balance'] += amount
                    print(f"Amount deposited successfully. New balance is {i['balance']}")
                    Bank.__update()
                return
            
        print("Invalid account number or pin")

    # Withdraw money from the account
    def withdrawMoney(self):
        accountNo = input("Enter your account number: ").strip()
        pin = input("Enter your 4 digit pin: ").strip()
                
        for i in Bank.data:
            if i['accountNo'] == accountNo and i['pin'] == pin:
                try:
                    amount = int(input("Enter the amount to withdraw: "))
                except ValueError:
                    print("Invalid amount, please enter numbers only")
                    return

                if amount <=0 or amount >100000:
                    print("Invalid amount, please enter upto 1,00,000")
                    return
                
                elif i['balance'] < amount:
                    print("Insufficient balance")
                    return
                
                else:
                    i['balance'] -= amount
                    print(f"Amount withdrawn successfully. New balance is {i['balance']}")
                    Bank.__update()
                    return
        print("Invalid account number or pin")


    # Get account details
    def getUserDetails(self):
        accountNo = input("Enter your account number: ").strip()
        pin = input("Enter your 4 digit pin: ").strip()
            
        for i in Bank.data:
            if i['accountNo'] == accountNo and i['pin'] == pin:
                print(f"Name: {i['name']}")
                print(f"Age: {i['age']}")
                print(f"Email: {i['email']}")
                print(f"Account Number: {i['accountNo']}")
                print(f"Balance: {i['balance']}")
                return
        print("Invalid account number or pin")


    # Update account details
    def updateDetails(self):
        accountNo = input("Enter your account number: ").strip()
        pin = input("Enter your 4 digit pin: ").strip()
            
        for i in Bank.data:
            if i['accountNo'] == accountNo and i['pin'] == pin:
                print("Press 1 to update name")
                print("Press 2 to update age")
                print("Press 3 to update email")
                print("Press 4 to update pin")

                try:
                    check = int(input("Enter your choice: "))
                except ValueError:
                    print("Invalid choice")
                    return

                if check == 1:
                    name = input("Enter your new name: ").strip()

                    if not name:
                        print("Name cannot be empty")
                        return

                    i['name'] = name
                    print("Name updated successfully")

                elif check == 2:
                    try:
                        i['age'] = int(input("Enter your new age: "))

                        if i['age'] < 18 or i['age'] > 100:
                            print("Invalid age, please enter a valid age")
                            return

                    except ValueError:
                        print("Invalid input, please enter a valid age")
                        return
                    
                    print("Age updated successfully")

                elif check == 3:
                    email = input("Enter your new email: ").strip()
                    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

                    if not email or not re.match(pattern, email):
                        print("Invalid email format")
                        return

                    i['email'] = email
                    print("Email updated successfully")

                elif check == 4:
                    newPin = input("Enter your new 4 digit pin: ").strip()

                    if not newPin.isdigit() or len(newPin) != 4:
                        print("PIN must contain exactly 4 digits")
                        return

                    i['pin'] = newPin
                    print("PIN updated successfully")

                else:
                    print("Invalid choice")
                    return

                Bank.__update()
                return
        print("Invalid account number or pin")


    # Delete account
    def deleteAccount(self):
        accountNo = input("Enter your account number: ").strip()
        pin = input("Enter your 4 digit pin: ").strip()

        for i in Bank.data:
            if i['accountNo'] == accountNo and i['pin'] == pin:

                confirm = input("Are you sure you want to delete this account? (yes/no): ")

                if confirm.lower() == "yes":
                    Bank.data.remove(i)
                    Bank.__update()
                    print("Account deleted successfully")
                else:
                    print("Account deletion cancelled")

                return

        print("Invalid account number or pin")


user = Bank()
print("Press 1 for creating a new account")
print("Press 2 for depositing money in the bank")
print("Press 3 for withdrawing the money")
print("Press 4 for details")
print("Press 5 for updating the details")
print("Press 6 for deleting the account")

try:
    check =int(input("Enter your choice: "))

    if check == 1:
        user.CreateAccount()

    elif check == 2:
        user.depositMoney()

    elif check == 3:
        user.withdrawMoney()

    elif check == 4:
        user.getUserDetails()

    elif check == 5:
        user.updateDetails()

    elif check == 6:
        user.deleteAccount()

    else: 
        print("Invalid input, please enter a valid choice.")

except ValueError:
    print("Invalid input, please enter a valid choice.")
