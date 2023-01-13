import sqlite3                    
from tkinter import *             
from tkinter import messagebox


class DB:                         
    def __init__(self):           
        self.conn = sqlite3.connect("TicketsDB.db")  
        self.cur = self.conn.cursor()    
        self.cur.execute(             
            "CREATE TABLE IF NOT EXISTS Ticket (id INTEGER PRIMARY KEY, customer TEXT, city TEXT, price TEXT)") 
        self.conn.commit() 

    def __del__(self):         
        self.conn.close()  

    def view(self):       
        self.cur.execute("SELECT * FROM Ticket") 
        rows = self.cur.fetchall() 
        return rows

    def insert(self, customer, city, price):  
        self.cur.execute("INSERT INTO Ticket VALUES (NULL,?,?,?)", (customer, city, price,)) 
        self.conn.commit()
        self.view()

    def update(self, id, customer, city):    
        self.cur.execute("UPDATE Ticket SET customer=?, city=? WHERE id=?", (customer, city, id,))
        self.conn.commit()
        self.view()

    def delete(self, id):                   
        self.cur.execute("DELETE FROM Ticket WHERE id=?", (id,))
        self.conn.commit()
        self.view()

    def search(self, customer="", city=""): 
        self.cur.execute("SELECT * FROM Ticket WHERE customer=? OR city=?", (customer, city,))
        rows = self.cur.fetchall()
        return rows


db = DB()  


def get_selected_row(event): 
    global selected_tuple
    try:
        index = list1.curselection()[0] 
        selected_tuple = list1.get(index) 
        e1.delete(0, END)                 
        e1.insert(END, selected_tuple[1]) 
        e2.delete(0, END)
        e2.insert(END, selected_tuple[2]) 
        e3.delete(0, END)
        e3.insert(END, selected_tuple[3]) 
    except IndexError:
        pass


def view_command():          
    list1.delete(0, END)  
    for row in db.view():   
        list1.insert(END, row)  


def search_command():       #to print the row we want based on customer or city 
    list1.delete(0, END)    #empty the list
    for row in db.search(customer_text.get(), city_text.get()): #get the name of the customer or the city and pass it to the search function of class DB
        list1.insert(END, row) #will insert all the rows having the same value of customer or city


def add_command():          #to add a new row into the table
    db.insert(customer_text.get(), city_text.get(), price_text.get()) #passing user input values 
    list1.delete(0, END) #empty the list
    list1.insert(END, (customer_text.get(), city_text.get(), price_text.get()))  #insert into the list and then the table, the values given by the user


def delete_command(): #deleting a row 
    db.delete(selected_tuple[0]) #calls the delete function of the class DB and passes the id as the parameter and condition
    view_command()


def update_command():
    db.update(selected_tuple[0], customer_text.get(), city_text.get()) #calls the update function of the class DB and passes the user input as parameters to update value of the row
    view_command()


window = Tk() 

window.title("My Tickets") 


def on_closing(): #destructor for the window
    dd = db
    if messagebox.askokcancel("Quit", "Do you want to quit?"): #when ok is clicked, displays the following message
        window.destroy()
        del dd #deletes the object once window has been closed


window.protocol("WM_DELETE_WINDOW", on_closing)  # handles window closing

l1 = Label(window, text="customer") #creating input labels in the window
l1.grid(row=0, column=0) #determining size of the input grid for these labels

l2 = Label(window, text="city")
l2.grid(row=0, column=2)

l3 = Label(window, text="price")
l3.grid(row=1, column=0)

customer_text = StringVar()
e1 = Entry(window, textvariable=customer_text) #taking input from the user in the grid and storing it in a string variable
e1.grid(row=0, column=1)

city_text = StringVar() #taking city name input
e2 = Entry(window, textvariable=city_text)
e2.grid(row=0, column=3)

price_text = StringVar() #taking price input
e3 = Entry(window, textvariable=price_text)
e3.grid(row=1, column=1)

list1 = Listbox(window, height=25, width=65) #creating the list space to display all the rows of the table
list1.grid(row=2, column=0, rowspan=6, columnspan=2) #determining the size

sb1 = Scrollbar(window) #creating a scrollbar for the window to scroll through the list entries
sb1.grid(row=2, column=2, rowspan=6)

list1.configure(yscrollcommand=sb1.set) #configuring the scroll function for the scrollbar object sb1
sb1.configure(command=list1.yview)

list1.bind('<<ListboxSelect>>', get_selected_row)

b1 = Button(window, text="View all", width=12, command=view_command) #creating buttons for the various operations. Giving it a name and assigning a particular command to it. 
b1.grid(row=2, column=3) #size of the button

b2 = Button(window, text="Search entry", width=12, command=search_command)
b2.grid(row=3, column=3)

b3 = Button(window, text="Add entry", width=12, command=add_command)
b3.grid(row=4, column=3)

b4 = Button(window, text="Update selected", width=12, command=update_command)
b4.grid(row=5, column=3)

b5 = Button(window, text="Delete selected", width=12, command=delete_command)
b5.grid(row=6, column=3)

b6 = Button(window, text="Close", width=12, command=window.destroy)
b6.grid(row=7, column=3)

window.mainloop() 
