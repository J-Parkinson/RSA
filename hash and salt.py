import hashlib, binascii, os
from tkinter import *
from tkinter import messagebox, simpledialog
from ast import literal_eval
from validate_email import validate_email

def createUser():
    user = {}
    with open("passwords.txt", "r+") as readdict:
        passwords = readdict.read().split("\n")[:-1]
    for x in range(len(passwords)):
        passwords[x] = literal_eval(passwords[x])
        if passwords[x]["Username"] == username.get():
            messagebox.showerror("Username taken", "This username is already taken. Please try another username.")
            return
    email = simpledialog.askstring("Email", "Please enter your email address.")
    if email == None:
        messagebox.showwarning("Warning", "You left the email box blank. Please re-enter your details.")
        return
    elif not validate_email(email):
        messagebox.showerror("Error", "This is not a valid email address. Please use a different email address.")
        return
    for x in range(len(passwords)):
        if email == passwords[x]["Email"]:
            messagebox.showerror("Error", "This email has already been used. Please use a different email address.")
            return
    user["Email"] = email
    user["Username"] = username.get()
    user["Salt"] = os.urandom(16)
    dk = hashlib.pbkdf2_hmac('sha512', password.get().encode(), user["Salt"], 146723)
    user["Hash"] = binascii.hexlify(dk) # b' ' is wrapper
    with open("passwords.txt", "a+") as passwords:
        passwords.write(str(user) + "\n")
    messagebox.showinfo("Account made", "You have successfully created an account.")
    return

def checkUser():
    with open("passwords.txt", "r+") as readdict:
        passwords = readdict.read().split("\n")[:-1]
    found = False
    for x in range(len(passwords)):
        passwords[x] = literal_eval(passwords[x])
        if passwords[x]["Username"] == username.get():
            hash = binascii.hexlify(hashlib.pbkdf2_hmac('sha512', password.get().encode(), passwords[x]["Salt"], 146723))
            if hash == passwords[x]["Hash"]:
                found = True
                messagebox.showinfo("Log in", "You have been logged in, " + passwords[x]["Username"] + ".")
    if not found:
        messagebox.showerror("Error", "Your username or password is incorrect. Please check your input.")
    return

def resetPassword():
    email = simpledialog.askstring("Email", "Please enter your email address.")
    if email == None:
        messagebox.showwarning("Warning", "You left the email box blank. Please re-enter your details.")
        return
    elif not validate_email(email):
        messagebox.showerror("Error", "This is not a valid email address. Please use a different email address.")
        return
    with open("passwords.txt", "r+") as readdict:
        passwords = readdict.read().split("\n")[:-1]
    found = False
    for x in range(len(passwords)):
        passwords[x] = literal_eval(passwords[x])
        if passwords[x]["Username"] == username.get() and passwords[x]["Email"] == email:
            passwords[x]["Hash"] = binascii.hexlify(hashlib.pbkdf2_hmac('sha512', simpledialog.askstring("Password", "Please enter your new password.", show="*").encode(), passwords[x]["Salt"], 146723))
            found = True
    if found:
        with open("passwords.txt", "r+") as readdict:
            readdict.truncate()
            for x in range(len(passwords)):
                readdict.write(str(passwords[x]) + "\n")
        messagebox.showinfo("Password changed", "Your password has been changed successfully.")
    else:
        messagebox.showerror("Error", "This account does not exist. Check your input.")
    return

root = Tk()

usernameL = Label(root, text="Username:")
usernameL.grid(row=0, column=0)

username = Entry(root, justify="center")
username.grid(row=0, column=1)

passwordL = Label(root, text="Password:")
passwordL.grid(row=1, column=0)

password = Entry(root, justify="center", show="*")
password.grid(row=1, column=1)

new = Button(root, text="New account", command=createUser)
new.grid(row=2, column=0)

ok = Button(root, text="OK", command=checkUser)
ok.grid(row=2, column=1)

forgot = Button(root, text="Forgot your password?", command=resetPassword)
forgot.grid(row=3, column=0, columnspan=2)

mainloop()