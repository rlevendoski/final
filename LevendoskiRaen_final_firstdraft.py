from tkinter import *
import sqlite3 as sq #For tables and database

#Main Window formatting
window1 = Tk() 
window1.title("1Basket") 
window1.geometry('800x600+0+0')
window1.configure(bg="lemon chiffon")
header = Label(window1, text="Eggs in 1Basket", font=("verdana",30), fg="dodger blue", bg="lemon chiffon").pack()

con = sq.connect('eggs.db') #dB field
c = con.cursor() #to call execute

#Label formatting
L1 = Label(window1, text = "Chicken", font=("georgia", 15), fg= "dodger blue", bg="lemon chiffon").place(x=10,y=100)
L2 = Label(window1, text = "Egg Count", font=("georgia",15), fg= "dodger blue", bg="lemon chiffon").place(x=10,y=150)

#Create variables
chick = StringVar(window1) #Chicken Selection Dropdown list
chick.set('----') #Placeholder for field

chkndb = StringVar(window1)#Database dropdown list
chkndb.set('----') #Placeholder

eggs = StringVar(window1)

#Dictionary for drop down list
chickens = {'Plymouth Rock', 'Rhode Island Red', 'Leghorn', 'Jersey Giant', 'Ameracauna', 'Other'}

chkn = OptionMenu(window1, chick, *chickens) #For 1st drop down list 
chkn.place(x=150,y=105)

chkndbase = OptionMenu(window1, chkndb, *chickens) #For 2nd drop down list
chkndbase.place(x=100,y=350)

#Entry for input box
eggT = Entry(window1, textvariable=eggs)
eggT.place(x=150,y=150)

#get function to submit entered data to database
def get():
        print("Thank you for submitting eggs.")
        #create or save to databases
        c.execute('CREATE TABLE IF NOT EXISTS' +chick.get()+ ' (Eggs INTEGER)') #SQL syntax
        c.execute('INSERT INTO ' +chick.get()+  ' (Eggs) VALUES (?)', (eggs.get())) #Insert record into database.
        con.commit()

#Reset fields after submit
        chick.set('----')
        eggs.set('')

#Clear boxes when submit button is hit
def clear():
    chick.set('----')
    chkndb.set('----')
    eggs.set('')
    
def record():
    c.execute('SELECT * FROM ' +chkndb.get()) 

    frame = Frame(window1)
    frame.place(x= 400, y = 175)
    
    Lb = Listbox(frame, height = 8, width = 25,font=("georgia", 12), fg= "dodger blue", bg="lemon chiffon") 
    Lb.pack(side = LEFT, fill = Y)
    
    scroll = Scrollbar(frame, orient = VERTICAL) #set scrollbar to list box for when entries exceed size of list box
    scroll.config(command = Lb.yview)
    scroll.pack(side = RIGHT, fill = Y)
    Lb.config(yscrollcommand = scroll.set) 
    
    Lb.insert(0, 'Date - Eggs') #first row in listbox
    
    data = c.fetchall() #Gets the data from the table
    
    for row in data:
        Lb.insert(1,row) # Inserts record row by row in list box

    L3 = Label(window1, text = chkndb.get()+ '      ', font=("georgia", 12), fg= "dodger blue", bg="lemon chiffon").place(x=400,y=100)
    L4 = Label(window1, text = "From most recent:", font=("georgia", 12), fg= "dodger blue", bg="lemon chiffon").place(x=400,y=150)
    con.commit() 

button_1 = Button(window1, text="Submit",command=get)
button_1.place(x=100,y=300)

button_2 = Button(window1,text= "Clear",command=clear)
button_2.place(x=10,y=300)

button_3 = Button(window1,text="Get DB",command=record)
button_3.place(x=10,y=350)

window1.mainloop() #run program