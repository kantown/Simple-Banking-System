from random import randint
import _sqlite3
conn = _sqlite3.connect('card.s3db')
cur = conn.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS card(id INTEGER PRIMARY KEY, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)')
conn.commit()
IIN = '400000'
acc_dic = dict()
logged_to = ''


def generate_card_number():
    card_number = IIN + str(randint(100000000, 999999999))
    suma = 0
    x = 1
    for letter in card_number:
        num = int(letter)
        if x % 2 == 1:
            num *= 2
            if num > 9:
                num -= 9
                suma += num
            else:
                suma += num
        else:
            suma += num
        x += 1
    if suma % 10 != 0:
        last_digit = 10 - (suma % 10)
    else:
        last_digit = 0
    card_number += str(last_digit)
    return card_number


def isLunh(number):
    s = number[:-1]
    x = 1
    suma = 0
    for letter in s:
        num = int(letter)
        if x % 2 == 1:
            num *= 2
            if num > 9:
                num -= 9
        suma += num
        x += 1
    if (suma % 10) + int(number[-1]) == 10:
        return True
    else:
        return False


def createAccount():
    card_number = generate_card_number()
    PIN = str(randint(1000, 9999))
    print(f"""\nYour card has been created
Your card number:
{card_number}
Your card PIN:
{PIN}""")

    cur.execute(f'INSERT INTO card (number, pin, balance) VALUES ({card_number}, {PIN}, {0})')
    conn.commit()


def signIn():
    global logged
    global logged_to
    print("Enter your card number")
    typed_card_number = input()
    print("Enter your card pin")
    typed_PIN = input()
    try:
        cur.execute(f"SELECT pin FROM card WHERE number = {typed_card_number}")
    except TypeError:
        print("Wrong card number or PIN!")
    else:
        try:
            result = cur.fetchone()[0]
        except TypeError:
            print("Wrong card number or PIN!")
        else:
            if typed_PIN == result:
                print("\nYou have successfully logged in!")
                logged_to = typed_card_number
                logged = True
            else:
                print("Wrong card number or PIN!")




def balance():
    # print(f"Balance: {acc_dic[logged_to]['balance']}")
    cur.execute(f"SELECT balance FROM card WHERE number = {logged_to}")
    print(cur.fetchone()[0])


logged = False
while True:
    if not logged:
        print("1. Create an account")
        print("2. Log into account")
        print("0. Exit")
        choice = int(input())
        if choice == 1:
            createAccount()
        elif choice == 2:
            signIn()
        elif choice == 0:
            print("Bye!")
            break
        else:
            print("Type correct number")
    else:
        print("1. Balance")
        print("2. Add income")
        print("3. Do transfer")
        print("4. Close account")
        print("5. Log out")
        print("0. Exit")
        choice = int(input())
        if choice == 1:
            balance()
        elif choice == 2:
            addInc = int(input("Enter income:"))
            cur.execute(f"SELECT balance FROM card WHERE number = {logged_to}")
            balanceNow = cur.fetchone()[0]
            cur.execute(f"UPDATE card SET balance = {balanceNow + addInc} WHERE number = {logged_to}")
            conn.commit()
            print("Income was added!")
        elif choice == 3:
            print("Transfer")
            givenNumber = input("Enter card number: ")
            if isLunh(givenNumber):
                cur.execute("SELECT number FROM card")
                card_ls = cur.fetchall()
                for tup in card_ls:
                    if givenNumber in tup:
                        isInList = True
                    else:
                        isInList = False
                if isInList:
                    if givenNumber != logged_to:
                        cur.execute(f"SELECT balance FROM card WHERE number = {givenNumber}")
                        receiverBalance = int(cur.fetchone()[0])
                        cur.execute(f"SELECT balance FROM card WHERE number = {logged_to}")
                        senderBalance = int(cur.fetchone()[0])
                        amount = int(input("Enter how much money you want to transfer: "))

                        if senderBalance >= amount:
                            receiverBalance += amount
                            senderBalance -= amount
                            cur.execute(f"UPDATE card SET balance = {receiverBalance} WHERE number = {givenNumber}")
                            cur.execute(f"UPDATE card SET balance = {senderBalance} WHERE number = {logged_to}")
                            conn.commit()
                        else:
                            print("Not enough money!")
                    else:
                        print("You can't transfer money to the same account!")
                else:
                    print("Such a card does not exist.")
            else:
                print("Probably you made a mistake in the card number. Please try again!")

        elif choice == 4:
            cur.execute(f"DELETE FROM card WHERE number = {logged_to}")
            conn.commit()
            logged = False
            logged_to = ''

        elif choice == 5:
            logged = False
            logged_to = ''

        elif choice == 0:
            print("Bye!")
            break
        else:
            print("Type correct number")
