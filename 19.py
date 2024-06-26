from tkinter import ttk
from tkinter import *
from tkinter.messagebox import showwarning, showinfo
import psycopg2
from psycopg2.extensions import register_type, UNICODE

CONN_STR = "host='10.163.31.228' dbname='rpr' user='eliseev_m_n' password='d705088b'"

FONT = ("Arial", 18)

'''
Основной класс приложения
'''


class tkinterApp(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for page in (
        startPage, page_clients, page_clients_add, page_clients_view, page_update, page_clients_delete):
            frame = page(container, self)

            self.frames[page] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(startPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


'''
Класс, отвечающий за окно с начальным меню
'''


class startPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        label_start = Label(self, text='База данных военных',
                            fg='black', font=("Arial", 40, 'bold'))

        but_1 = ttk.Button(self, text='База данных клиентов', style='normal.TButton',
                           command=lambda: controller.show_frame(page_clients))

        label_start.place(x=145, y=100,
                          width=1000, height=110)
        but_1.place(x=460, y=340,
                    width=370, height=90)

'''
Класс, отвечающий за окно с выбором действия над клинтами в базе
'''


class page_clients(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        # создание кнопок и надписей
        label_start = Label(self, text='База данных военных',
                            fg='black', font=("Arial", 40, 'bold'))

        but_1 = ttk.Button(self, text='Открыть базу данных военных', style='normal.TButton',
                           command=lambda: controller.show_frame(page_clients_view))
        but_2 = ttk.Button(self, text='Добавить военного', style='normal.TButton',
                           command=lambda: controller.show_frame(page_clients_add))
        but_3 = ttk.Button(self, text='Обновить данные о военном', style='normal.TButton',
                           command=lambda: controller.show_frame(page_update))
        but_4 = ttk.Button(self, text='Удалить военного из базы данных', style='normal.TButton',
                           command=lambda: controller.show_frame(page_clients_delete))
        but_back = ttk.Button(self, text="<---", style='normal.TButton',
                              command=lambda: self.controller.show_frame(startPage))

        # размещение кнопок и надписей
        label_start.place(x=145, y=100,
                          width=1000, height=110)
        but_1.place(x=420, y=300,
                    width=450, height=90)
        but_2.place(x=420, y=400,
                    width=450, height=90)
        but_3.place(x=420, y=500,
                    width=450, height=90)
        but_4.place(x=420, y=600,
                    width=450, height=90)
        but_back.place(x=80, y=610,
                       width=200, height=70)


'''
Класс, отвечающий за окно с выводом базы клиентов
'''


class page_clients_view(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.init()

    def init(self):
        label = ttk.Label(self, text="База данных военных", font=('Arial', 23, 'bold'), anchor='center')
        label.grid(row=0, column=0, padx=200, pady=25)

        self.printDB()
        but_menu = ttk.Button(self, text="<---", style='normal.TButton',
                              command=lambda: self.controller.show_frame(page_clients))
        but_menu.grid(row=2, column=0, ipadx=20, ipady=10, padx=50, pady=50)

    def print_clients(self, people):
        register_type(UNICODE)
        conn = psycopg2.connect(CONN_STR)
        cur = conn.cursor()
        cur.execute('select name, rota , rang , stash, nagradi , ychastie_v_voenn_merop , data_b, god_pop_sl from lichn_sostav')
        cols = cur.description
        row = cur.fetchone()
        while row:  # 0 4 7
            st = []
            for i in range(len(cols)):
                st.append(row[i])
            people.append(st)
            row = cur.fetchone()
        cur.close()
        conn.close()
        return people

    '''
    Вывод сохраненных клиентов в виде таблице
    '''

    def printDB(self):
        people = self.print_clients([])
        self.tree = ttk.Treeview(self, columns=['name', 'rota' , 'rang' , 'stash', 'nagradi' , 'ychastie_v_voenn_merop' , 'data_b', 'god_pop_sl'],
                                 height=25, show='headings', style='normal.Treeview')
        self.tree.column('name', width=100, anchor=CENTER)
        self.tree.column('rota', width=100, anchor=CENTER)
        self.tree.column('rang', width=100, anchor=CENTER)
        self.tree.column('stash', width=100, anchor=CENTER)
        self.tree.column('ychastie_v_voenn_merop', width=100, anchor=CENTER)
        self.tree.column('data_b', width=100, anchor=CENTER)
        self.tree.column('god_pop_sl', width=100, anchor=CENTER)
        self.tree.column('nagradi', width=100, anchor=CENTER)
        self.tree.heading('name', text='Имя')
        self.tree.heading('rota', text='Рота')
        self.tree.heading('rang', text='Ранг')
        self.tree.heading('nagradi', text='Награды')
        self.tree.heading('stash', text='Стаж')
        self.tree.heading('ychastie_v_voenn_merop', text='Участие в военных мероприятиях')
        self.tree.heading('data_b', text='Дата рождения')
        self.tree.heading('god_pop_sl', text='Год поступления на службу')
        self.tree.grid(row=1, column=0, padx=222)

        for person in people:
            self.tree.insert('', END, values=person)


'''
Класс, отвечающий за окно с вводом клинтов в базу
'''


class page_clients_add(Frame):

    def __init__(self, parent, controller):

        Frame.__init__(self, parent)
        self.controller = controller
        self.init()

    def init(self):

        labl = ttk.Label(self, text='Добавление военного в базу', font=('Arial', 25, 'bold'))
        labl.grid(row=0, column=0, pady=100, padx=70)

        labl_4 = ttk.Label(self, text='Введите имя служащего', font=FONT)
        labl_4.grid(row=1, column=0, sticky='w', padx=145, pady=10)
        self.ent_4 = ttk.Entry(self, font=FONT)
        self.ent_4.grid(row=2, column=0, sticky='w', ipadx=100, ipady=10, padx=145, pady=10)

        labl_6 = ttk.Label(self, text='Введите роту', font=FONT)
        labl_6.grid(row=3, column=0, sticky='w', padx=145, pady=10)
        self.ent_6 = ttk.Entry(self, font=FONT)
        self.ent_6.grid(row=4, column=0, sticky='w', ipadx=100, ipady=10, padx=145, pady=10)

        labl_8 = ttk.Label(self, text='Введите ранг', font=FONT)
        labl_8.grid(row=5, column=0, sticky='w', padx=145, pady=10)
        self.ent_8 = ttk.Entry(self, font=FONT)
        self.ent_8.grid(row=6, column=0, sticky='w', ipadx=100, ipady=10, padx=145, pady=10)

        labl_10 = ttk.Label(self, text='Введите стаж', font=FONT)
        labl_10.grid(row=1, column=1, sticky='w', pady=10)
        self.ent_10 = ttk.Entry(self, font=FONT)
        self.ent_10.grid(row=2, column=1, sticky='w', ipadx=100, ipady=10, pady=10)

        labl_12 = ttk.Label(self, text='Введите награды', font=FONT)
        labl_12.grid(row=3, column=1, sticky='w', pady=10)
        self.ent_12 = ttk.Entry(self, font=FONT)
        self.ent_12.grid(row=4, column=1, sticky='w', ipadx=100, ipady=10, pady=10)

        labl_14 = ttk.Label(self, text='Введите участия в военных мероприятиях', font=FONT)
        labl_14.grid(row=5, column=1, sticky='w',  pady=10)
        self.ent_14 = ttk.Entry(self, font=FONT)
        self.ent_14.grid(row=6, column=1, sticky='w', ipadx=100, ipady=10, pady=10)



        but_check = ttk.Button(self, text="Добавить", style='normal.TButton', command=self.if_all_write)
        but_check.grid(row=7, column=1, ipadx=140, ipady=20, pady=20)

        but_menu = ttk.Button(self, text="<---", style='normal.TButton',
                              command=lambda: self.controller.show_frame(page_clients))
        but_menu.grid(row=7, column=0, ipadx=20, ipady=10, padx=50)

    def add_clients(self, name,rota,rang,stash,nagradi,ychastie_v_voenn_merop):
        conn = psycopg2.connect(CONN_STR)
        cur = conn.cursor()
        cur.callproc('add_sost', [name,rota,rang,stash,nagradi,ychastie_v_voenn_merop])
        conn.commit()
        cur.close()
        conn.close()

    def if_all_write(self):
        if all([self.ent_4.get() != '',
                self.ent_6.get() != '',
                self.ent_8.get() != '',
                self.ent_10.get() != '',
                self.ent_12.get() != '',
                self.ent_14.get() != '']):
            self.add_clients(self.ent_4.get(), self.ent_6.get(), self.ent_8.get(), self.ent_10.get(), self.ent_12.get(),self.ent_14.get())
            showinfo(title="Информация", message="Успешно! Военный записан в базу данных!")
            self.ent_4.delete(0, END)
            self.ent_4.insert(0, '')
            self.ent_6.delete(0, END)
            self.ent_6.insert(0, '')
            self.ent_8.delete(0, END)
            self.ent_8.insert(0, '')
            self.ent_10.delete(0, END)
            self.ent_10.insert(0, '')
            self.ent_12.delete(0, END)
            self.ent_12.insert(0, '')
        else:
            showwarning(title="Информация", message="Не все поля заполнены!")


'''
Класс, отвечающий за окно с добавлением военного в базу
'''


class page_update(Frame):

    def __init__(self, parent, controller):

        Frame.__init__(self, parent)
        self.controller = controller
        self.init()

    def init(self):
        labl = ttk.Label(self, text='Обновление военного в базе данных', font=('Arial', 25, 'bold'))
        labl.grid(row=0, column=0, pady=40, padx=100)

        labl_4 = ttk.Label(self, text='Введите имя', font=FONT)
        labl_4.grid(row=1, column=0, sticky='w', padx=145, pady=20)
        self.ent_4 = ttk.Entry(self, font=FONT)
        self.ent_4.grid(row=2, column=0, sticky='w', ipadx=100, ipady=10, padx=145, pady=15)

        labl_5 = ttk.Label(self, text='Введите новую роту', font=FONT)
        labl_5.grid(row=3, column=0, sticky='w', padx=145)
        self.ent_5 = ttk.Entry(self, font=FONT)
        self.ent_5.grid(row=4, column=0, sticky='w', ipadx=100, ipady=10, padx=145, pady=15)

        labl_6 = ttk.Label(self, text='Введите новый ранг', font=FONT)
        labl_6.grid(row=5, column=0, sticky='w', padx=145)
        self.ent_6 = ttk.Entry(self, font=FONT)
        self.ent_6.grid(row=6, column=0, sticky='w', ipadx=100, ipady=10, padx=145, pady=15)

        labl_7 = ttk.Label(self, text='Введите новые стаж', font=FONT)
        labl_7.grid(row=7, column=0, sticky='w', padx=145)
        self.ent_7 = ttk.Entry(self, font=FONT)
        self.ent_7.grid(row=8, column=0, sticky='w', ipadx=100, ipady=10, padx=145, pady=15)

        labl_8 = ttk.Label(self, text='Введите новый награды', font=FONT)
        labl_8.grid(row=1, column=1, sticky='w')
        self.ent_8 = ttk.Entry(self, font=FONT)
        self.ent_8.grid(row=2, column=1, sticky='w', ipadx=100, ipady=10,  pady=15)

        labl_9 = ttk.Label(self, text='Введите новый участия в мероприятиях', font=FONT)
        labl_9.grid(row=3, column=1, sticky='w')
        self.ent_9 = ttk.Entry(self, font=FONT)
        self.ent_9.grid(row=4, column=1, sticky='w', ipadx=100, ipady=10, pady=15)

        labl_10 = ttk.Label(self, text='Введите новую дату рождения', font=FONT)
        labl_10.grid(row=5, column=1, sticky='w')
        self.ent_10 = ttk.Entry(self, font=FONT)
        self.ent_10.grid(row=6, column=1, sticky='w', ipadx=100, ipady=10, pady=15)

        labl_11 = ttk.Label(self, text='Введите новый год поступления на службу', font=FONT)
        labl_11.grid(row=7, column=1, sticky='w')
        self.ent_11 = ttk.Entry(self, font=FONT)
        self.ent_11.grid(row=8, column=1, sticky='w', ipadx=100, ipady=10, pady=15)

        but_check = ttk.Button(self, text="Обновить", style='normal.TButton', command=self.if_all_write)
        but_check.grid(row=9, column=1, ipadx=140, ipady=20, pady=10)

        but_menu = ttk.Button(self, text="<---", style='normal.TButton',
                              command=lambda: self.controller.show_frame(page_clients))
        but_menu.grid(row=9, column=0, ipadx=20, ipady=10, padx=50, pady=70)

    def change_city(self, name,rota,rang,stash,nagradi,ychastie_v_voenn_merop,data_b, god_pop_sl):
        conn = psycopg2.connect(CONN_STR)
        cur = conn.cursor()
        cur.callproc('update', [name,rota,rang,stash,nagradi,ychastie_v_voenn_merop,data_b, god_pop_sl])
        conn.commit()
        cur.close()
        conn.close()

    def if_all_write(self):
        if all([self.ent_4.get() != '',
                self.ent_5.get() != '',
                self.ent_6.get() != '',
                self.ent_7.get() != '',
                self.ent_8.get() != '',
                self.ent_9.get() != '',
                self.ent_10.get() != '',
                self.ent_11.get() != '']):
            self.change_city(self.ent_4.get(), self.ent_5.get(),self.ent_6.get(),self.ent_7.get(),self.ent_8.get(),self.ent_9.get(),self.ent_10.get(),self.ent_11.get())
            showinfo(title="Информация", message="Успешно! Информация обновлена!")
            self.ent_4.delete(0, END)
            self.ent_4.insert(0, '')
            self.ent_5.delete(0, END)
            self.ent_5.insert(0, '')
            self.ent_6.delete(0, END)
            self.ent_6.insert(0, '')
            self.ent_7.delete(0, END)
            self.ent_7.insert(0, '')
            self.ent_8.delete(0, END)
            self.ent_8.insert(0, '')
            self.ent_9.delete(0, END)
            self.ent_9.insert(0, '')
            self.ent_10.delete(0, END)
            self.ent_10.insert(0, '')
            self.ent_11.delete(0, END)
            self.ent_11.insert(0, '')
        else:
            showwarning(title="Информация", message="Не все поля заполнены!")


'''
Класс, отвечающий за окно с удалением клиентов из базу
'''


class page_clients_delete(Frame):

    def __init__(self, parent, controller):

        Frame.__init__(self, parent)
        self.controller = controller
        self.init()

    def init(self):
        labl = ttk.Label(self, text='Удаление военного из базы', font=('Arial', 25, 'bold'))
        labl.grid(row=0, column=1, pady=150, padx=100)

        labl_4 = ttk.Label(self, text='Введите id военного', font=FONT)
        labl_4.grid(row=1, column=1, sticky='w', padx=125)
        self.ent_4 = ttk.Entry(self, font=FONT)
        self.ent_4.grid(row=2, column=1, sticky='w', ipadx=100, ipady=10, padx=125, pady=20)

        but_check = ttk.Button(self, text="Удалить", style='normal.TButton', command=self.if_all_write)
        but_check.grid(row=5, column=1, ipadx=140, ipady=20, pady=10)

        but_menu = ttk.Button(self, text="<---", style='normal.TButton',
                              command=lambda: self.controller.show_frame(page_clients))
        but_menu.grid(row=6, column=0, ipadx=20, ipady=10, padx=50, pady=70)

    def delete_client(self, id_sos):
        conn = psycopg2.connect(CONN_STR)
        cur = conn.cursor()
        cur.callproc('delete_sost', [id_sos])
        conn.commit()
        cur.close()
        conn.close()

    def if_all_write(self):
        if self.ent_4.get() != '':
            self.delete_client(self.ent_4.get())
            showinfo(title="Информация", message="Успешно! Военный удален из базы данных!")
            self.ent_4.delete(0, END)
            self.ent_4.insert(0, '')
        else:
            showwarning(title="Информация", message="Не все поля заполнены!")


app = tkinterApp()
app.title("База данных туров пансионата")
app.geometry('1300x800+300+100')
app.resizable(False, False)
style = ttk.Style()
style.configure('normal.Treeview', font = ('Arial', 12))
style.configure('normal.TButton', font = ('Arial', 20))
app.mainloop()