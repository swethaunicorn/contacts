from tkinter import *
from tkinter import ttk
import sqlite3

class Contacts():
    db_filename = 'contacts.db'
    def __init__(self,root):
        self.root = root
        self.creat_gui()

        ttk.style = ttk.Style()
        ttk.style.configure("Treeview", font=('helvetica', 10))
        ttk.style.configure("Treeview.Heading", font=('helvetica', 12, 'bold'))

    def execute_db_query(self, query, parameters=()):
        with sqlite3.connect(self.db_filename) as conn:
            print(conn)
            print("You have been Successfully connected with database")
            cursor = conn.cursor()
            query_result = cursor.execute(query, parameters)
            conn.commit()
        return query_result


    def creat_gui(self):
        self.creat_left_icone()
        self.creat_label_frame()
        self.create_message_area()
        self.create_tree_view()
        self.create_scroll_bar()
        self.creat_button()
        self.view_records()


    def creat_left_icone(self):
        photo = PhotoImage('Home\Download\logo.png')
        lable = Label(image=photo)
        lable.image = photo
        lable.grid(row=0, column=0)

    def creat_label_frame(self):
        lablefream = LabelFrame(self.root, text='Creat New Contects', bg='sky blue', font='helvetica 10')
        lablefream.grid(row=0,column=1, padx=8, pady=8, sticky='ew')
        Label(lablefream, text='Name', bg='black', fg='white').grid(row=1, column=1, sticky=W, padx=15, pady=2)
        self.namelable = Entry(lablefream)
        self.namelable.grid(row=1, column=2, sticky=W, padx=5, pady=2)
        Label(lablefream, text='Email', bg='green', fg='white').grid(row=2, column=1, sticky=W, padx=15, pady=2)
        self.emaillable = Entry(lablefream)
        self.emaillable.grid(row=2, column=2, sticky=W, padx=5, pady=2)
        Label(lablefream, text='Number', bg='brown', fg='white').grid(row=3, column=1, sticky=W, padx=15, pady=2)
        self.numlable = Entry(lablefream)
        self.numlable.grid(row=3, column=2, sticky=W, padx=5, pady=2)
        Button(lablefream, text='Add Contacts', command=self.on_add_contact_button_clicked, bg='black', fg='white').grid(row=4, column=2, sticky=E, padx=5, pady=2)

    def create_message_area(self):
        self.mess = Label(self.root, text='', fg='red')
        self.mess.grid(row=3, column=1, sticky=W)

    def create_tree_view(self):
        self.tree = ttk.Treeview(height=10, columns=("email","numbers"))
        self.tree.grid(row=6, column=0, columnspan=3)
        self.tree.heading('#0', text='Names', anchor=W)
        self.tree.heading("email", text='Email Address', anchor=W)
        self.tree.heading("numbers", text='Contact Number', anchor=W)

    def create_scroll_bar(self):
        self.scorllbar = Scrollbar(orient='vertical', command=self.tree.yview)
        self.scorllbar.grid(row=6, column=3, rowspan=10, sticky=W)

    def creat_button(self):
        Button(text='Delect selected', command=self.on_delete_selected_button_clicked, bg='red', fg='white').grid(row=9, column=0, padx=10, pady=20, sticky=W)
        Button(text='Modify selected', command='', bg='purple', fg='white').grid(row=9, column=1, padx=10, pady=20, sticky=W)
        Button(text='Exit', command=self.root.quit, bg='blue', fg='white', font='helvetica 10').grid(row=9, column=2, padx=10, pady=20, sticky=W)

    def on_add_contact_button_clicked(self):
        self.add_new_contacts()

    def on_delete_selected_button_clicked(self):
        self.mess['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.mess['text'] = 'No item selected to delete'
            return
        self.delete_contacts()

    def add_new_contacts(self):
        if self.new_contacts_validation():
            query = 'INSERT INTO contacts_list VALUES(NULL,?,?,?)'
            parameters = (self.namelable.get(),self.emaillable.get(),self.numlable.get())
            self.execute_db_query(query, parameters)
            self.mess['text'] = 'New Contact {} is added'.format(self.namelable.get())
            self.namelable.delete(0,END)
            self.emaillable.delete(0, END)
            self.numlable.delete(0, END)
        else:
            self.mess['text'] = 'name, email, number black should not by empty'
        self.view_records()

    def new_contacts_validation(self):
        return self.namelable.get() != 0 and self.emaillable.get() != 0 and self.numlable.get() != 0

    def view_records(self):
        items = self.tree.get_children()
        for item in items:
            self.tree.delete(item)
        query = 'SELECT * FROM contacts_list ORDER BY name DESC'
        contact_entries = self.execute_db_query(query)
        for row in contact_entries:
            self.tree.insert('', 0, text=row[1], values=(row[2],row[3]))

    def delete_contacts(self):
        self.mess['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM contacts_list WHERE name = ?'
        self.execute_db_query(query,(name,))
        self.mess['text'] = 'Contact for {} deleted'.format(name)


if __name__ == '__main__':
    root = Tk()
    root.title('My Contacts')
    application = Contacts(root)
    root.mainloop()
