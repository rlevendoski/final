from tkinter import *
import sqlite3
from PIL import ImageTk, Image
import numpy as np
import matplotlib.pyplot as plt

#Main Window / Home
root = Tk()
root.title("1Basket - Home")
root.geometry('800x600')

bg = ImageTk.PhotoImage(Image.open('final/images/rainboweggs.png')) #Background image

#Create a canvas for object transparent backgrounds
canvas = Canvas(root, width=800, height=400)
canvas.pack(fill="both", expand=True)

#Set image in canvas
canvas.create_image(0,0, image=bg, anchor="nw")

#Add a label
canvas.create_text(400, 250, text="Welcome to 1Basket!", font=('Georgia', 50), fill="white")

#Function for Eggs & Second Window
def add_eggs():
    global editor
    editor = Tk()
    editor.title('1Basket - Add Eggs')
    editor.configure(bg="lemon chiffon")
    editor.geometry('800x600+0+0')
    header = Label(editor, text="Add & Review Eggs", font=("Georgia", 30), fg="coral", bg="lemon chiffon")
    header.place(x=245, y=0)

    #Create or connect to DB + create cursor
    conn = sqlite3.connect('eggs.db')
    c = conn.cursor()

    #Label formatting for Chicken and Egg entry form
    L1 = Label(editor, text = "Chicken", font=("georgia", 15), fg= "coral", bg="lemon chiffon").place(x=10,y=100)
    L2 = Label(editor, text = "Egg Count", font=("georgia",15), fg= "coral", bg="lemon chiffon").place(x=10,y=150)

    #Create variables for chicken and egg entry form
    chick = StringVar(editor) #Chicken Selection Dropdown list
    chick.set('----') #Placeholder for field

    chkndb = StringVar(editor)#Database for 2nd dropdown list
    chkndb.set('----') #Placeholder

    eggs = StringVar(editor)

    #Dictionary for drop down list
    chickens = {'Jersey', 'Fancy', 'Leghorn', 'Other'}

    chkn = OptionMenu(editor, chick, *chickens) #For 1st drop down list 
    chkn.place(x=150,y=105)

    chkndbase = OptionMenu(editor, chkndb, *chickens) #For 2nd drop down list
    chkndbase.place(x=200,y=300)

    #Label for database egg info
    eggT = Entry(editor, textvariable=eggs, font=("georgia", 11))
    eggT.place(x=150,y=150)

    #get function to submit entered data to database
    def get():
        print("Thank you for submitting eggs.")
        #create or save to databases
        c.execute('CREATE TABLE IF NOT EXISTS ' + chick.get() + ' (Eggs INTEGER)')
        c.execute('INSERT INTO ' + chick.get() +  ' (Eggs) VALUES (?)', (eggs.get())) #Insert record into database.

        conn.commit()

        #Reset fields after submit
        chick.set('----')
        eggs.set('')

    #Close Window
    def close():
        add_eggs.destroy()

    #Record function for DB    
    def record():
        c.execute('SELECT * FROM ' +chkndb.get())
        #DB Frame
        frame = Frame(editor)
        frame.place(x= 400, y = 175)
        #Listbox for DB
        Lb = Listbox(frame, height = 8, width = 25,font=("georgia", 12), fg= "coral", bg="lemon chiffon") 
        Lb.pack(side = LEFT, fill = Y)
        #Scrollbar
        scroll = Scrollbar(frame, orient = VERTICAL) #set scrollbar to list box for when entries exceed size of list box
        scroll.config(command = Lb.yview)
        scroll.pack(side = RIGHT, fill = Y)
        Lb.config(yscrollcommand = scroll.set) 
        
        Lb.insert(0, 'Eggs Collected') #first row in listbox
        
        data = c.fetchall() #Gets the data from the table
        
        for row in data:
            Lb.insert(1,row) # Inserts record row by row in list box
        #Listbox labels
        L3 = Label(editor, text = chkndb.get()+ '      ', font=("georgia", 12), fg= "coral", bg="lemon chiffon").place(x=400,y=100)
        L4 = Label(editor, text = "From most recent:", font=("georgia", 12), fg= "coral", bg="lemon chiffon").place(x=400,y=150)
        conn.commit()
    #2nd Window buttons
    button_1 = Button(editor, text="Submit", font=("georgia", 11),command=get)
    button_1.place(x=10,y=300)
    
    button_2 = Button(editor,text="Get DB", font=("georgia", 11),command=record)
    button_2.place(x=100,y=300)
   
    button_3 = Button(editor,text= "Close", font=("georgia", 11),command=editor.destroy)
    button_3.place(x=300,y=300)
#Function for graph
def graph():
    conn=sqlite3.connect('eggs.db')
    c = conn.cursor()
    
    c.execute("SELECT chicken, eggs FROM eggs")
    downx = []
    downy = []
    for row in c.fetchall():
        downx.append(row[0])
        downy.append(row[1])

    plt.plot(downx, downy, '-')
    plt.show()

#Create Submit Button
eggs_btn = Button(root, text="Add Eggs", font=("georgia", 11), command=add_eggs)
eggs_btn_window = canvas.create_window(225, 300, anchor="nw", window=eggs_btn)

#Button for Graph - figure out how to graph different chickens
graph_btn = Button(root, text="Total Eggs (Graph)", font=("georgia", 11), command=graph)
graph_btn_window = canvas.create_window(320, 300, anchor="nw", window=graph_btn)

#Create Exit Button
exit = Button(root, text="Exit App", font=("georgia", 11),command=root.quit)
exit_window = canvas.create_window(480, 300, anchor="nw", window=exit)

#Run Program
root.mainloop()
