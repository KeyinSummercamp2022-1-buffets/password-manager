from guizero import App, Text, TextBox, PushButton, Window, Box
import random
import api

##  Open and close windows  ##

token = ""
passwords = [[]]
username = ""
password = ""


def find_passwords():
    global passwords, username, password
    response = api.get_passwords(username, password, token)
    if "error" in response:
        app.warn("Error", response["error"])
        return
    passwords = response


def open_window():
    close_login()
    Window.show(sign_up_window)


def closed_window():
    Window.hide(sign_up_window)


def open_Vault():
    show_passwords()
    Window.show(Vault_window)


def close_Vault():
    Window.hide(Vault_window)


def open_Password():
    close_Vault()
    Window.show(Password_window)


def close_Password():
    Window.hide(Password_window)


def logging_off():
    global passwords, password, username, token
    username = ""
    password = ""
    passwords = [[]]
    token = ""
    close_Vault()
    show_login()


def show_login():
    app.show()


def close_login():
    app.hide()


def back_to_vault():
    close_Password()
    find_passwords()
    open_Vault()


def back_to_login():
    closed_window()
    show_login()


def signup():
    global token, username, password
    response = api.create(New_UserBox.value, New_PassBox.value)
    if "error" in response:
        app.warn("Error", response["error"])
        return
    response = api.login(New_UserBox.value, New_PassBox.value)
    if "error" in response:
        app.warn("Error", response["error"])
        return
    token = response["token"]
    username = New_UserBox.value
    password = New_PassBox.value
    closed_window()
    find_passwords()
    open_Vault()


def login():
    global token, passwords, username, password
    response = api.login(User_Box.value, Pass_Box.value)
    if "error" in response:
        app.warn("Error", response["error"])
        return
    token = response["token"]
    passwords = response
    username = User_Box.value
    password = Pass_Box.value
    close_login()
    closed_window()
    find_passwords()
    open_Vault()


##  Window 1  ##

app = App(title="MonkePass", layout="grid", bg="sky blue")


sign_up_window = Window(app, title="Sign Up", layout="grid", bg="MistyRose3")


Vault_window = Window(app, title="My Passwords", layout="grid", bg="MistyRose1")


Password_window = Window(app, title="New Password", layout="grid", bg="sky blue")


##  Login  ##

User = Text(app, text="User ID: ", size=20, grid=[0, 0], align="left", bg="white")
User_Box = TextBox(
    app,
    grid=[1, 0],
    align="left",
    width="fill",
)
User_Box.bg = "DarkOrange1"
User_Box.text_color = "blue"

Master_Pass = Text(
    app, text="Master Password: ", grid=[0, 1], size=20, align="left", bg="white"
)
Pass_Box = TextBox(app, align="left", grid=[1, 1], width="fill", hide_text=True)
Pass_Box.bg = "DarkOrange1"

Login = PushButton(
    app, text="Login", grid=[0, 2], align="left", width=5, height=2, command=login
)

Blank = Text(app, text="        ", grid=[0, 5], align="left", size=20)


##  Create Account  ##

Welcome = Text(
    app,
    text="Welcome to the jungle!",
    grid=[0, 6],
    align="left",
    size=15,
    font="Comic Sans MS",
)

Welcome_PT2 = Text(app, "If you're a new Monke, sign up below:", grid=[0, 7], align="left", size=15, font="Comic Sans MS")


Sign_Up = PushButton(
    app,
    text="Sign Up",
    grid=[0, 8],
    width=5,
    height=2,
    align="left",
    command=open_window,
)


##  Window 2  ##

New_User = Text(
    sign_up_window, text="User ID: ", size=20, grid=[0, 0], align="left", bg="white"
)
New_UserBox = TextBox(sign_up_window, grid=[1, 0], align="left", width="fill")
New_User.text_color = "red3"
New_UserBox.bg = "coral2"

New_Pass = Text(
    sign_up_window,
    text="Master Password: ",
    grid=[0, 1],
    size=20,
    align="left",
    bg="white",
)
New_PassBox = TextBox(
    sign_up_window, align="left", grid=[1, 1], width="fill", hide_text=True
)
New_Pass.text_color = "red3"
New_PassBox.bg = "coral2"


Confirm_Pass = Text(
    sign_up_window,
    text="Confirm Password: ",
    grid=[0, 3],
    size=20,
    align="left",
    bg="white",
)
Confirm_PassBox = TextBox(
    sign_up_window, align="left", grid=[1, 3], width="fill", hide_text=True
)
Confirm_Pass.text_color = "red3"
Confirm_PassBox.bg = "coral2"


def confirm_button():
    def match():
        sign_up_window.warn("Uh oh!", "Monke Brain Go Panic! Your answers don't seem to match.")

    def no_username():
        sign_up_window.warn("Oh uh!", "Monke Brain Go Panic! Please fill in all boxes.")

    def too_short():
        sign_up_window.warn("Uh oh!", "Monke Brain Go Panic! Please enter a password that is 12 characters.")

    def correct_password():
        signup()

    if (
        len(New_UserBox.value) == 0
        or len(New_PassBox.value) == 0
        or len(Confirm_PassBox.value) == 0
    ):
        Confirm.when_clicked = no_username
    elif len(New_PassBox.value) < 12 or len(Confirm_PassBox.value) < 12:
        Confirm.when_clicked = too_short
    else:
        if New_PassBox.value != Confirm_PassBox.value:
            Confirm.when_clicked = match
        elif New_PassBox.value == Confirm_PassBox.value:
            Confirm.when_clicked = correct_password


Back = PushButton(
    sign_up_window, text="Back", align="bottom", grid=[2, 0], command=back_to_login
)
Confirm = PushButton(
    sign_up_window, text="Confirm", align="right", grid=[2, 1], command=confirm_button
)


##  Window 3  ##


def show_passwords():
    global List_of_passwords, passwords
    List_of_passwords.destroy()
    List_of_passwords = Box(Vault_window, grid=[0, 1])
    for passwd in passwords[0]:
        Text(
            List_of_passwords,
            f"Title: {passwd['title']}, Username: {passwd['username']}, Password: {passwd['password']}",
        )


Blank_Button = PushButton(
    Vault_window, text="    Saved Passwords     ", grid=[0, 0], width=40
)
Plus_password = PushButton(Vault_window, text="+", grid=[5, 0], command=open_Password)
List_of_passwords = Box(Vault_window, grid=[0, 1])

Logout = PushButton(Vault_window, text="Log Out", grid=[5, 1], command=logging_off)


##  Window 4  ##


def save_password():
    global token, username, password, passwords
    response = api.new_password(
        username,
        password,
        token,
        Name_TextBox.value,
        Username_TextBox.value,
        Password_TextBox.value,
    )
    if "error" in response:
        app.warn("Error", response["error"])
        return
    Vault_window.info(
        "Success!!!!!!!!!!", "You've successfully created a new password!"
    )
    close_Password()
    find_passwords()
    open_Vault()


Password_Name = Text(
    Password_window, text="Title: ", size=20, grid=[0, 0], align="left"
)
Name_TextBox = TextBox(Password_window, grid=[1, 0], width="fill", align="left")
Name_TextBox.bg = "DarkOrange1"


Password_Username = Text(
    Password_window, text="Username/Email: ", size=20, grid=[0, 1], align="left"
)
Username_TextBox = TextBox(Password_window, grid=[1, 1], width="fill", align="left")
Username_TextBox.bg = "DarkOrange1"

Password_Pass = Text(
    Password_window, text="Password: ", size=20, grid=[0, 2], align="left"
)
Password_TextBox = TextBox(Password_window, grid=[1, 2], width="fill", align="left")
Password_TextBox.bg = "DarkOrange1"

Password_Blank = Text(
    Password_window, text="                  ", size=20, grid=[0, 3], width="fill"
)

Exit_Button = PushButton(
    Password_window,
    text="Back",
    height=1,
    width=2,
    grid=[0, 8],
    align="left",
    command=back_to_vault,
)
Save_Button = PushButton(
    Password_window, text="Save", height=1, width=2, grid=[1, 8], command=save_password
)

Password_Text = Text(
    Password_window, text="To generate a password: ", size=15, grid=[0, 4], align="left"
)
Password_Cont = Text(
    Password_window,
    text="Enter preferred number of characters.",
    size=15,
    grid=[0, 5],
    align="left",
)
Password_Length = TextBox(Password_window, grid=[1, 5], align="left", width=2, height=1)


def get_passwords():
    password_possibilities = (
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ,./?!@#$%&(){}1234567890"
    )

    try:
        length = int(Password_Length.value)
    except ValueError:
        Password_window.warn("Invalid Lenght", "That was not a number")
        return

    password = ""
    for _ in range(length):
        password += random.choice(password_possibilities)
        password = str(password)
        printpass = TextBox(
            Password_window,
            text=password,
            width=20,
            height=10,
            grid=[0, 10],
            visible=True,
            multiline=True,
        )
        printpass.text_color = "black"
        printpass.bg = "white"


Generate = PushButton(
    Password_window, command=get_passwords, text="Generate", grid=[1, 7]
)

Vault_window.hide()
sign_up_window.hide()
Password_window.hide()
app.display()
