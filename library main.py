# ~~~Advanced Library Management By Biswambhar Pal ~~~
# ~~~~~~ Biswambhar Pal ~~~~~~

from tkinter import *
from PIL import ImageTk,Image #pip install pillow
import tkinter.messagebox as tmsg
from tkinter import ttk 
import random
import sqlite3

root = Tk()
root.geometry("1350x740")
root.configure(bg="ghost white")
root.title("Library Management System")
root.iconbitmap("add_book.ico")
top_heading = Frame(root)
Label(top_heading,text="Library Management System By Biswambhar Pal",font="Britannic 18 bold",bg="royalblue1",fg="light cyan",relief=GROOVE).pack(fill=X,ipady=2,pady=10)
top_heading.pack(fill=X)

###########~~~~~~~~~~~~~~~Summary Button Window ~~~~~~~~~~~~~##########
def summary_func():
    global summary_window
    summary_window = Tk()
    summary_window.configure(bg="lightblue1")

    summary_window.geometry("900x500")
    Label(summary_window,text="LIBRARY MANAGEMENT SYSTEM \nBY \nBISWAMBHAR PAL",font="times 20 bold",bg="steelblue4",fg="snow",relief=RIDGE,padx=20,pady=10).pack(pady=(20,40))
    Label(summary_window,text="Summary",font="times 20 bold",bg="steelblue4",fg="snow",relief=RIDGE,padx=20,pady=10).pack(pady=(20,40))
     #Create a databse or connect to one   
    conn = sqlite3.connect("add_book_table.db")
    #create cursor
    cur = conn.cursor()

    book_no = cur.execute("SELECT * FROM books")
    book_no = book_no.fetchall()

    mem_no = cur.execute("SELECT * FROM members")
    mem_no = mem_no.fetchall()

    issued_no = cur.execute("SELECT * FROM issuedbooks")
    issued_no = issued_no.fetchall()


    frame = Frame(summary_window,bd=10,relief=RIDGE)
    
    count_book = 0
    for i in book_no:
        count_book = count_book + 1    

    count_mem = 0
    for i in mem_no:
        count_mem = count_mem + 1

    count_is_book = 0
    for i in issued_no:
        count_is_book = count_is_book + 1

    frame_btn = Frame(summary_window)
    exit_btn = Button(frame_btn,text="EXIT",font="times 13 bold",bg="red4",fg="white",padx=10,command=exit_summary).pack(padx=5,pady=5)
    frame_btn.pack(pady=10,side=BOTTOM)

    Label(summary_window,text = f"Total No of Books : {count_book}",font = "times 20 bold",bg="thistle1",fg="maroon4").pack()
    Label(summary_window,text = f"Total No of Members : {count_mem}",font = "times 20 bold",bg="thistle1",fg="maroon4").pack()
    Label(summary_window,text = f"Total No of Issued Books : {count_is_book}",font = "times 20 bold",bg="thistle1",fg="maroon4").pack()
    
    frame.pack()
    #Close connection
    conn.close()

def exit_summary():
    summary_window.destroy()

###########~~~~~~~~~~~~~~~ Issued books Display Window ~~~~~~~~~~~~~##########
def issued_book_display():
    global display
    display = Tk()
    display.configure(bg="lightblue1")

    display.geometry("1300x700")
    Label(display,text="Issued Books Details",font="times 20 bold",bg="steelblue4",fg="snow",relief=RIDGE,padx=20,pady=10).pack(pady=(20,40))
     #Create a databse or connect to one   
    conn = sqlite3.connect("add_book_table.db")
    #create cursor
    cur = conn.cursor()

    details = cur.execute("SELECT * FROM issuedbooks")
    details = details.fetchall()
    frame = Frame(display,bd=10,relief=RIDGE)
    
    frame_btn = Frame(display)
    exit_btn = Button(frame_btn,text="EXIT",font="times 13 bold",bg="red4",fg="white",padx=10,command=exit_display).pack(padx=5,pady=5)
    frame_btn.pack(pady=10,side=BOTTOM)
    list_box = Listbox(frame,width=100,height=30,font="times 17 bold",bg="lavender",fg="maroon4")
    
    serial_no=1
    for i in details:
        list_box.insert(END,f"{serial_no}: || Book ID: {i[0]} | Book Name: {i[1]} |  Member Id: {i[2]} | Member Name: {i[3]}")
        #Label(frame, ,font="times 17 bold",bg="cadetblue1",fg="maroon4").pack(padx=(0,21),pady=5)
        serial_no = serial_no + 1

    scrollbar = Scrollbar(frame)
    scrollbar.pack(side=RIGHT, fill=Y)
    list_box.pack(pady=20,padx=20)
    
    list_box = Listbox(frame, yscrollcommand = scrollbar.set)
    scrollbar.config(command=list_box.yview)
    
    
    frame.pack()
    #Close connection
    conn.close()
def exit_display():
    display.destroy()

###########~~~~~~~~~~~~~~~ Return Book Window ~~~~~~~~~~~~~##########

def return_book_btn():
    #Create a databse or connect to one   
    conn = sqlite3.connect("add_book_table.db")
    #create cursor
    cur = conn.cursor()

    value = str(re_combo.get())
    id = value.split(",")
    id = id[0].split("-->")
    id = id[0].split(": ")
    id = id[1]
    print(id)
    #delete a record
    try:
        cur.execute(f"DELETE from issuedbooks WHERE book_id = {id}")
        conn.commit()
        cur.execute(f"")

        issue_book = cur.execute(f"SELECT * FROM books WHERE book_id={id}")
        issue_book_info = issue_book.fetchall()
        copy = issue_book_info[0][4]

        cur.execute(f"UPDATE books SET copy_no={copy+1} WHERE book_id={id}")
        conn.commit()

        tmsg.showinfo("Done","Book Successfully Returned",parent=return_book_window)
        return_book_window.destroy()
    except:
        tmsg.showwarning("Warning","Please select a member",parent=return_book_window)

    #Close connection
    conn.close()


def return_book_func():
    global return_book_window
    return_book_window= Tk()
    return_book_window.configure(bg="cyan2")
    #Create a databse or connect to one   
    conn = sqlite3.connect("add_book_table.db")
    #create cursor
    cur = conn.cursor()

    Label(return_book_window,text="Return Book",font="times 20 bold",bg="steelblue4",fg="snow",relief=RIDGE,padx=20,pady=10).pack(pady=(20,40))

    
    issued_book_list = []
    global re_combo

    fr_o =Frame(return_book_window,bd=3,relief=SUNKEN)
    fr1=Frame(fr_o)
    Label(fr1, text='Select Here :',font="times 17 bold",bg="steelblue4",fg="floral white").pack(side=LEFT,padx=(0,21))
    
    list_re = []
    book_name = StringVar()
    books = cur.execute("SELECT * FROM issuedbooks").fetchall()
    for book in books:
        list_re.append(f"Book: {str(book[0])}-->{str(book[1])}, Member: {str(book[2])}-->{book[3]}")

    re_combo = ttk.Combobox(fr1, textvariable=book_name,font="times 15",width = 50)
    re_combo.pack(side=LEFT,padx=(0,21),ipadx=10)

    re_combo['values'] = list_re
    fr1.pack(pady=(30,10))

    fr_o.pack(ipady=15,ipadx=15)

    #Button
    Submit_btn_member = Button(return_book_window,text="Return Book",font="times 15 bold",bg="lime green",command=return_book_btn).pack(pady=(10,5))
    exit_btn_member = Button(return_book_window,text="EXIT",font="times 13 bold",bg="red4",fg="white",padx=10,command=exit_return_window).pack(padx=20,pady=5)

    #commit Changes
    conn.commit()
    #Close connection
    conn.close()

def exit_return_window():
    return_book_window.destroy()


###########~~~~~~~~~~~~~~~ Delete member ~~~~~~~~~~~~~##########
def del_mem():

    conn = sqlite3.connect("add_book_table.db")
    #create cursor
    cur = conn.cursor()

    value = str(txt_member_del.get())
    id = value.split(".")[0]

    #delete a record
    try:
        cur.execute(f"DELETE from members WHERE member_id = {id}")
        txt_member_del.delete(0,END)
        tmsg.showinfo("Done","Member Successfully Deletted",parent=del_mem_win)
        del_mem_win.destroy()
    except:
        tmsg.showwarning("Warning","Please select a member",parent=del_mem_win)
    #commit Changes
    conn.commit()
    #Close connection
    conn.close()

def delete_member_func():
    global del_mem_win
    del_mem_win=Tk()
    del_mem_win.geometry('450x400')
    conn = sqlite3.connect("add_book_table.db")
    #create cursor
    cur = conn.cursor()

    members = cur.execute("SELECT * FROM members").fetchall()
    member_list = []
    for member in members:
        member_list.append(str(member[0])+'.'+member[1])

    Label(del_mem_win,text="Delete Member",font="times 20 bold",bg="steelblue4",fg="snow",relief=RIDGE,padx=20,pady=10).pack(pady=(20,40))

    Label(del_mem_win,text="Select a Member to Delete",font="veredana 15",bg="steelblue",fg="snow",padx=20,pady=10).pack(pady=(20,40))

    global txt_member_del

    fr = Frame(del_mem_win)
    lbl_author = Label(fr, text='Select member:',font="times 17 bold",bg="steelblue4",fg="floral white").pack(side=LEFT,padx=(0,21))
    member_name = StringVar()
    txt_member_del = ttk.Combobox(fr,textvariable=member_name,font="times 15")
    txt_member_del.pack(side=LEFT,padx=(0,21))
    txt_member_del['values'] = member_list
    fr.pack(pady=10)

    Submit_btn_member = Button(del_mem_win,text="Delete",font="times 15 bold",bg="red",fg="white",command=del_mem).pack(pady=(10,5))
    
    #commit Changes
    conn.commit()
    #Close connection
    conn.close()


#########~~~~~~~~~~~Issue Book Window~~~~~~~~~~~#########
def issue():
    conn = sqlite3.connect("add_book_table.db")
    #create cursor
    cur = conn.cursor()

    selected_book_id = int(txt_book_combo.get().split('.')[0])
    selected_book_name = txt_book_combo.get().split('.')[1]
    selected_member_id = int(txt_member_combo.get().split('.')[0])
    selected_member_name = txt_member_combo.get().split('.')[1]
    #print(selected_book,selected_member)
    #check=set(sel_b_1).isdisjoint(set(sel_b_2))
    a=cur.execute("SELECT * FROM issuedbooks")
    b=a.fetchall()
    
    k=0
    list_count_book = []
    for i in b:
        list_count_book.append(b[k][0])
        k = k+1

    k=0
    list_count_mem =[]
    for i in b:
        list_count_mem.append(b[k][2])
        k=k+1

    #print("-------->",selected_book not in list_count_book, selected_book," -- ",selected_member in list_count_mem, selected_member,"--",list_count_book,list_count_mem)

    if selected_book_id in list_count_book and selected_member_id in list_count_mem:
        tmsg.showinfo("ALready Done","You already Issued this Book",parent = issue_book_window)
    #print(list_count)
    else:
        if txt_member_combo.get() != "" and txt_book_combo.get() != "":
            try:
                query = "INSERT INTO issuedbooks(book_id,book_name,member_id,member_name)VALUES(?,?,?,?)"
                cur.execute(query, (selected_book_id,selected_book_name ,selected_member_id, selected_member_name))
                conn.commit()

                issue_book = cur.execute(f"SELECT * FROM books WHERE book_id={selected_book_id}")
                issue_book_info = issue_book.fetchall()
                copy=issue_book_info[0][4]

                cur.execute(f"UPDATE books SET copy_no={copy-1} WHERE book_id={selected_book_id}")
                conn.commit()
                tmsg.showinfo("Success","Book has been issued successfully!",parent=issue_book_window)
                issue_book_window.destroy()
            except:
                tmsg.showerror('Error','Transaction Failed',parent=issue_book_window)
        else:
            tmsg.showwarning('Warning','Please fill all the fields',parent=issue_book_window)
        
    
    conn.close()
    
    # fetch_issue_book_func()

def fetch_issue_book_func():
    # txt_book_combo.delete(0,END)
    
    empty=[]
    txt_book_combo['values'] = empty
    conn = sqlite3.connect("add_book_table.db")
    #create cursor
    cur = conn.cursor()

    books = cur.execute("SELECT * FROM books WHERE copy_no > 0").fetchall()
    
    for book in books:
        avl_book_list.append(str(book[0])+'.'+book[1])
    txt_book_combo['values'] = avl_book_list
    #commit Changes
    conn.commit()
    #Close connection
    conn.close()
    
    

def is_book_func():
    global issue_book_window
    issue_book_window= Tk()
    #Create a databse or connect to one
    issue_book_window.configure(bg="cyan2")
    conn = sqlite3.connect("add_book_table.db")
    #create cursor
    cur = conn.cursor()

    Label(issue_book_window,text="ISSUE BOOK",font="times 20 bold",bg="steelblue4",fg="snow",relief=RIDGE,padx=20,pady=10).pack(pady=(20,40))

    global avl_book_list
    avl_book_list = []
    global txt_book_combo
    global txt_member_combo

    fr_o =Frame(issue_book_window,bd=3,relief=SUNKEN)
    fr1=Frame(fr_o)
    Label(fr1, text='Enter book name:',font="times 17 bold",bg="steelblue4",fg="floral white").pack(side=LEFT,padx=(0,21))
    book_name = StringVar()
    
    
    txt_book_combo = ttk.Combobox(fr1, textvariable=book_name,font="times 15")
    txt_book_combo.pack(side=LEFT,padx=(0,21),ipadx=10)
    fetch_issue_book_func()
    # txt_book_combo['values'] = avl_book_list
    fr1.pack(pady=(30,10))
    
    members = cur.execute("SELECT * FROM members").fetchall()
    member_list = []
    for member in members:
        member_list.append(str(member[0])+'.'+member[1])

    fr2 = Frame(fr_o)
    lbl_author = Label(fr2, text='Select member:',font="times 17 bold",bg="steelblue4",fg="floral white").pack(side=LEFT,padx=(0,21))
    member_name = StringVar()
    txt_member_combo = ttk.Combobox(fr2,textvariable=member_name,font="times 15")
    txt_member_combo.pack(side=LEFT,padx=(0,21))
    txt_member_combo['values'] = member_list
    fr2.pack(pady=10)
    fr_o.pack(ipady=15,ipadx=15)

    #Button
    Submit_btn_member = Button(issue_book_window,text="Issue Book",font="times 15 bold",bg="lime green",command=issue).pack(pady=(10,5))
    exit_btn_member = Button(issue_book_window,text="EXIT",font="times 13 bold",bg="red4",fg="white",padx=10,command=exit_issue_window).pack(padx=20,pady=5)

    #commit Changes
    conn.commit()
    #Close connection
    conn.close()

def exit_issue_window():
    issue_book_window.destroy()


#########~~~~~~~~~~~Delete Button function~~~~~~~~~~#########
def delete_book():
    #Create a databse or connect to one
    conn = sqlite3.connect("add_book_table.db")
    #create cursor
    cur = conn.cursor()
    try:
        y_n = tmsg.askyesno("DELETE","Do you want to delete this book ?")
        if y_n == 1:
            index=Book_listbox.curselection()[0]
            #print(index)
            value = str(Book_listbox.get(ACTIVE))
            id = value.split(".")[0]

            #delete a record
            cur.execute(f"DELETE from books WHERE book_id = {id}")
            Book_info_listbox.delete(0,END)
        elif y_n == 0:
            pass
    except:
        tmsg.showwarning("Warning","Please select a book to delete")

    #commit Changes
    conn.commit()
    #Close connection
    conn.close()
    fetch_book_names()

#########~~~~~~~~~~ ADD NEW MEMBER WINDOW ~~~~~~~~~~#########

def exit_member_window():
    add_member.destroy()

def clear_member_screen():
    member_screen.delete(0,END)
    gender_screen.delete(0,END)
    mobile_screen.delete(0,END)
    member_id_screen.delete(0,END)

def fetch_members_names():
    pass

def member_entry():
    #Create a databse or connect to one
    conn = sqlite3.connect("add_book_table.db")
    #create cursor
    cur = conn.cursor()
    #insert into Table

    if member_screen.get()!="" and gender_screen.get()!="" and mobile_screen.get()!="" and member_id_screen.get!="" :
        try:
            cur.execute("INSERT INTO members VALUES ( :member_id, :member_name, :gender, :mobile_no)",
            {
                "member_id": member_id_screen.get(),
                "member_name": member_screen.get(),
                "gender": gender_screen.get(),
                "mobile_no": mobile_screen.get()
            }
            )

            tmsg.showinfo("DONE", "Member Successfully Added",parent=add_member)
        except:
                if type(member_id_screen.get()) != int:
                    tmsg.showerror("Not Done","Unable to Add Member\nCheck your ID number\nIt is already Registered",parent=add_member)
                    #
    else:
        tmsg.showwarning("Invalid Fields", "Please fill All The Fields" ,parent=add_member)

    

    #commit Changes
    conn.commit()
    #Close connection
    conn.close()
    #Update books list in listbox
    fetch_members_names()
    #clear the screen
    clear_member_screen()

def add_member_func():
    global add_member
    add_member=Tk()
    add_member.geometry("600x550")
    add_member.title("ADD NEW MEMBER")
    add_member.configure(bg="cyan2")
    top_heading=Label(add_member,text="ADD MEMBER",font="times 20 bold",bg="steelblue4",fg="snow",relief=RIDGE,padx=20,pady=10).pack(pady=20)

    global member_screen
    global gender_screen
    global mobile_screen
    global member_id_screen


    middle_frame=Frame(add_member,bd=3,relief=SUNKEN,bg="paleturquoise1")


    label_f4=Frame(middle_frame,bg="steelblue")
    Label(label_f4,text="Member ID",font="times 15 bold",bg="steelblue4",fg="floral white").pack(side=LEFT,padx=(0,21))
    member_id_screen=Entry(label_f4,font="Bahnschrift 20 bold",bg="light cyan",fg="midnight blue")
    member_id_screen.pack(ipadx=10,ipady=5,pady=5,padx=(55,20))
    label_f4.pack(pady=5)


    label_f1=Frame(middle_frame,bg="steelblue")
    Label(label_f1,text="Member Name",font="times 15 bold",bg="steelblue4",fg="floral white").pack(side=LEFT)
    member_screen=Entry(label_f1,font="Bahnschrift 20 bold",bg="light cyan",fg="midnight blue")
    member_screen.pack(ipadx=10,ipady=5,pady=5,padx=(45,25))
    label_f1.pack(pady=5)

    label_f2=Frame(middle_frame,bg="steelblue")
    Label(label_f2,text="Gender",font="times 15 bold",bg="steelblue4",fg="floral white").pack(side=LEFT,padx=(0,73))
    gender_screen=Entry(label_f2,font="Bahnschrift 20 bold",bg="light cyan",fg="midnight blue")
    gender_screen.pack(side=LEFT,ipadx=10,ipady=5,pady=5,padx=30)
    label_f2.pack(pady=5)

    label_f3=Frame(middle_frame,bg="steelblue")
    Label(label_f3,text="Mobile Number",font="times 15 bold",bg="steelblue4",fg="floral white").pack(side=LEFT)
    mobile_screen=Entry(label_f3,font="Bahnschrift 20 bold",bg="light cyan",fg="midnight blue")
    mobile_screen.pack(ipadx=10,ipady=5,pady=5,padx=(40,24))
    label_f3.pack(pady=5)


    #Buttons
    clr_btn_member = Button(middle_frame,text="Clear",font="times 12 bold",bg="orangered2",command=clear_member_screen).pack(padx=20,pady=5)
    Submit_btn_member = Button(middle_frame,text="SUBMIT",font="times 15 bold",bg="lime green",command=member_entry).pack(pady=(10,5))
    exit_btn_member = Button(middle_frame,text="EXIT",font="times 13 bold",bg="red4",fg="white",padx=10,command=exit_member_window).pack(padx=20,pady=5)

    middle_frame.pack(fill=Y,pady=20,ipadx=15,ipady=5)


#########~~~~~~~~~~ ADD NEW BOOK WINDOW ~~~~~~~~~~#########

def clear_books():
    book_id_screen.delete(0,END)
    title_screen.delete(0,END)
    Author_screen.delete(0,END)
    Status_screen.delete(0,END)
    copy_no_screen.delete(0,END)

def register():
    #Create a databse or connect to one
    conn = sqlite3.connect("add_book_table.db")
    #create cursor
    cur = conn.cursor()
    #insert into Table
    if book_id_screen.get()!="" and title_screen.get()!="" and Author_screen.get()!="" and Status_screen.get()!="" and copy_no_screen.get()!="":
        try:
            cur.execute("INSERT INTO books VALUES (:book_id, :title, :Author, :Status, :copy_no)",
            {
                "book_id": book_id_screen.get(),
                "title": title_screen.get(),
                "Author": Author_screen.get(),
                "Status": Status_screen.get(),
                "copy_no": copy_no_screen.get()
            }
            )

            tmsg.showinfo("DONE", "Book Successfully Added",parent=add_book)
        except:
            tmsg.showerror("Not Done","Unable to Add Book\nBook ID is already available",parent=add_book)
    else:
        tmsg.showwarning("Invalid Fields", "Please fill All The Fields" ,parent=add_book)

    #commit Changes
    conn.commit()
    #Close connection
    conn.close()
    #Update books list in listbox
    fetch_book_names()
    #clear the screen
    clear_books()

def add_new_book():
    global add_book
    add_book=Tk()
    add_book.geometry("600x650")
    add_book.title("ADD NEW BOOK")
    add_book.configure(bg="cyan2")
    top_heading=Label(add_book,text="ADD BOOK",font="times 20 bold",bg="steelblue4",fg="snow",relief=RIDGE,padx=20,pady=10).pack(pady=20)

    global book_id_screen
    global title_screen
    global Author_screen
    global Status_screen
    global copy_no_screen

    middle_frame=Frame(add_book,bd=3,relief=SUNKEN,bg="paleturquoise1")
    label_f1=Frame(middle_frame,bg="steelblue")
    Label(label_f1,text="Book ID",font="times 15 bold",bg="steelblue4",fg="floral white").pack(side=LEFT)
    book_id_screen=Entry(label_f1,font="Bahnschrift 20 bold",bg="light cyan",fg="midnight blue")
    book_id_screen.pack(ipadx=10,ipady=5,pady=5,padx=(45,25))
    label_f1.pack(pady=5)

    label_f2=Frame(middle_frame,bg="steelblue")
    Label(label_f2,text="Book Title",font="times 15 bold",bg="steelblue4",fg="floral white").pack(side=LEFT)
    title_screen=Entry(label_f2,font="Bahnschrift 20 bold",bg="light cyan",fg="midnight blue")
    title_screen.pack(ipadx=10,ipady=5,pady=5,padx=25)
    label_f2.pack(pady=5)

    label_f3=Frame(middle_frame,bg="steelblue")
    Label(label_f3,text="Author",font="times 15 bold",bg="steelblue4",fg="floral white").pack(side=LEFT)
    Author_screen=Entry(label_f3,font="Bahnschrift 20 bold",bg="light cyan",fg="midnight blue")
    Author_screen.pack(ipadx=10,ipady=5,pady=5,padx=(50,25))
    label_f3.pack(pady=5)

    label_f4=Frame(middle_frame,bg="steelblue")
    Label(label_f4,text="Status",font="times 15 bold",bg="steelblue4",fg="floral white").pack(side=LEFT)
    Status_screen=Entry(label_f4,font="Bahnschrift 20 bold",bg="light cyan",fg="midnight blue")
    Status_screen.pack(ipadx=10,ipady=5,pady=5,padx=(55,25))
    label_f4.pack(pady=5)

    label_f5=Frame(middle_frame,bg="steelblue")
    Label(label_f5,text="Number of Copy Available",font="times 15 bold",bg="steelblue4",fg="floral white").pack(side=LEFT)
    copy_no_screen=Entry(label_f5,font="Bahnschrift 20 bold",bg="light cyan",fg="midnight blue",width=10)
    copy_no_screen.pack(ipadx=10,ipady=5,pady=5,padx=(40,25))
    label_f5.pack(pady=5)


    #Buttons
    clr_btn = Button(middle_frame,text="Clear",font="times 12 bold",bg="orangered2",command=clear_books).pack(padx=20,pady=5)
    Submit_btn = Button(middle_frame,text="SUBMIT",font="times 15 bold",bg="lime green",command=register).pack(pady=(10,5))

    middle_frame.pack(fill=Y,pady=20,ipadx=15,ipady=5)
    exit_btn_member = Button(middle_frame,text="EXIT",font="times 13 bold",bg="red4",fg="white",padx=10,command=exit_book_window).pack(padx=20,pady=5)


#fetch All book names and show in listbox
def fetch_book_names():
    Book_listbox.delete(0,END)
    #Create a databse or connect to one
    conn = sqlite3.connect("add_book_table.db")
    #create cursor
    cur = conn.cursor()

    cur.execute("SELECT * FROM books")
    
    records=cur.fetchall()
    counter=0
    for record in records:
        Book_listbox.insert(0,f"{record[0]}. {record[1]}")
        counter+=1

    #commit Changes
    conn.commit()
    #Close connection
    conn.close()

def exit_book_window():
    add_book.destroy()

#########~~~~~~~~~~ Update Book Info Window ~~~~~~~~~~#########
def exit_up_book_window():
    update_book.destroy()

def clear_update_window():
    book_id_update_screen.delete(0,END)
    title_update_screen.delete(0,END)
    Author_update_screen.delete(0,END)
    Status_update_screen.delete(0,END)
    copy_no_update_screen.delete(0,END)

def update_save():
    conn = sqlite3.connect("add_book_table.db")  
    #create cursor
    cur = conn.cursor()

    value = str(Book_listbox.get(ANCHOR))
    id = value.split(".")[0]
    #cur.execute("UPDATE books SET (book_id, title, Author, Status, copy_no) VALUES = (book_id_update_screen.get(),title_update_screen.get(),Author_update_screen.get(),Status_update_screen.get(),copy_no_update_screen.get()) WHERE book_id={id}")
    #print(id)
    try:
        update= """UPDATE books SET book_id = ?, title = ?, Author =?,Status=?,copy_no=? where book_id = ?"""
        columnValues = (book_id_update_screen.get(), title_update_screen.get(), Author_update_screen.get(), Status_update_screen.get(), copy_no_update_screen.get(),id)
        cur.execute(update,columnValues)
    except:
        tmsg.showerror("Failed","Unable to Update Info\nBook Id Already available")
    #commit Changes
    conn.commit()
    #Close connection
    conn.close()

    #Fetch all Books name to Book_listbox
    fetch_book_names()
    
    update_book.destroy()
    

def update_book_info():
    global update_book

    #Create a databse or connect to one
    conn = sqlite3.connect("add_book_table.db")
    #create cursor
    cur = conn.cursor()

    global book_id_update_screen
    global title_update_screen
    global Author_update_screen
    global Status_update_screen
    global copy_no_update_screen

    try:
        update_book =Tk()
        update_book.title("Update Book Info")
        update_book.geometry("600x650")

        middle_frame=Frame(update_book,bd=3,relief=SUNKEN,bg="paleturquoise1")
        label_f1=Frame(middle_frame,bg="steelblue")
        Label(label_f1,text="Book ID",font="times 15 bold",bg="steelblue4",fg="floral white").pack(side=LEFT)
        book_id_update_screen=Entry(label_f1,font="Bahnschrift 20 bold",bg="light cyan",fg="midnight blue")
        book_id_update_screen.pack(ipadx=10,ipady=5,pady=5,padx=(45,25))
        label_f1.pack(pady=5)

        label_f2=Frame(middle_frame,bg="steelblue")
        Label(label_f2,text="Book Title",font="times 15 bold",bg="steelblue4",fg="floral white").pack(side=LEFT)
        title_update_screen=Entry(label_f2,font="Bahnschrift 20 bold",bg="light cyan",fg="midnight blue")
        title_update_screen.pack(ipadx=10,ipady=5,pady=5,padx=25)
        label_f2.pack(pady=5)

        label_f3=Frame(middle_frame,bg="steelblue")
        Label(label_f3,text="Author",font="times 15 bold",bg="steelblue4",fg="floral white").pack(side=LEFT)
        Author_update_screen=Entry(label_f3,font="Bahnschrift 20 bold",bg="light cyan",fg="midnight blue")
        Author_update_screen.pack(ipadx=10,ipady=5,pady=5,padx=(50,25))
        label_f3.pack(pady=5)

        label_f4=Frame(middle_frame,bg="steelblue")
        Label(label_f4,text="Status",font="times 15 bold",bg="steelblue4",fg="floral white").pack(side=LEFT)
        Status_update_screen=Entry(label_f4,font="Bahnschrift 20 bold",bg="light cyan",fg="midnight blue")
        Status_update_screen.pack(ipadx=10,ipady=5,pady=5,padx=(55,25))
        label_f4.pack(pady=5)

        label_f5=Frame(middle_frame,bg="steelblue")
        Label(label_f5,text="Number of Copy Available",font="times 15 bold",bg="steelblue4",fg="floral white").pack(side=LEFT)
        copy_no_update_screen=Entry(label_f5,font="Bahnschrift 20 bold",bg="light cyan",fg="midnight blue",width=10)
        copy_no_update_screen.pack(ipadx=10,ipady=5,pady=5,padx=(40,25))
        label_f5.pack(pady=5)

        #Buttons
        clr_btn = Button(middle_frame,text="Clear",font="times 12 bold",bg="orangered2",command=clear_update_window).pack(padx=20,pady=5)
        Submit_btn = Button(middle_frame,text="Update",font="times 15 bold",bg="lime green",command=update_save).pack(pady=(10,5))

        middle_frame.pack(fill=Y,pady=20,ipadx=15,ipady=5)
        exit_btn_member = Button(middle_frame,text="EXIT",font="times 13 bold",bg="red4",fg="white",padx=10,command=exit_up_book_window).pack(padx=20,pady=5)

        index=Book_listbox.curselection()[0]
        value = str(Book_listbox.get(index))
        id = value.split(".")[0]
        book = cur.execute(f"SELECT * FROM books WHERE book_id={id}")
        book_info = book.fetchall()
        book_id_update_screen.insert(0,book_info[0][0])
        title_update_screen.insert(0,book_info[0][1])
        Author_update_screen.insert(0,book_info[0][2])
        copy_no_update_screen.insert(0,book_info[0][4])
        if book_info[0][4] == 0:
            Status_update_screen.insert(0,"Not Available")
        else:
            Status_update_screen.insert(0,"Available")
    except:
        tmsg.showwarning("Warning!","Please select a Book")
        update_book.destroy()

    #commit Changes
    conn.commit()
    #Close connection
    conn.close()


#########~~~~~~~~~~ MAIN WINDOW ~~~~~~~~~~#########
if __name__ == "__main__":

    def search_books():
        """
            For searching book in the Library
        """
            #Create a databse or connect to one
        conn = sqlite3.connect("add_book_table.db")
        #create cursor
        cur = conn.cursor()        

        value = search_entry.get()
        searchquery = cur.execute("SELECT * FROM books WHERE title LIKE ?",('%'+value+'%',)).fetchall()
        Book_listbox.delete(0,END)
        counter = 0
        for book in searchquery:
            Book_listbox.insert(counter, str(book[0])+'.'+str(book[1]))
            counter += 1

        #commit Changes
        conn.commit()
        #Close connection
        conn.close()

    def search_sort():
        #Create a databse or connect to one
        conn = sqlite3.connect("add_book_table.db")
        #create cursor
        cur = conn.cursor()
        query = "SELECT * FROM books ORDER BY title"

        Book_listbox.delete(0,END)
        counter = 0
        searchquery=cur.execute(query).fetchall()
        for book in searchquery:
            Book_listbox.insert(counter, str(book[0])+'.'+str(book[1]))
            counter += 1
        #commit Changes
        conn.commit()
        #Close connection
        conn.close()

    def avl_books():
        #Create a databse or connect to one
        conn = sqlite3.connect("add_book_table.db")
        #create cursor
        cur = conn.cursor()
        query = "SELECT * FROM books WHERE copy_no != 0"

        Book_listbox.delete(0,END)
        counter = 0
        searchquery=cur.execute(query).fetchall()
        for book in searchquery:
            Book_listbox.insert(counter, str(book[0])+'.'+str(book[1]))
            counter += 1
        #commit Changes
        conn.commit()
        #Close connection
        conn.close()

        
    #Outside Frame
    outside_frame = Frame(root,bd = 5,relief = RIDGE)
    #~~~~~~~top Buttons~~~~~~~#
    top_button_frame = Frame(outside_frame,bd=3,relief=SUNKEN,bg="royalblue1")
    Add_member_btn = Button(top_button_frame,text="Add New Member",font="times 14 bold",bg="light cyan",command=add_member_func) #function building on . . . . . .
    Add_Book_btn = Button(top_button_frame,text="Add New Book",font="times 14 bold",bg="light cyan",command=add_new_book)  
    Issue_book_btn = Button(top_button_frame,text="Issue Book",font="times 14 bold",bg="light cyan",command=is_book_func)
    Return_book_btn = Button(top_button_frame,text="Return Book",font="times 14 bold",bg="light cyan",command=return_book_func)
    del_member_btn = Button(top_button_frame,text="Delete Member",font="times 14 bold",bg="light cyan",fg="brown4",command=delete_member_func)
    del_book_btn=Button(top_button_frame,text="Delete Book",font="times 14 bold",bg="light cyan",fg="brown4",command=delete_book)
    summary_btn = Button(top_button_frame,text="Summary",font="times 14 bold",bg="light cyan",command = summary_func)
    #Button Packing
    Add_member_btn.pack(side=LEFT,pady=5,padx=(10,5))
    Add_Book_btn.pack(side=LEFT,pady=5,padx=(10,5))
    Issue_book_btn.pack(side=LEFT,pady=5,padx=(10,10))
    Return_book_btn.pack(side=LEFT,pady=5,padx=(10,10))
    del_member_btn.pack(side=LEFT,pady=5,padx=(10,5))
    del_book_btn.pack(side=LEFT,pady=5,padx=(10,5))
    summary_btn.pack(side=LEFT,pady=5,padx=(10,5))
    top_button_frame.pack(ipadx=2,ipady=2,padx=10,pady=(10,5))
    #----------Top Buttons end ---------------

    #Books Show textbox
    show_area =Frame(outside_frame) # Creating a frame for actual work area

    label_top=Frame(show_area,bg="alice blue")
    book_list_label=Label(label_top,text="BOOKS LIST",font="times 12",bg="palegreen2")
    book_info_label=Label(label_top,text="BOOKS INFO",font="times 12",bg="palegreen2")
    book_list_label.pack(side=LEFT,anchor=NW,padx=100,pady=(0,5))
    book_info_label.pack(side=LEFT,anchor=NW,padx=(135,2))
    label_top.pack(anchor=NW)

    global Book_listbox
    global Book_info_listbox

    Book_listbox = Listbox(show_area,font="times 15",width=28,height=28) #listbox to store books names
    Book_listbox.pack(side=LEFT,padx=15,anchor=NW)
    Button(show_area,text = "Update Info",font="times 13 bold",bg="midnightblue",fg="lightblue1",command=update_book_info).pack(anchor=SW,padx=(120,2),pady=(0,5))
    Book_info_listbox = Listbox(show_area,font="times 15",width=32,height=10) #listbox to show books information
    Book_info_listbox.pack(side=LEFT,padx=15,anchor=NW,pady=(50,0))
    

    #Scroll Bar
    scrollbar = Scrollbar(show_area)
    scrollbar.pack(side=RIGHT, fill=Y)
    Book_listbox.config(yscrollcommand = scrollbar.set) 
    scrollbar.config(command=Book_listbox.yview)

    #Search Box (Right side box)
    search_frame=Frame(show_area,bd=5,relief=RAISED,bg="lightskyblue1")

    #Importing a image
    image = Image.open("library.jpg")
    image = image.resize((1000, 150), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    image_label = Label(search_frame,image=photo)
    image_label.pack(fill=X,pady=(0,5))

    search_entry=Entry(search_frame,font="times 20",bd=5,relief=SUNKEN)
    Label(search_frame,text="Search Book",font="times 16 bold",bg="lightskyblue1").pack(side=LEFT,anchor=NW,padx=(20,5),ipadx=4,pady=25)
    Search_btn = Button(search_frame,text="Search Book",font="times 13 bold",bg="old lace",command=search_books).pack(side=RIGHT,anchor=NE,padx=(8,18),ipadx=8,pady=23)
    search_entry.pack(padx=(20,30),ipadx=4,pady=20)

    #Buttons

    Button(search_frame,text="Sort All Books",font="times 15 bold",padx=10,pady=10,bg="dark slate grey",fg="snow",command=search_sort).pack(pady=5)
    Button(search_frame,text="Available Books",font="times 15 bold",padx=10,pady=10,bg="dark slate grey",fg="snow",command=avl_books).pack(pady=5)
    Button(search_frame,text="Issued Books",font="times 15 bold",padx=10,pady=10,bg="dark slate grey",fg="snow",command=issued_book_display).pack(pady=5)
    
    search_frame.pack(side=RIGHT,fill=BOTH,padx=20)
    show_area.pack(fill=BOTH)
    outside_frame.pack(padx=25,ipadx=15,ipady=15,pady=(40,25),fill=BOTH)
    outside_frame.configure(bg="alice blue")
    show_area.configure(bg="alice blue")

    
    #Fetch all Books name to Book_listbox
    fetch_book_names()

    #fetch all Book info to Book_info_listbox
    def fetch_book_info(event):
        global Book_listbox
        #Create a databse or connect to one
        conn = sqlite3.connect("add_book_table.db")
        #create cursor
        cur = conn.cursor()
        try:
            index=Book_listbox.curselection()[0]
            #print(index)
            value = str(Book_listbox.get(index))
            id = value.split(".")[0]
            
            book = cur.execute(f"SELECT * FROM books WHERE book_id={id}")
            book_info = book.fetchall()
            Book_info_listbox.delete(0,END)
            Book_info_listbox.insert(0, 'Book ID: '+str(book_info[0][0]))
            Book_info_listbox.insert(1, 'Book Name: '+book_info[0][1])
            Book_info_listbox.insert(2, 'Author: '+book_info[0][2])
            Book_info_listbox.insert(3,f"Number of Copies Available: {book_info[0][4]}")
            if book_info[0][4] == 0:
                Book_info_listbox.insert(4,"Status: Not Available")
            else:
                Book_info_listbox.insert(4,"Status: Available")
            # av= str(book_info[0][3]).lower()
            #print(av)
        except:
            pass
        #commit Changes
        conn.commit()
        #Close connection
        conn.close()

    Book_listbox.bind('<<ListboxSelect>>',fetch_book_info)

    root.mainloop()