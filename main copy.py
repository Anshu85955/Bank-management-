import json
import random
import string
from pathlib import Path 



class Bank:
    dataBase = 'data.json'
    data = []
    try:
        if Path(dataBase).exists():   #  added ()
            with open(dataBase) as fs:
                data = json.loads(fs.read())
        else:
            print("No such File Exists.")
    except Exception as err:
        print(f"Exception occured as {err}")

    @classmethod
    def __Update(cls):   #  moved outside except block
        with open(cls.dataBase, 'w') as fs:
            fs.write(json.dumps(Bank.data, indent=4))  # added indent for readability

    @classmethod
    def __accountgerate(cls):   
        alpha = random.choices(string.ascii_letters, k=4)
        nums = random.choices(string.digits, k=4)
        spchar = random.choices("!@#$&%^*", k=1)  
        id = alpha + nums + spchar
        random.shuffle(id)
        return "".join(id)

    def createaccount(self):
        info = {
            "name": input("tell me your name:- "),
            "age": int(input("tell me your age:- ")),
            "email": input("tell me your email:- "),
            "Mob_no": input("tell me your mobile number :- "), 
            "pin": int(input("tell me your 4 Digit pin:- ")),
            "accountNo": Bank.__accountgerate(),
            "balance": 0
        }
        if info['age'] < 18 or len(str(info["pin"])) != 4:
            print(" Sorry you cannot create your account.")
        else:
            print(" Account has been created Successfully!")
            for i in info:
                print(f"{i} : {info[i]}")
            print(" Please note down your Account Number.")

            Bank.data.append(info)
            Bank.__Update()

    def depositmoney(self):   # moved outside createaccount
        accnumber = input("please tell your account Number:- ")
        pin = int(input("please tell your pin aswell:- "))

        userdata = None
        for i in Bank.data:
            if i['accountNo'] == accnumber and i['pin'] == pin:
                userdata = i
                break

        if not userdata:
            print("Sorry No data Found")
        else:
            amount = int(input("How much amount you want to deposit: "))  
            if amount > 10000 or amount <= 0:
                print("Sorry the amount is too much, you can deposit below 10000 and more than 0")
            else:
                userdata['balance'] += amount
                Bank.__Update()
                print("Amount deposited Successfully!")

    def withdrawmoney(self):   # moved outside depositammount
        accnumber = input("please tell your account Number:- ")
        pin = int(input("please tell your pin aswell:- "))

        userdata = None
        for i in Bank.data:
            if i['accountNo'] == accnumber and i['pin'] == pin:
                userdata = i
                break

        if not userdata:
            print("Sorry No data Found")
        else:
            amount = int(input("How much amount you want to Withdraw: "))  
            if amount > 10000 or amount <= 0:
                print("Sorry  you have not a sufficient banck balance")
            else:
                userdata['balance'] -= amount
                Bank.__Update()
                print("Amount Withdraw Successfully!")

    def showdetails(self):   # moved outside withdraw 
        accnumber = input("please tell your account Number:- ")
        pin = int(input("please tell your pin aswell:- "))

        userdata = None
        for i in Bank.data:
            if i['accountNo'] == accnumber and i['pin'] == pin:
                userdata = i
                break

        if userdata:
            print("Your account details:")
            for k, v in userdata.items():
                print(f"{k}: {v}")
        else:
            print("Sorry No data Found")

    def updatedetails(self): # moved outside the showdetails
        accnumber = input("please tell your account number ")
        pin = int(input("please tell your pin aswell "))

        userdata = [i for i in Bank.data if i['accountNo'] == accnumber and i['pin'] == pin]

        if not userdata:
            print("No such user found ")
        
        else:
            print("You cannot change the age, account number, balance")

            print("Fill the details for change or leave it empty if no change")

            newdata = {
                "name": input("please tell new name or press enter : "),
                "email": input("please tell your new Email or press enter to skip :"),
                "pin": input("enter new Pin or press enter to skip: ")
            }

            if newdata["name"] == "":
                newdata["name"] = userdata[0]['name']
            if newdata["email"] == "":
                newdata["email"] = userdata[0]['email']
            if newdata["pin"] == "":
                newdata["pin"] = userdata[0]['pin']
            else:
                newdata['pin'] = int(newdata['pin'])
            
            newdata['age'] = userdata[0]['age']
            newdata['accountNo'] = userdata[0]['accountNo']
            newdata['balance'] = userdata[0]['balance']
            newdata['Mob_no'] = userdata[0]['Mob_no']

            # update values
            for i in newdata:
                userdata[0][i] = newdata[i]

            Bank.__Update()
            print("Details updated successfully")

    def delete(self):  # move outside the updatedetails
        accnumber = input("please tell your account number: ")
        pin = int(input("please tell your pin as well: "))

        userdata = [i for i in Bank.data if i['accountNo'] == accnumber and i['pin'] == pin]

        if not userdata:
            print("Sorry, no such data exists")
        else:
            check = input("Press A if you actually want to delete your account, or press Z to cancel: ")
            if check.lower() == "a":
                index = Bank.data.index(userdata[0])
                Bank.data.pop(index)
                Bank.__Update()
                print("Account deleted successfully.")
            else:
                print("Deletion cancelled.")


user = Bank()

print("Press 1 for creating your account")
print("Press 2 for deposite money in the Bank")
print("Press 3 for withdrawing your money")
print("Press 4 for details")
print("Press 5 for Updating the details")
print("Press 6 for deleting your account")

check = int(input("tell your response :- "))

if check == 1:
    user.createaccount()

if check == 2:
    user.depositmoney()

if check == 3:
    user.withdrawmoney()

if check == 4:
    user.showdetails()

if check == 5:
    user.updatedetails()

if check == 6:
    user.delete()
