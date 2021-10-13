#INTELLIGENT GRADING ORIENTED REGISTER

from tkinter import *
import backend
import os
from datetime import date
import pandas as pd
import xlsxwriter

if os.path.isdir("Elevi") == False:
    os.mkdir("Elevi")

if os.path.isdir("Note") == False:
    os.mkdir("Note")

def get_selected_row(event):
    try:
        global selected_tuple
        index = list1.curselection()[0] #user da click pe linia dorita si se salveaza indexul liniei (0-END)
        selected_tuple = list1.get(index) #se salveaza linia cu datele selectate de user
        #cand dam click pe linie, se completeaza in entry cu datele corespunzatoare
        e1.delete(0,END)
        e1.insert(END,selected_tuple[1])
        e2.delete(0,END)
        e2.insert(END,selected_tuple[2])
        e3.delete(0,END)
        e3.insert(END,selected_tuple[3])
        e4.delete(0,END)
        e4.insert(END,selected_tuple[4])
    except IndexError:
        pass

#vizualizare elevi in lista
def view_command():
    list1.delete(0, END) #Sa nu se repete de fiecare data cand apasam view all
    for row in backend.view():
        list1.insert(END, row)

#cautare elev
def search_command():
    list1.delete(0, END)
    for row in backend.search(nume_text.get(), prenume_text.get(), adresa_text.get(), cnp_text.get()):
        list1.insert(END, row)

#adaugare elev in bd
def add_command():
    backend.insert(nume_text.get(), prenume_text.get(), adresa_text.get(), cnp_text.get())
    list1.delete(0,END)
    list1.insert(END,nume_text.get(), prenume_text.get(), adresa_text.get(), cnp_text.get())
    backend.creare_tabel_nota(nume_text.get(), prenume_text.get())
    url = "Note/" + prenume_text.get() + " " + nume_text.get() + ".xlsx"

    dataExcel = pd.ExcelWriter(url, engine='xlsxwriter')
    view_command()

#stergere elev din bd cu tot cu tabela de note
def delete_command():
    
    path = "Elevi/" + selected_tuple[2] + " " + selected_tuple[1] + ".db"
    #print("Note/" + selected_tuple[2] + " " + selected_tuple[1] + ".xlsx")
    os.remove(path)
    
    pathExcel = "Note/" + selected_tuple[2] + " " + selected_tuple[1] + ".xlsx"
    os.remove(pathExcel)

    backend.delete(selected_tuple[0])
    view_command()

#modificare date elev
def update_command():
    oldpath = path = "Elevi/" + selected_tuple[2] + " " + selected_tuple[1] + ".db"
    newpath = path = "Elevi/" + prenume_text.get() + " " + nume_text.get() + ".db"
    os.rename(oldpath, newpath)

    backend.update(selected_tuple[0], nume_text.get(), prenume_text.get(), adresa_text.get(), cnp_text.get())

    if os.path.isdir("Note/" + selected_tuple[2] + " " + selected_tuple[1] + ".xlsx") == False:
        oldpathExcel = "Note/" + selected_tuple[2] + " " + selected_tuple[1] + ".xlsx"
        newpathExcel = "Note/" + prenume_text.get() + " " + nume_text.get() + ".xlsx"
        os.rename(oldpathExcel, newpathExcel)

    view_command()
#face ecranul pentru aduagare notei in catalog
def adauga_nota():

    #adauga nota in sine
    def add_note():
        # backend.sterge_capsule(selected_tuple[1], selected_tuple[2])
        today = date.today()
        d = today.strftime("%Y-%m-%d")
        backend.insert_nota(selected_tuple[1], selected_tuple[2], d, nota_mate.get(), nota_romana.get(), nota_info.get(), nota_fizica.get())

    nota = Toplevel()
    nota.title('Catalog')
    l1 = Label(nota, text = "Matematica")
    l1.grid(row = 0, column = 0)

    l2 = Label(nota, text = "Romana")
    l2.grid(row=1, column = 0)

    l3 = Label(nota, text = "Informatica")
    l3.grid(row=2, column = 0)

    l4 = Label(nota, text = "Fizica")
    l4.grid(row=3, column = 0)

    nota_mate = StringVar()
    e1 = Entry(nota, textvariable = nota_mate)
    e1.grid(row = 0, column = 1)

    nota_romana = StringVar()
    e2 = Entry(nota, textvariable = nota_romana)
    e2.grid(row = 1, column = 1)

    nota_info = StringVar()
    e3 = Entry(nota, textvariable = nota_info)
    e3.grid(row = 2, column = 1)

    nota_fizica = StringVar()
    e4 = Entry(nota, textvariable = nota_fizica)
    e4.grid(row=3, column = 1)

    b1 = Button(nota, text = "Adauga", width = 10, command = add_note)
    b1.grid(row=4, column=0)

def vezi_nota():
    returned_rows = backend.generare_nota_mate(selected_tuple[1], selected_tuple[2])
    note_mate = [i[0] for i in returned_rows]
    
    returned_rows = backend.generare_nota_romana(selected_tuple[1], selected_tuple[2])
    note_romana = [i[0] for i in returned_rows]

    returned_rows = backend.generare_nota_info(selected_tuple[1], selected_tuple[2])
    note_info = [i[0] for i in returned_rows]

    returned_rows = backend.generare_nota_fizica(selected_tuple[1], selected_tuple[2])
    note_fizica = [i[0] for i in returned_rows]

    note ={"Matematica":note_mate, "Romana":note_romana, "Informatica": note_info, "Fizica": note_fizica}
    data = pd.DataFrame.from_dict(note, orient='index')
    data = data.transpose()
    
    url = "Note/" + selected_tuple[2] + " " + selected_tuple[1] + ".xlsx"

    dataExcel = pd.ExcelWriter(url, engine='xlsxwriter')
    data.to_excel(dataExcel, sheet_name='Sheet1')
    dataExcel.save()

window = Tk()
window.title("Catalog Virtual")
window.geometry("505x150")
window.resizable(0, 0)
l1 = Label(window, text = "Nume")
l1.grid(row=0, column=0)

l2 = Label(window, text = "Prenume")
l2.grid(row=0, column=2)

l3 = Label(window, text = "Adresa")
l3.grid(row=1, column=0)

l4 = Label(window, text = "CNP")
l4.grid(row=1, column=2)

nume_text = StringVar()
e1 = Entry(window, textvariable = nume_text)
e1.grid(row=0, column=1)

prenume_text = StringVar()
e2 = Entry(window, textvariable = prenume_text)
e2.grid(row=0, column=3)

adresa_text = StringVar()
e3 = Entry(window, textvariable = adresa_text)
e3.grid(row=1, column=1)

cnp_text = StringVar()
e4 = Entry(window, textvariable = cnp_text)
e4.grid(row=1, column=3)

list1 = Listbox(window, height = 6, width=35)
list1.grid(row=2, column=0,rowspan=8, columnspan=2)

sb1 = Scrollbar(window)
sb1.grid(row=2, column=2, rowspan=7)

list1.bind('<<ListboxSelect>>', get_selected_row)

b1 = Button(window, text = "Vezi tot", width = 12, command = view_command)
b1.grid(row=2, column =3)

b2 = Button(window, text = "Cautare", width = 12, command=search_command)
b2.grid(row=3, column =3)

b3 = Button(window, text = "Adaugare elev", width = 12, command=add_command)
b3.grid(row=4, column =3)

b4 = Button(window, text = "Actualizare elev", width = 12, command = update_command)
b4.grid(row=5, column =3)

b5 = Button(window, text = "Sterge selectia", width = 12, command=delete_command)
b5.grid(row=2, column =4)

b6 = Button(window, text = "Inchide", width = 12, command = window.destroy)
b6.grid(row=5, column =4)

b7 = Button(window, text = "Adauga Nota", width = 12, command = adauga_nota)
b7.grid(row = 4, column=4)

b8 = Button(window, text = "Vezi Note Elev", width = 12, command = vezi_nota)
b8.grid(row=3, column = 4)

list1.configure(yscrollcommand=sb1.set)
sb1.configure(command=list1.yview)

window.mainloop()