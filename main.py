from tkinter import messagebox, filedialog
from tkinter import *
import sqlite3

with sqlite3.connect('AmDB.db') as con:
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS people (name TEXT, photo BLOB, bio TEXT)")

def change_in_db(new_name, directory, bio, old_name):
    try:
        with open(directory, 'rb') as photo:
            image = photo.read()
            data = (new_name, image, bio, old_name)
            with sqlite3.connect('AmDB.db') as con: 
                con.execute("""UPDATE people SET name = ?, photo = ?, bio = ? WHERE name = ?""", data)
    except Exception as e:
        print(f"Error saving image: {e}")
        messagebox.showerror("Ошибка", "Не удалось сохранить изображение")

def input_in_db(name, directory, bio):
    try:
        with open(directory, 'rb') as photo:
            image = photo.read()
            data = (name, image, bio)
            with sqlite3.connect('AmDB.db') as con: 
                con.execute("""INSERT INTO people (name, photo, bio) VALUES (?, ?, ?)""", data)
    except Exception as e:
        print(f"Error saving image: {e}")
        messagebox.showerror("Ошибка", "Не удалось сохранить изображение")

def get_db():
    list_name, list_photo, list_bio = [], [], []
    with sqlite3.connect('AmDB.db') as con: 
        data = con.execute("SELECT name FROM people")
        for row in data: 
            list_name.append(row)
        
        data = con.execute("SELECT photo FROM people")
        for row in data:
            try:
                if row[0] is None:
                    print("Warning: Empty image data in database")
                    empty_image = PhotoImage()
                    list_photo.append(empty_image)
                    continue
                    
                # Create PhotoImage from BLOB data
                photo = PhotoImage(data=row[0])
                list_photo.append(photo)
            except Exception as e:
                print(f"Error loading image: {e}")
                print(f"Image data length: {len(row[0]) if row[0] else 0}")
                # Create empty image if loading fails
                empty_image = PhotoImage()
                list_photo.append(empty_image)
        
        data = con.execute("SELECT bio FROM people")
        for row in data: 
            list_bio.append(row)
    
    return list_name, list_photo, list_bio

def editing(name, x, y, name_title, resb):
    name.title(f"{name_title}")
    name.geometry(f"{x}x{y}")
    name.resizable(resb, resb)
    name.geometry("+%d+%d" % ((root.winfo_screenwidth()/2) - (x/2), (root.winfo_screenheight()/2) - (y/2)))
    name.focus_set()
    name.grab_set()

root = Tk()
editing(root, 1200, 650, "Знаменитые композиторы России", FALSE)

def tWid(list_bio, index):
    textWidget = Text(root, width=49, height=39)
    textWidget.place(x=845, y=0)
    if list_bio != 0: 
        textWidget.insert(END, f"{list_bio[index][0]}")
    textWidget.config(state=DISABLED)

tWid(0, 0)
listbox = Listbox(root, selectmode=SINGLE, width=39, height=39)
listbox.place(x=0, y=0)

def closing(event = NONE): 
    root.quit()

def content():
    content = Toplevel(root)
    editing(content, 330, 140, "Содержание", FALSE) 
    txt=f'''База данных Знаменитые композиторы России
Позволяет: добавлять/изменять/удалять информацию.
Клавиши программы:
F1 - Вызов справки по программе,
F2 - Добавить в базу данных,
F3 - Удалить из базы данных,
F4 - Изменить запись в базе данных,
Ctrl + X - Выход из программы.'''
    Label(content,text=txt,justify=LEFT).place(x=0,y=0)
    Button(content,text="Выход",anchor=NW,command=content.destroy).place(x=280,y=110)

def about_program(event = NONE):
    messagebox.showinfo("О программе", f"""База данных Знаменитые композиторы России
(c) Иванов Иван Иванович, Россия, 2023""")

def bar():
    menubar = Menu(root)
    root.config(menu = menubar)
    
    fondmenu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Фонд", menu=fondmenu)
    fondmenu.add_command(label="Найти...", accelerator="Ctrl + F", command=find)
    fondmenu.add_separator()
    fondmenu.add_command(label="Добавить", accelerator="F2", command=adding)
    fondmenu.add_command(label="Удалить", accelerator="F3", command=d3l3t3)
    fondmenu.add_command(label="Изменить", accelerator="F4", command=edit)
    fondmenu.add_separator()
    fondmenu.add_command(label="Выход", accelerator="Ctrl + X", command=closing)
    
    referencemenu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Справка", menu=referencemenu)
    referencemenu.add_command(label="Содержание", command=content)
    referencemenu.add_separator()
    referencemenu.add_command(label="О программе", accelerator='F1', command=about_program)
    
    Label(text = "      F1 - Справка      |     F2 - Добавить      |     F3 - Удалить      |     F4 - Изменить      |     Ctrl + X - Выход", 
          bd=1, relief=SUNKEN, anchor=W, bg="#9797FF").pack(side = BOTTOM, fill = X)
    
    sp_binds = {'F1': about_program, 'Control-x': closing, 'F4': edit, 'F3': d3l3t3, 'F2': adding, '<Control-f>': find}
    for x, v in sp_binds.items():
        root.bind(f'<{x}>', v)

def find(event = NONE):
    find = Toplevel(bg="#9797FF")
    editing(find, 300, 80, "Поиск", FALSE)
    
    Label(find, text="Введите имя", background="#9797FF").pack(anchor=N)
    entryName = Entry(find, relief=SUNKEN, bd=2)
    entryName.pack(anchor=NW, fill=X, padx=5)
    
    def confirm():
        if len(entryName.get()) > 0:
            for i in range(listbox.size()):
                if entryName.get() == listbox.get(i):
                    find.destroy()
                    listbox.select_clear(0, listbox.size())
                    listbox.select_set(i)
                    Button(root, image=PhotoImage(), height=625, width=600).place(x=240)
                    tWid(0, 0)
                    return
            messagebox.showinfo('Внимание', 'Ничего не найдено. Введите снова')
    
    Button(find, text="Ок", command=confirm).place(x=167, y=50)
    Button(find, text="Отмена", command=find.destroy).place(x=107, y=50)

def edit(event = NONE):
    list_name, list_photo, list_bio = get_db()
    if not(listbox.curselection()): 
        messagebox.showinfo("Уведомление", "Выберите элемент")
        return
    else: 
        index = listbox.curselection()[0]
    
    edit = Toplevel(root, bg="#9797FF")
    editing(edit, 300, 320, "Изменение", FALSE)
    
    Label(edit,text="Введите имя",background="#9797FF").pack(anchor=N)
    entryName = Entry(edit, relief=SUNKEN, bd=2)
    entryName.pack(anchor=NW,fill=X, padx=5)
    
    Label(edit, text="Введите описание", background="#9797FF").pack(anchor=N)
    textBio = Text(edit, relief=SUNKEN, bd=2, height=7)
    textBio.pack(anchor=NW, fill=X, padx=5)
    
    Label(edit, text="Выберите картинку", background="#9797FF").pack(anchor=N)
    def select_file():
        filePath = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
        fileEntry.delete(0, END)
        fileEntry.insert(0, filePath)
    
    fileEntry = Entry(edit, relief=SUNKEN, bd=2)
    fileEntry.pack(anchor=NW,fill=X, padx=5)
    
    entryName.insert(0, f"{list_name[index][0]}")
    textBio.insert(END, f"{list_bio[index][0]}")
    Button(edit, text="Выбрать файл", command=select_file).place(x=7, y=230)
    
    def confirm():
        for i in range(listbox.size()):
            if entryName.get() == listbox.get(i): 
                messagebox.showwarning("Предупреждение", "Такое имя уже есть")
                return
        
        if len(entryName.get()) == 0 or len(textBio.get("1.0", "end-1c")) == 0 or len(fileEntry.get()) == 0: 
            messagebox.showwarning("Предупреждение", "Отсутствует имя, описание или путь до фотографии")
            return
        else:
            result = messagebox.askquestion("Уведомление", "Вы уверены?")
            if result == "yes":
                tWid(0, 0)
                Button(root, image=PhotoImage(), height=625, width=600).place(x=240)
                change_in_db(entryName.get(), fileEntry.get(), textBio.get("1.0", "end-1c"), list_name[index][0])
                output_name()
                edit.destroy()
    
    Button(edit, text="Ок", command=confirm).place(x=7, y=285)
    Button(edit, text="Отмена", command=edit.destroy).place(x=35, y=285)

def adding(event=NONE):
    adding = Toplevel(root, bg="#9797FF")
    editing(adding, 300, 320, "Добавление", FALSE)
    
    Label(adding,text="Введите имя",background="#9797FF").pack(anchor=N)
    entryName = Entry(adding, relief=SUNKEN, bd=2)
    entryName.pack(anchor=NW,fill=X, padx=5)
    
    Label(adding, text="Введите описание", background="#9797FF").pack(anchor=N)
    textBio = Text(adding, relief=SUNKEN, bd=2, height=7)
    textBio.pack(anchor=NW, fill=X, padx=5)
    
    Label(adding, text="Выберите картинку", background="#9797FF").pack(anchor=N)
    fileEntry = Entry(adding, relief=SUNKEN, bd=2)
    fileEntry.pack(anchor=NW,fill=X, padx=5)
    
    def select_file():
        filePath = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
        fileEntry.delete(0, END)
        fileEntry.insert(0, filePath)
    
    Button(adding, text="Выбрать файл", command=select_file).place(x=7, y=230)
    
    def confirm():
        for i in range(listbox.size()):
            if entryName.get() == listbox.get(i): 
                messagebox.showwarning("Предупреждение", "Такое имя уже есть")
                return
                
        if len(entryName.get()) == 0 or len(textBio.get("1.0", "end-1c")) == 0 or len(fileEntry.get()) == 0: 
            messagebox.showwarning("Предупреждение", "Отсутствует имя, описание или путь до фотографии")
            return
        else:
            result = messagebox.askquestion("Уведомление", "Вы уверены?")
            if result == "yes":
                tWid(0, 0)
                Button(root, image=PhotoImage(), height=625, width=600).place(x=240)
                input_in_db(entryName.get(), fileEntry.get(), textBio.get("1.0", "end-1c"))
                output_name()
                adding.destroy()
    
    Button(adding, text="Ок", command=confirm).place(x=7, y=285)
    Button(adding, text="Отмена", command=adding.destroy).place(x=35, y=285)

def d3l3t3(event=NONE):
    list_name, list_photo, list_bio = get_db()
    d3l3t3 = Toplevel(bg="#9797FF")
    editing(d3l3t3, 300, 500, "Удаление", FALSE)
    
    listd3l3t3 = Listbox(d3l3t3, selectmode=SINGLE, height=26)
    listd3l3t3.pack(fill=X, padx=5, pady=5)
    
    for i in list_name:
        listd3l3t3.insert(END, f"{i[0]}")
    
    def delete():
        with sqlite3.connect('AmDB.db') as con:
            cur, index = con.cursor(), listd3l3t3.curselection()[0]
            value = listd3l3t3.get(index)
            cur.execute(f"DELETE FROM people WHERE name='{value}'")
        d3l3t3.destroy()
        output_name()
        tWid(0, 0)
        Button(root, image=PhotoImage(), height=625, width=600).place(x=240)
    
    Button(d3l3t3,text="ОК", command=delete).place(x=170, y=470)
    Button(d3l3t3,text="Отмена", command=d3l3t3.destroy).place(x=110, y=470)

def output_again(event):
    list_name, list_photo, list_bio = get_db()
    w = event.widget
    
    if w.curselection(): 
        index = int(w.curselection()[0])
    else: 
        return
    
    img = list_photo[index]
    qqq = Button(root, image=img, height=625, width=600, bd=1)
    qqq.image = img
    qqq.place(x=240)
    tWid(list_bio, index)

def output_name():
    list_name, list_photo, list_bio = get_db()
    listbox.delete(0, END)
    for i in list_name: 
        listbox.insert(END, f"{i}")

bar()
output_name()
listbox.bind('<<ListboxSelect>>', output_again)
root.mainloop()