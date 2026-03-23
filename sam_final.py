import tkinter as tk
from tkinter import *
from pathlib import Path
from tkinter.font import Font
import sqlite3
import random

# ------- FOLDERS -------
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / "Assets"
def init_db():
    con = sqlite3.connect('sam_database.db')
    db = con.cursor()

    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT,
            password TEXT,
            balance INTEGER
        )
    """)

    db.execute("""
        CREATE TABLE IF NOT EXISTS history (
            owner_id INTEGER,
            send_rec_id INTEGER,
            send_rec_name TEXT,
            sent_amount INTEGER,
            recieved_amount INTEGER
        )
    """)
    
    con.commit()
    con.close()

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# ------- VALIDATION -------
def validate_email(email):
    con = sqlite3.connect('sam_database.db')
    db = con.cursor()
    db.execute('SELECT email FROM users')
    email_list = db.fetchall()
    for i in email_list:
        if i[0] == email:
            return False
    return True
def validated(email, password):#it will validate using datbase 
    # TEMPORARY – replace with actual DB check
    emailstat = False
    passwordstat = False
    conn = sqlite3.connect('sam_database.db')
    db = conn.cursor()
    db.execute("SELECT email FROM users")
    email_list = db.fetchall()
    db.execute("SELECT password FROM users")
    password_list = db.fetchall()
    conn.close()
    for i in email_list:
        email_string = i[0]
        if email_string == email:
            emailstat = True
            break
    for j in password_list:
        pass_string = j[0]
        if pass_string == password:
            passwordstat = True
            break
    if passwordstat is True and emailstat is True:
        return True
    else:
        return False

init_db()

# ------- MAIN WINDOW -------
win = tk.Tk()
win.geometry("754x504")
win.resizable(False, False)
win.title("SAM Bank")

# ------- global dictionary to store all the images used -------
imgs = {}

#create landing page
def open_landing_page():
    Landing_page = Canvas(
        win, bg="#FFFFFF", height=504, width=745,
        bd=0, highlightthickness=0, relief="ridge"
    )
    Landing_page.place(x=0, y=0)

    imgs["landing_bg"] = PhotoImage(file=relative_to_assets("Background.png"))
    Landing_page.create_image(372, 252, image=imgs["landing_bg"])

    # Centered Title (X=377 is center of 745 width)
    Landing_page.create_text(
        377, 185, anchor="center", # Centered text
        text="WELCOME TO SAM BANK LIMITED !",
        fill="#FFFFFF",
        font=("Helvetica", 25, "bold") # H1
    )

    imgs["landing_login"] = PhotoImage(file=relative_to_assets("login_button_landing.png"))
    Button(
        win, image=imgs["landing_login"],
        borderwidth=0, highlightthickness=0, relief="flat",
        command=login
    ).place(x=254, y=241, width=237, height=65)

    imgs["landing_signup"] = PhotoImage(file=relative_to_assets("sign_up_landing.png"))
    Button(
        win, image=imgs["landing_signup"],
        borderwidth=0, highlightthickness=0, relief="flat",
        command=singup
    ).place(x=254, y=319, width=237, height=65)

    imgs["logo_big"] = PhotoImage(file=relative_to_assets("logo_large.png"))
    Landing_page.create_image(370, 107, image=imgs["logo_big"])

    # Centered Footer Text
    Landing_page.create_text(
        377, 433, anchor="center", 
        text="Powered by SAM Tech", fill="#FFFFFF", font=("Arial", 10) # Small
    )
    Landing_page.create_text(
        377, 450, anchor="center", 
        text="All rights reserved", fill="#FFFFFF", font=("Arial", 7) # Small
    )
# ------- CREATE HOME PAGE -------
def open_home_page(id):
    con = sqlite3.connect("sam_database.db")
    db = con.cursor()
    db.execute("SELECT name FROM users WHERE id = ?" , (id,))
    last_name= db.fetchall() #pull from database
    last_name = last_name[0]
    last_name = last_name[0]
    db.execute("SELECT balance FROM users WHERE id = ?" , (id,))
    balance = db.fetchall()
    balance = balance[0]
    balance = balance[0] #pull from database 
    home_canvas = Canvas(
        win, bg="#FFFFFF", height=504, width=745,
        bd=0, highlightthickness=0, relief="ridge"
    )
    home_canvas.place(x=0, y=0)  

    imgs["home_bg"] = PhotoImage(file=relative_to_assets("Background.png"))
    home_canvas.create_image(377, 252, image=imgs["home_bg"])

    imgs["bar"] = PhotoImage(file=relative_to_assets("BAR.png"))
    home_canvas.create_image(377, 195, image=imgs["bar"])

    imgs["sam logo"] = PhotoImage(file=relative_to_assets("sam_logo.png"))
    home_canvas.create_image(370, 75, image=imgs["sam logo"])

    # Welcome Text (Centred based on the overall canvas, even if the bar is offset slightly)
    home_canvas.create_text(377, 135,
    anchor="center", # Centred
    text="Welcome, {0}  ".format(last_name),
    fill="#FFFFFF",
    font=("Arial", 18, "bold") # H3
    )
    
    # Balance Text (Kept offset to align with the bar graphic)
    home_canvas.create_text(290, 180,
    anchor="nw", # Left-aligned to coordinate 260
    text="PKR: {0}  ".format(balance),
    fill="#FFFFFF",
    font=("Arial", 20, "bold") # H3
    )

    imgs["exit_button"] = PhotoImage(file=relative_to_assets("exit.png"))
    Button(
        home_canvas,
        image=imgs["exit_button"],
        borderwidth=0,
        relief="flat",
        command=open_landing_page
    ).place(x=20, y=20, width=64, height=61)

    imgs["send_button"] = PhotoImage(file=relative_to_assets("SEND.png"))
    Button(
        home_canvas,
        image=imgs["send_button"],
        borderwidth=0,
        relief="flat",
        command= lambda : send_money(id)
    ).place(x=55, y=255, width=189, height=207)
    
    imgs["history_button"] = PhotoImage(file=relative_to_assets("HISTORY.png"))
    Button(
        home_canvas,
        image=imgs["history_button"],
        borderwidth=0,
        relief="flat",
        command= lambda : history_page(id)
    ).place(x=275, y=255, width=189, height=207)

    imgs["rewards_button"] = PhotoImage(file=relative_to_assets("REWARDS.png"))
    Button(
        home_canvas,
        image=imgs["rewards_button"],
        borderwidth=0,
        relief="flat",
        command=lambda:open_ttt(id,home_canvas)
    ).place(x=495, y=255, width=189, height=207)
 

# -------- LOGIN PAGE -------
def login_page_login(email_entry, pass_entry, login_canvas):# the final button on login page
    email = email_entry.get()
    password = pass_entry.get()
    if validated(email, password):
        con = sqlite3.connect("sam_database.db")
        db = con.cursor()
        db.execute("SELECT id FROM users WHERE email = ?" , (email,))
        id = db.fetchall()
        id = id[0]
        id = id[0]
        login_canvas.destroy()
        open_home_page(id)
    else:
        # Align warning text to the left of the backdrop/entry area
        login_canvas.create_text(
            228, 346,
            anchor="nw",
            text="*Incorrect email or password",
            fill="#D0FF00",
            font=("Arial", 15) # Body/Details
        )
    


# NEXT BUTTON FUNCTION:
def signup_next(pass_entry,email_entry,fname_entry,lname_entry,signup_canvas):
    con = sqlite3.connect('sam_database.db')
    db = con.cursor()
    email=email_entry.get()
    fname=fname_entry.get()
    lname=lname_entry.get()
    name = fname + " " + lname
    pswd=pass_entry.get()
    #if email not in data base progress else print account already exists
    if validate_email(email) is False:
        # Align warning text to the left of the entry area
        signup_canvas.create_text(
        355, 300,
        anchor="nw",
        text="*Email already in use",
        fill="#D0FF00",
        font=("Arial", 15)) # Body/Details
        
    else:
        id = random.randint(1000000 , 2000000)
        insert_query = "INSERT INTO users (id , name , email , password, balance) VALUES (? , ? , ? , ?, ?)"
        db.execute(insert_query , (id , name , email , pswd , 5000))
        con.commit()
        open_landing_page()
        con.close()
#-------------sign up page
def singup():
    signup_canvas = Canvas(
        win, bg="#FFFFFF", height=504, width=745,
        bd=0, highlightthickness=0, relief="ridge"
    )
    signup_canvas.place(x=0, y=0)

    imgs["home_bg"] = PhotoImage(file=relative_to_assets("Background.png"))
    signup_canvas.create_image(377,252, image=imgs["home_bg"])
    imgs["backdrop"] = PhotoImage(file=relative_to_assets("backdrop.png"))
    signup_canvas.create_image(377,308, image=imgs["backdrop"])
    imgs["logo_small"] = PhotoImage(file=relative_to_assets("logo_small.png"))
    signup_canvas.create_image(378, 86, image=imgs["logo_small"])

    # --- TEXT ---
    # Center section title
    signup_canvas.create_text(377, 175, anchor="center", text="Personal Information", fill="#FFFFFF", font=("Arial", 18, "bold")) # H3    
    
    # Labels (Left-aligned to entry fields)
    signup_canvas.create_text(220, 220, anchor="nw", text="First Name", fill="#FFFFFF", font=("Arial", 15)) # Body/Details
    signup_canvas.create_text(220, 285, anchor="nw", text="Email", fill="#FFFFFF", font=("Arial", 15)) # Body/Details
    signup_canvas.create_text(220, 343, anchor="nw", text="Password", fill="#FFFFFF", font=("Arial", 15)) # Body/Details
    signup_canvas.create_text(385, 220, anchor="nw", text="Last Name", fill="#FFFFFF", font=("Arial", 15)) # Body/Details
    
    First_name_entry= Entry(win, font=("Arial", 14)) # Input Field
    First_name_entry.place(x=220, y=250, width=140, height=28)
    Email_entry= Entry(win, font=("Arial", 14)) # Input Field
    Email_entry.place(x=220, y=310, width=305, height=28)
    Last_name_entry= Entry(win, font=("Arial", 14)) # Input Field
    Last_name_entry.place(x=385, y=250, width=140, height=28)
    pass_entry= Entry(win, font=("Arial", 14),show="*") # Input Field
    pass_entry.place(x=220, y=370, width=305, height=28)

    # --- NEXT BUTTON ---
    imgs["btn_next"] = PhotoImage(file=relative_to_assets("nextbutton.png"))
    Button(
        win,
        image=imgs["btn_next"],
        borderwidth=0,
        highlightthickness=0,
        relief="flat",
        command= lambda:signup_next(pass_entry,Email_entry,First_name_entry,Last_name_entry,signup_canvas)
    ).place(x=287,y=410 , width=172, height=48)

    imgs["exit_button"] = PhotoImage(file=relative_to_assets("exit.png"))
    Button(
        signup_canvas,
        image=imgs["exit_button"],
        borderwidth=0,
        relief="flat",
        command=open_landing_page
    ).place(x=20, y=20, width=64, height=61)


#SIGN UP PAGE ASSETS BEING LOADED IN 
    
    

    # LOAD THE LOGIN PAGE

def login():
    
    # Check if Landing_page exists before trying to destroy it (it's globally scoped but better to be safe)
    global Landing_page
    if 'Landing_page' in globals() and isinstance(Landing_page, Canvas):
        Landing_page.destroy()

    login_canvas = Canvas(
        win, bg="#FFFFFF", height=504, width=745,
        bd=0, highlightthickness=0, relief="ridge"
    )
    login_canvas.place(x=0, y=0)

    # --- LOAD IMAGES & STORE ---
    imgs["login_bg"] = PhotoImage(file=relative_to_assets("Background.png"))
    login_canvas.create_image(377, 252, image=imgs["login_bg"])

    imgs["logo_small"] = PhotoImage(file=relative_to_assets("logo_small.png"))
    login_canvas.create_image(378, 86, image=imgs["logo_small"])

    imgs["backdrop"] = PhotoImage(file=relative_to_assets("backdrop.png"))
    login_canvas.create_image(377, 308, image=imgs["backdrop"])

    # --- ENTRIES ---
    email_entry = Entry(win, font=("Arial", 14)) # Input Field
    email_entry.place(x=235, y=230, width=285, height=28)

    pass_entry = Entry(win, font=("Arial", 14), show="*") # Input Field
    pass_entry.place(x=235, y=303, width=285, height=28)

    # --- TEXT (Left-aligned to entry fields) ---
    login_canvas.create_text(237, 200, anchor="nw", text="Email", fill="#FFFFFF", font=("Arial", 15)) # Body/Details
    login_canvas.create_text(237, 273, anchor="nw", text="Password", fill="#FFFFFF", font=("Arial", 15)) # Body/Details

    # --- SIGN IN BUTTON ---
    imgs["btn_signin"] = PhotoImage(file=relative_to_assets("sign_in_login.png"))
    Button(
        win,
        image=imgs["btn_signin"],
        borderwidth=0,
        highlightthickness=0,
        relief="flat",
        command=lambda: login_page_login(email_entry, pass_entry, login_canvas)
    ).place(x=259, y=382, width=237, height=65)

    imgs["exit_button"] = PhotoImage(file=relative_to_assets("exit.png"))
    Button(
        login_canvas,
        image=imgs["exit_button"],
        borderwidth=0,
        relief="flat",
        command=open_landing_page
    ).place(x=20, y=20, width=64, height=61)

# -------Initial landing page-------
# Note: This block is executed *immediately* when the script runs to set up the initial screen.
# It uses the same updated fonts as open_landing_page().
Landing_page = Canvas(
    win, bg="#FFFFFF", height=504, width=745,
    bd=0, highlightthickness=0, relief="ridge"
)
Landing_page.place(x=0, y=0)

imgs["landing_bg"] = PhotoImage(file=relative_to_assets("Background.png"))
Landing_page.create_image(372, 252, image=imgs["landing_bg"])

# Centered Title (X=377 is center of 745 width)
Landing_page.create_text(
    377, 185, anchor="center",
    text="WELCOME TO SAM BANK LIMITED !",
    fill="#FFFFFF",
    font=("Helvetica", 25, "bold") # H1
)

imgs["landing_login"] = PhotoImage(file=relative_to_assets("login_button_landing.png"))
Button(
    win, image=imgs["landing_login"],
    borderwidth=0, highlightthickness=0, relief="flat",
    command=login
).place(x=254, y=241, width=237, height=65)

imgs["landing_signup"] = PhotoImage(file=relative_to_assets("sign_up_landing.png"))
Button(
    win, image=imgs["landing_signup"],
    borderwidth=0, highlightthickness=0, relief="flat",
    command=singup
).place(x=254, y=319, width=237, height=65)

imgs["logo_big"] = PhotoImage(file=relative_to_assets("logo_large.png"))
Landing_page.create_image(370, 107, image=imgs["logo_big"])

# Centered Footer Text
Landing_page.create_text(
    377, 433, anchor="center",
    text="Powered by SAM Tech", fill="#FFFFFF", font=("Arial", 10) # Small
)
Landing_page.create_text(
    377, 450, anchor="center",
    text="All rights reserved", fill="#FFFFFF", font=("Arial", 7) # Small
)

def send_money_backend(id , acc_number , amount):
    con = sqlite3.connect("sam_database.db")
    db= con.cursor()
    try:
        amount = int(amount)
        acc_number = int(acc_number)
    except ValueError:
        return 3 # Invalid number format

    db.execute("SELECT EXISTS(SELECT 1 FROM users WHERE id = ?)" , (acc_number,))
    id_status = db.fetchone()[0]
    if not id_status:
        return 1 #return value 1 indicates account not found
    else:
        db.execute("SELECT balance FROM users WHERE id = ?" , (id,))
        balance = db.fetchall()
        balance = balance[0]
        balance = balance[0]
        if balance - amount < 0:
            return 2 #return value 2 indicates insufficient balance
        else:
            balance = balance - amount
            db.execute("UPDATE users SET balance = ? WHERE id = ?" , (balance , id))
            db.execute("SELECT balance FROM users WHERE id = ?" , (acc_number,))
            reciepent_balance = db.fetchall()
            reciepent_balance = reciepent_balance[0]
            reciepent_balance = reciepent_balance[0]
            reciepent_balance += amount
            db.execute("SELECT name FROM users WHERE id = ?", (acc_number,))
            reciepent_name = db.fetchall()[0]
            reciepent_name = reciepent_name[0]
            db.execute("SELECT name FROM users WHERE id = ?" , (id,))
            sender_name = db.fetchall()[0]
            sender_name = sender_name[0]
            db.execute("UPDATE users SET balance = ? WHERE id = ?" , (reciepent_balance , acc_number))
            db.execute("INSERT INTO history (owner_id , send_rec_id, send_rec_name, sent_amount, recieved_amount) VALUES "
            "(?, ?, ?, ?, ?)" , (id, acc_number, reciepent_name, amount, 0))
            db.execute("INSERT INTO history (owner_id , send_rec_id, send_rec_name, sent_amount, recieved_amount) VALUES "
            "(?, ?, ?, ?, ?)" , (acc_number , id, sender_name, 0, amount))
            con.commit()
            
            return 0 #return value 0 indicates successful operation



def send_money_validation(id, acc_number, amount):
    # This print statement needs to be handled visually in the GUI, but for now we'll keep the logic.
    if not acc_number or not amount:
        print("Please fill all fields")
        return
        
    backend_status = send_money_backend(id, acc_number, amount)
    
    # For a real application, replace these prints with a GUI message box/label
    if backend_status == 0:
        print("Transfer successful!")
        open_home_page(id)
    elif backend_status == 1:
        print("Account not found")
    elif backend_status == 2:
        print("Insufficient balance")
    elif backend_status == 3:
        print("Invalid account number or amount format")
    else:
        print("Transfer failed")

def history_page(id):
    for widget in win.winfo_children():
        if isinstance(widget, Canvas):
            widget.destroy()
    
    history_page = Canvas(
        win, bg="#FFFFFF", height = 504, width = 745,
        bd = 0, highlightthickness=0, relief="ridge"
    )
    history_page.place(x=0,y=0)

#background
    imgs["landing_bg"] = PhotoImage(file=relative_to_assets("Background.png"))
    history_page.create_image(372, 252, image=imgs["landing_bg"])
    
    # Title for History Page (Centred)
    history_page.create_text(
        377, 120, anchor="center", text="TRANSACTION HISTORY",
        fill="#FFFFFF", font=("Arial", 24, "bold")) # H2
    history_page.create_text(97,170,anchor="center",text="RECIEVER'S ID",fill="#FFFFFF", font=("Arial", 12))
    history_page.create_text(277,170,anchor="center",text="NAME",fill="#FFFFFF", font=("Arial", 12))
    history_page.create_text(447,170,anchor="center",text="SENT AMOUNT",fill="#FFFFFF", font=("Arial", 12))
    history_page.create_text(637,170,anchor="center",text="RECIEVED AMOUNT",fill="#FFFFFF", font=("Arial", 12))
    

    con = sqlite3.connect("sam_database.db")
    db = con.cursor()
    db.execute("SELECT * FROM history WHERE owner_id = ? LIMIT 10" , (id,))
    history_data = db.fetchall()

    height = 200
    while len(history_data) > 0 and height<450:
        sender_id = history_data[0][1]
        sender_name = history_data[0][2]
        sent_amount = history_data[0][3]
        received_amount = history_data[0][4]
        history_page.create_text(97,height,anchor="center",text=str(sender_id),fill="#FFFFFF", font=("Arial", 10))
        history_page.create_text(277,height,anchor="center",text=sender_name,fill="#FFFFFF", font=("Arial", 10))
        history_page.create_text(447,height,anchor="center",text=sent_amount,fill="#FFFFFF", font=("Arial", 10))
        history_page.create_text(637,height,anchor="center",text=received_amount,fill="#FFFFFF", font=("Arial", 10))
        history_data = history_data[1:]
        height += 25

    


    imgs["exit_button"] = PhotoImage(file=relative_to_assets("exit.png"))
    Button(history_page, image=imgs["exit_button"],
        borderwidth=0, relief="flat", command= lambda: open_home_page(id)
    ).place(x=20, y=20, width=64, height=61)


#transfer money 
def send_money(id):

    for widget in win.winfo_children():
        if isinstance(widget, Canvas):
            widget.destroy()
            
    send_money_page = Canvas(
        win, bg="#FFFFFF", height=504, width=745,
        bd=0, highlightthickness=0, relief="ridge"
    )
    send_money_page.place(x=0, y=0)

    # Background
    imgs["landing_bg"] = PhotoImage(file=relative_to_assets("Background.png"))
    send_money_page.create_image(372, 252, image=imgs["landing_bg"])


    imgs["back1_bg"] = PhotoImage(file=relative_to_assets("new_back.png"))
    send_money_page.create_image(202, 292, image=imgs["back1_bg"])


    imgs["back2_bg"] = PhotoImage(file=relative_to_assets("new_back.png"))
    send_money_page.create_image(552, 292, image=imgs["back2_bg"])
    # Button
    imgs["transfer_button"] = PhotoImage(file=relative_to_assets("TRANSFER_BUTTON.png"))
    Button(
        win,
        image=imgs["transfer_button"],    
        borderwidth=0,
        highlightthickness=0,
        relief="flat",
        command= lambda: send_money_validation(id , acc_entry.get() , amount_entry.get())
    ).place(x=104, y=410, width=196, height=59)

    # Labels (Aligned to the left side of the respective backdrop areas)
    send_money_page.create_text(202, 140, anchor="center", text="TRANSFER MONEY",
        fill="#EEEBEB", font=("Arial", 22, "bold")) # H2

    send_money_page.create_text(552, 140, anchor="center", text="YOUR DETAILS",
        fill="#EEEBEB", font=("Arial", 22, "bold")) # H2

    # Recipient ID (Aligned to entry field)
    send_money_page.create_text(70, 195, text="Recipient's ID:",
        anchor="nw", fill="#EEEBEB", font=("Arial", 15)) # Body/Details

    acc_entry = Entry(win, font=("Arial", 14)) # Input Field
    acc_entry.place(x=70, y=230, width=265, height=50)

    # Amount (Aligned to entry field)
    send_money_page.create_text(70, 305, text="Amount to Transfer",
        anchor="nw", fill="#EEEBEB", font=("Arial", 15)) # Body/Details

    amount_entry = Entry(win, font=("Arial", 14)) # Input Field
    amount_entry.place(x=70, y=335, width=265, height=50)

    con = sqlite3.connect("sam_database.db")
    db = con.cursor()
    db.execute("SELECT name FROM users WHERE id = ?" , (id,))
    name = db.fetchall()
    name = name[0]
    name = name[0]
    db.execute("SELECT email FROM users WHERE id = ?" , (id,))
    email = db.fetchall()
    email = email[0]
    email = email[0]

    # Your Details (Aligned to the left of the details backdrop)
    send_money_page.create_text(450, 195, anchor="nw",
        text="Name: " + name, fill="#EEEBEB", font=("Arial", 15)) # Body/Details
    send_money_page.create_text(450, 250, anchor="nw",
        text="ID: " + str(id), fill="#EEEBEB", font=("Arial", 15)) # Body/Details
    send_money_page.create_text(450, 305, anchor="nw",
        text="Email: " + email, fill="#EEEBEB", font=("Arial", 15)) # Body/Details

    # Exit button
    imgs["exit_button"] = PhotoImage(file=relative_to_assets("exit.png"))
    Button(send_money_page, image=imgs["exit_button"],
        borderwidth=0, relief="flat", command= lambda: open_home_page(id)
    ).place(x=20, y=20, width=64, height=61)



def end_of_game_result(board):
    # Check rows
    for r in range(3):
        if board[r][0] and board[r][0] == board[r][1] == board[r][2]:
            return "WIN" if board[r][0] == "X" else "LOSS"

    # Check columns
    for c in range(3):
        if board[0][c] and board[0][c] == board[1][c] == board[2][c]:
            return "WIN" if board[0][c] == "X" else "LOSS"

    # Check diagonals
    if board[0][0] and board[0][0] == board[1][1] == board[2][2]:
        return "WIN" if board[0][0] == "X" else "LOSS"
    if board[0][2] and board[0][2] == board[1][1] == board[2][0]:
        return "WIN" if board[0][2] == "X" else "LOSS"

    # Check draw
    for r in range(3):
        for c in range(3):
            if board[r][c] is None:
                return None  # game still running

    return "DRAW"

def open_ttt(id, home_canvas):

    # destroy old page
    home_canvas.destroy()

    ttt_canvas = Canvas(
        win, bg="#FFFFFF", height=504, width=745,
        bd=0, highlightthickness=0, relief="ridge"
    )
    ttt_canvas.place(x=0, y=0)

    # background
    imgs["home_bg"] = PhotoImage(file=relative_to_assets("Background.png"))
    ttt_canvas.create_image(377, 252, image=imgs["home_bg"])

    # Title (Centered)
    ttt_canvas.create_text(
        377, 40, anchor="center",
        text="TIC TAC TOE",
        fill="#FFFFFF",
        font=("Helvetica", 28, "bold") # H1
    )

    # Back button
    imgs["exit_button"] = PhotoImage(file=relative_to_assets("exit.png"))
    Button(
        ttt_canvas,
        image=imgs["exit_button"],
        borderwidth=0,
        relief="flat",
        command=lambda: open_home_page(id)
    ).place(x=20, y=20, width=64, height=61)

    # GAME STATE
    board = [[None]*3 for _ in range(3)]
    buttons = [[None]*3 for _ in range(3)]

    # RESULT LABEL (Centered)
    result_label = Label(
        ttt_canvas,
        text="",
        font=("Arial", 18, "bold"), # H3
        bg="#0B0D33",
        fg="white"
    )
    # Positioning adjusted to be central beneath the game board
    result_label.place(x=377, y=420, anchor="center") 

    # --- SHOW RESULT ---
    def show_result(res):
        if res == "WIN":
            result_label.config(text="YOU WON 67 PKR!", fg="#00FF99")
            con = sqlite3.connect("sam_database.db")
            db = con.cursor()
            db.execute("SELECT balance FROM users WHERE id = ?" , (id,))
            balance = db.fetchall()[0]
            balance = balance[0]
            balance = balance + 67
            db.execute("UPDATE users SET balance = ? WHERE id = ?" , (balance , id))
            con.commit()
        elif res == "LOSS":
            result_label.config(text="YOU LOST!", fg="#FF4444")
        else:
            result_label.config(text="DRAW!", fg="white")


    # --- COMPUTER MOVE ---
    def computer_move():
        empty = [(r, c) for r in range(3) for c in range(3) if board[r][c] is None]
        if not empty:
            return

        r, c = random.choice(empty)
        board[r][c] = "O"
        buttons[r][c].config(text="O", fg="white")

        result = end_of_game_result(board)
        if result:
            show_result(result)


    # --- PLAYER MOVE ---
    def click(r, c):
        if board[r][c] is not None:
            return  # box filled

        board[r][c] = "X"
        buttons[r][c].config(text="X", fg="white")

        result = end_of_game_result(board)
        if result:
            show_result(result)
            return

        # Make computer move 200ms after player
        win.after(200, computer_move)


    # --- DRAW GRID (nested loops) ---
    start_x = 230
    start_y = 120
    size = 80
    gap = 12

    for r in range(3):
        for c in range(3):
            btn = Button(
                ttt_canvas,
                text="",
                font=("Arial", 30, "bold"), # Large for game pieces
                bg="#2F2A55",
                fg="white",
                activebackground="#4B3A88",
                bd=0,
                highlightthickness=0,
                relief="flat",
                command=lambda rr=r, cc=c: click(rr, cc)
            )

            btn.place(
                x=start_x + (size + gap) * c,
                y=start_y + (size + gap) * r,
                width=size,
                height=size
            )

            buttons[r][c] = btn

# ------- MAIN LOOP -------
win.mainloop()