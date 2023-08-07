import random
import csv
import smtplib
import pytz
from datetime import *
from tkinter import *
from PIL import ImageTk, Image

# initialise variable for email
port = 587
password = "uwaoczrsbuijbgmu"
sender_email = "donotreply.bludbank@gmail.com"

# initialise general variables
loginErrorMsg = False
verifErrorMsg = False
transactionErrorMsg = ""
username = ''
receipt = []
sessionWithdrawedAmount = 0


# MATEJ main function to create tkinter window
def main():
    window = Tk()
    window.title("BludBank ATM")
    window.geometry("800x650")

    welcomeMenu(window)


# MATEJ welcomes page where users can select log in
def welcomeMenu(window):
    clearFrame(window)
    resetVariables()

    # create a header to display the bludbank logo
    titleFrame = Frame(window)
    img = ImageTk.PhotoImage(Image.open("bludbank.png"))
    label = Label(titleFrame, image=img)
    label.pack(pady=(40, 0))
    titleFrame.pack(side=TOP, fill=X, padx=10, pady=10)

    # create a frames to display the main title and subtitle
    headerFrame = Frame(window)
    Label(headerFrame, text="Blud Bank", font=("Arial", 50)).pack(pady=(30, 0))

    Label(headerFrame, text="Bloody good banking!",
          font=("Arial", 24)).pack(pady=(10, 100))
    headerFrame.pack()

    # create a login button that opens the login menu when pressed
    Button(window,
           text="Login",
           font=("Arial", 18),
           padx=20,
           pady=10,
           command=lambda: loginMenu(window)).pack()

    # display copyright info in footer
    footerFrame = Frame(window)
    Label(footerFrame, text="Copyright @ Blud Bank 2023",
          font=("Arial", 12)).pack(pady=5)
    footerFrame.pack(side=BOTTOM)

    # run the main event loop
    window.mainloop()


# MATEJ function to allow users to log in
def loginMenu(window):
    clearFrame(window)

    # create a header to display the bludbank logo and exit button
    titleFrame = Frame(window)
    img = ImageTk.PhotoImage(Image.open("bludbank.png").resize((60, 60)))
    label = Label(titleFrame, image=img)
    label.pack(side=LEFT, padx=5, pady=5)
    Button(titleFrame,
           text="Cancel",
           font=("Arial", 16),
           padx=3,
           pady=3,
           command=lambda: welcomeMenu(window)).pack(side=RIGHT, anchor=NE)
    titleFrame.pack(side=TOP, fill=X, padx=5, pady=5)

    # create an input for the user to input their username
    topFrame = Frame(window)
    Label(topFrame, text="Username: ", font=("Arial", 20)).pack(side=LEFT,
                                                                pady=(5, 5))
    entName = Entry(topFrame, foreground="#292929", background="#F4F6F7")
    entName.pack(side=LEFT, pady=(5, 5))
    topFrame.pack(pady=(200, 0))

    # create an input for the user to input their PIN
    midFrame = Frame(window)
    Label(midFrame, text="PIN:           ",
          font=("Arial", 20)).pack(side=LEFT, pady=(5, 5))
    entPsw = Entry(midFrame,
                   foreground="#292929",
                   background="#F4F6F7",
                   show="*")
    entPsw.pack(side=LEFT, pady=(5, 5))
    midFrame.pack(side=TOP)

    # create a button to validate the user login when pressed
    buttonFrame = Frame(window)
    btnConnect = Button(buttonFrame,
                        text="Login",
                        padx=20,
                        pady=10,
                        font=("Arial", 20),
                        command=lambda: validateLogin(window, entName, entPsw))
    btnConnect.pack(pady=(30, 0))
    buttonFrame.pack(side=TOP)

    window.mainloop()


# BOTH function to determine whether the user exists
def validateLogin(window, entName, entPsw):
    # initialise relevant variables
    global loginErrorMsg
    global username
    sendEmail = False
    userEmailAddress = ''

    # take in the email and password
    usernameInput = entName.get().lower()
    pin = entPsw.get()

    # create an error frame
    errorFrame = Frame(window)
    errorFrame.pack(side=TOP)

    # open the file in reader mode and then as an dictionary object
    with open('user-data.csv', 'r') as userFile:
        userFileReader = csv.DictReader(userFile)
        # check if the username matches and if the password matches
        for user in userFileReader:
            if user['username'] == usernameInput:
                if user['pin'] == pin:
                    sendEmail = True
                    username = user['username']
                    userEmailAddress = user['email']

    # if its a new user: use email/some sort of verification and then add them to the database
    if sendEmail == True:
        emailVerification(window, userEmailAddress)
    else:
        # runs in the case that the user does not exist
        while True:
            if loginErrorMsg == True:
                break
            Label(errorFrame,
                  text=("⚠ Incorrect username or password."),
                  font=("Arial", 12)).pack(side=LEFT, pady=(10, 5))
            errorFrame.pack(side=TOP)
            loginErrorMsg = True


# BOTH function that verifies user through a PIN sent to their email
def emailVerification(window, userEmailAddress):
    clearFrame(window)

    # create a header to display the bludbank logo and exit button
    titleFrame = Frame(window)
    img = ImageTk.PhotoImage(Image.open("bludbank.png").resize((60, 60)))
    label = Label(titleFrame, image=img)
    label.pack(side=LEFT, padx=5, pady=5)
    Button(titleFrame,
           text="Cancel",
           font=("Arial", 16),
           padx=3,
           pady=3,
           command=lambda: welcomeMenu(window)).pack(side=RIGHT, anchor=NE)
    titleFrame.pack(side=TOP, fill=X, padx=5, pady=5)

    # creating the verification number and message
    verifCode = random.randint(1000, 9999)
    message = """From: BludBank Pty Ltd.
Subject: Verification Code
Your verification number is """ + str(verifCode) + """

Have a great day!
"""

    # initialise smtp and send verificiation email
    smtpObj = smtplib.SMTP('smtp.gmail.com', port)
    smtpObj.starttls()
    smtpObj.login(sender_email, password)
    smtpObj.sendmail(sender_email, userEmailAddress, message)

    # create input frame for the verification email PIN
    verifFrame = Frame(window, width=100)
    entPin = Entry(verifFrame,
                   background="#F4F6F7",
                   foreground="#292929",
                   font=("Arial", 40),
                   justify='center',
                   width=20)
    entPin.pack(side=TOP)
    verifFrame.pack(pady=(200, 10), ipadx=50)

    # display instructions to input verification code
    headerFrame = Frame(window)
    Label(headerFrame,
          text="Enter verification code sent to your email.",
          font=("Arial", 20)).pack(pady=(10, 50))
    headerFrame.pack()

    # create a button that validates the user when pressed
    buttonFrame = Frame(window)
    Button(buttonFrame,
           text="Submit",
           font=("Arial", 20),
           padx=20,
           pady=10,
           command=lambda: validateEmailVerif(window, verifCode, entPin)).pack(
               pady=(30, 0))
    buttonFrame.pack()

    window.mainloop()


# MATEJ function to check if inputted email verification PIN is correct
def validateEmailVerif(window, verifCode, entPin):
    # initialise relevant variables
    inputverifCode = entPin.get()
    userVerified = False
    global verifErrorMsg

    # create error frame
    verifErrorFrame = Frame(window)
    verifErrorFrame.pack(side=TOP)

    # check if the inputted PIN matches the real one
    if str(inputverifCode) == str(verifCode):
        userVerified = True

    # proceed to the menu if the user is verified or display an error message
    if userVerified == True:
        mainMenu(window)
    else:
        while True:
            if verifErrorMsg == True:
                break

            Label(verifErrorFrame,
                  text=("⚠ Incorrect code. Try again."),
                  font=("Arial", 12)).pack(side=LEFT, pady=(5, 50))
            verifErrorFrame.pack(side=TOP)
            verifErrorMsg = True


# MATEJ function to display the main menu and acccess deposit and withdraw functions
def mainMenu(window):
    global username

    clearFrame(window)

    # create a button that exits the main menu when pressed
    exitFrame = Frame(window)
    Button(exitFrame,
           text="Logout",
           font=("Arial", 16),
           padx=3,
           pady=3,
           command=lambda: exitMenu(window)).pack(side=RIGHT, anchor=NE)
    exitFrame.pack(side=TOP, fill=X, padx=10, pady=10)

    # create a header to display the bludbank logo and exit button
    titleFrame = Frame(window)
    img = ImageTk.PhotoImage(Image.open("bludbank.png"))
    label = Label(titleFrame, image=img)
    label.pack(pady=(0, 0))
    titleFrame.pack(side=TOP, fill=X, padx=10, pady=10)

    # create a main menu title and subtitle
    headerFrame = Frame(window)
    Label(headerFrame, text="Main Menu", font=("Arial", 50)).pack(pady=(30, 0))

    Label(headerFrame, text="Select An Option",
          font=("Arial", 24)).pack(pady=(10, 70))
    headerFrame.pack()

    # create buttons that open the desposit or withdraw menu when pressed
    btnFrame = Frame(window)
    Button(btnFrame,
           text="Withdraw",
           font=("Arial", 18),
           padx=20,
           pady=10,
           command=lambda: withdrawMenu(window)).pack(side=LEFT)
    Button(btnFrame,
           text="Deposit",
           font=("Arial", 18),
           padx=20,
           pady=10,
           command=lambda: depositMenu(window)).pack(side=RIGHT)
    btnFrame.pack()

    # display the user's balance
    bankBalance = checkDetails()[0]
    balanceFrame = Frame(window)
    Label(balanceFrame,
          text=("Balance: $" + str(bankBalance)),
          font=("Arial", 14)).pack(pady=(20, 10))
    balanceFrame.pack()

    # Run the main event loop
    window.mainloop()
    pass


# MATEJ function for users to deposit funds into their account
def depositMenu(window):
    clearFrame(window)
    global username

    # create a header to display the bludbank logo and exit button
    titleFrame = Frame(window)
    img = ImageTk.PhotoImage(Image.open("bludbank.png").resize((60, 60)))
    label = Label(titleFrame, image=img)
    label.pack(side=LEFT, padx=5, pady=5)
    Button(titleFrame,
           text="Exit",
           font=("Arial", 16),
           padx=3,
           pady=3,
           command=lambda: mainMenu(window)).pack(side=RIGHT, anchor=NE)
    titleFrame.pack(side=TOP, fill=X, padx=5, pady=5)

    # display the user's balance
    bankBalance = checkDetails()[0]
    balanceFrame = Frame(window)
    Label(balanceFrame,
          text=("Balance: $" + str(bankBalance)),
          font=("Arial", 16)).pack(pady=(80, 10))
    balanceFrame.pack()

    # create a title prompting the user to enter amount
    labelFrame = Frame(window)
    Label(labelFrame, text="Enter amount to deposit:",
          font=("Arial", 20)).pack(pady=(90, 10))
    labelFrame.pack()

    # input for users to enter amount to deposit
    inputFrame = Frame(window, width=100)
    entAmount = Entry(inputFrame,
                      background="#F4F6F7",
                      foreground="#292929",
                      font=("Arial", 40),
                      justify='center',
                      width=20)
    entAmount.pack(side=TOP)
    inputFrame.pack(pady=(10, 5), ipadx=50)

    # create empty transaction error label
    transactionErrorFrame = Frame(window)
    Label(transactionErrorFrame, text=(""),
          font=("Arial", 12)).pack(side=LEFT, pady=(5, 30))
    transactionErrorFrame.pack(side=TOP)

    # create a button that submits the deposit when pressed
    buttonFrame = Frame(window)
    Button(buttonFrame,
           text="Deposit",
           font=("Arial", 20),
           padx=20,
           pady=10,
           command=lambda: transaction(window, entAmount, "d",
                                       transactionErrorFrame)).pack(pady=(30,
                                                                          5))
    buttonFrame.pack()

    window.mainloop()


# MATEJ function for users to withdraw funds from their account
def withdrawMenu(window):
    clearFrame(window)
    global username

    # create a header to display the bludbank logo and exit button
    titleFrame = Frame(window)
    img = ImageTk.PhotoImage(Image.open("bludbank.png").resize((60, 60)))
    label = Label(titleFrame, image=img)
    label.pack(side=LEFT, padx=5, pady=5)
    Button(titleFrame,
           text="Exit",
           font=("Arial", 16),
           padx=3,
           pady=3,
           command=lambda: mainMenu(window)).pack(side=RIGHT, anchor=NE)
    titleFrame.pack(side=TOP, fill=X, padx=5, pady=5)

    # display the user's balance
    bankBalance = checkDetails()[0]
    balanceFrame = Frame(window)
    Label(balanceFrame,
          text=("Balance: $" + str(bankBalance)),
          font=("Arial", 16)).pack(pady=(80, 10))
    balanceFrame.pack()

    # create a title prompting the user to enter amount
    labelFrame = Frame(window)
    Label(labelFrame, text="Enter amount to withdraw:",
          font=("Arial", 20)).pack(pady=(90, 10))
    labelFrame.pack()

    # input for users to enter amount to withdraw
    inputFrame = Frame(window, width=100)
    entAmount = Entry(inputFrame,
                      background="#F4F6F7",
                      foreground="#292929",
                      font=("Arial", 40),
                      justify='center',
                      width=20)
    entAmount.pack(side=TOP)
    inputFrame.pack(pady=(10, 5), ipadx=50)

    # create empty transaction error label
    transactionErrorFrame = Frame(window)
    Label(transactionErrorFrame, text=(""),
          font=("Arial", 12)).pack(side=LEFT, pady=(5, 30))
    transactionErrorFrame.pack(side=TOP)

    # create a button that submits the deposit when pressed
    buttonFrame = Frame(window)
    Button(buttonFrame,
           text="Withdraw",
           font=("Arial", 20),
           padx=20,
           pady=10,
           command=lambda: transaction(window, entAmount, "w",
                                       transactionErrorFrame)).pack(pady=(30,
                                                                          5))
    buttonFrame.pack()

    window.mainloop()


# RISITH function to check for transaction errors
def transaction(window, entAmount, transactionType, transactionErrorFrame):
    # intitalise relevant variables
    global username
    global transactionErrorMsg
    global sessionWithdrawedAmount

    transactionErrorMsg = ""

    # checking if the amount is an integer
    try:
        amount = int(entAmount.get())
    except ValueError:
        transactionError(window, transactionErrorFrame, "variableNotInt")
        return

    # checking if there is a negative deposit
    if amount < 1:
        transactionError(window, transactionErrorFrame, "negativeAmount")
        return

    # checking if the withdrawal limit has been reached
    if (sessionWithdrawedAmount + amount) > 1000 and transactionType == 'w':
        transactionError(window, transactionErrorFrame, "withdrawalLimit")
        return

    # checking if the transaction amount is able to be made of notes
    if amount % 5 != 0:
        transactionError(window, transactionErrorFrame, "invalidAmount")
        return

    updatedUserFileReader = []

    # opening the file in reader mode and updating the bank balance of the desired user
    with open('user-data.csv', 'r') as userFile:
        userFileReader = csv.DictReader(userFile)
        for user in userFileReader:
            if user['username'] == username:
                bankBalance = float(user['bankbalance'])
                # checking if there is enough money to withdraw in the bankbalance
                if transactionType == 'w' and amount > bankBalance:
                    transactionError(window, transactionErrorFrame,
                                     "insufficientFunds")
                    return
                # withdrawing/deposting the money
                if transactionType == 'w':
                    bankBalance -= amount
                    sessionWithdrawedAmount += amount
                if transactionType == 'd':
                    bankBalance += amount
                user['bankbalance'] = bankBalance
            updatedUserFileReader.append(user)

    # writing into the file the updated rows
    with open('user-data.csv', 'w', newline='') as userFile:
        headers = ['username', 'pin', 'bankbalance', 'email']
        userFileWriter = csv.DictWriter(userFile,
                                        delimiter=',',
                                        fieldnames=headers)
        userFileWriter.writerow(dict((heads, heads) for heads in headers))
        userFileWriter.writerows(updatedUserFileReader)

    # adding the transaction to the receipt
    addReceipt(transactionType, amount)
    mainMenu(window)


# MATEJ displays the relevant error message thrown from inputs to transactions
def transactionError(window, transactionErrorFrame, error):
    global transactionErrorMsg

    # store error messages for each transaction error
    errorMsgs = {
        "negativeAmount": "⚠ Error! Please input a positive value.",
        "variableNotInt": "⚠ Error! Please enter a number.",
        "invalidAmount": "⚠ Invalid amount! We only accept cash values.",
        "insufficientFunds": "⚠ Error! You don't have enough money.",
        "withdrawalLimit":
        "⚠ Error! The amount you entered exceeds this session's withdrawal limit of $1000!",
        "defaultError": "⚠ Error! Please try again."
    }

    # display the error if it is not already being displayed
    if error == transactionErrorMsg:
        return
    else:
        clearTransactionError(transactionErrorFrame)
        Label(transactionErrorFrame,
              text=(errorMsgs[error]),
              font=("Arial", 12)).pack(side=LEFT, pady=(5, 50))
        transactionErrorFrame.pack(side=TOP)
        transactionErrorMsg = error


# RISITH adding receipt items to the 2d list receipt
def addReceipt(transactionType, amount):
    global receipt
    tz_syd = pytz.timezone('Australia/Sydney')
    now = datetime.now(tz_syd)
    time = now.strftime("%H:%M:%S")
    receipt.append([transactionType, amount, time])
    pass


# RISITH sends the receipt
def sendReceipt():
    # retrieve needed variables
    global receipt
    global username
    bankBalance, userEmailAddress = checkDetails()
    tz_syd = pytz.timezone('Australia/Sydney')
    now = datetime.now(tz_syd)

    # formatting/creating the receipt
    receiptMessage = """
----------------------------------------------------
                    Bludbank ATM
----------------------------------------------------

CUSTOMER NAME: """ + username + "\nDATE: " + now.strftime("%d/%m/%Y") + "\n\n"

    # loop through transactions and add withdrawals/deposits to receipt
    for transaction in receipt:
        if transaction[0] == 'w':
            receiptMessage = receiptMessage + str(
                receipt.index(transaction) + 1) + ". WITHDREW $"
        elif transaction[0] == 'd':
            receiptMessage = receiptMessage + str(
                receipt.index(transaction) + 1) + ". DEPOSITED $"
        receiptMessage += str(transaction[1]) + " AT " + str(
            transaction[2]) + "\n"

    receiptMessage += "\nTOTAL BALANCE: $" + str(bankBalance)

    # send the receipt in an amail
    smtpObj = smtplib.SMTP('smtp.gmail.com', port)
    smtpObj.starttls()
    smtpObj.login(sender_email, password)
    smtpObj.sendmail(
        sender_email, userEmailAddress, """From: BludBank Pty Ltd.
Subject: Receipt""" + receiptMessage)

    # save the receipt message as a file
    with open('receipt.txt', 'w') as file:
        file.write(receiptMessage)


# RISITH to return the bank balance and email of the user
def checkDetails():
    # initialise relevant variables
    global username
    balance = 0
    email = ""

    # open user data file
    with open('user-data.csv', 'r') as userFile:
        userFileReader = csv.DictReader(userFile)
        # check if the username matches and if the password matches
        for user in userFileReader:
            if user['username'] == username:
                balance = user['bankbalance']
                email = user['email']
    return balance, email


# MATEJ function to display exit menu, send the receipt and log out user
def exitMenu(window):
    sendReceipt()
    clearFrame(window)

    # create a header to display the bludbank logo and exit button
    titleFrame = Frame(window)
    img = ImageTk.PhotoImage(Image.open("bludbank.png"))
    label = Label(titleFrame, image=img)
    label.pack(pady=(40, 0))
    titleFrame.pack(side=TOP, fill=X, padx=10, pady=10)

    # create a thank you message
    headerFrame = Frame(window)
    Label(headerFrame, text="Thanks for visiting!",
          font=("Arial", 50)).pack(pady=(30, 0))

    Label(headerFrame,
          text="A receipt has been sent to your email.",
          font=("Arial", 24)).pack(pady=(10, 100))
    headerFrame.pack()

    # create a button that exits to the welcome screen when pressed
    Button(window,
           text="Exit",
           font=("Arial", 18),
           padx=20,
           pady=10,
           command=lambda: welcomeMenu(window)).pack()

    window.mainloop()


# MATEJ to reset variables after log out for new user
def resetVariables():
    # initialise relevant variables
    global loginErrorMsg
    global verifErrorMsg
    global transactionErrorMsg
    global username
    global receipt
    global sessionWithdrawedAmount

    # reset variables
    loginErrorMsg = False
    verifErrorMsg = False
    transactionErrorMsg = ""
    username = ''
    receipt = []
    sessionWithdrawedAmount = 0


# MATEJ function to clear all the frames in a window
def clearFrame(window):
    for frames in window.winfo_children():
        frames.destroy()


# MATEJ function to clear all widgets in a frame
def clearTransactionError(frame):
    for widgets in frame.winfo_children():
        widgets.destroy()


# start the program!!!
if __name__ == "__main__":
    main()
