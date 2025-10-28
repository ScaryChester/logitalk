from customtkinter import *
from socket import *

class MainWindow(CTk):
    def __init__(self):
        super().__init__()

        self.username = 'illya'

        # візуальна частина
        self.geometry('800x600')
        self.title("LogiTalk - чат")
        self.minsize(400, 400)

        # налаштування для меню
        self.menu_width = 50
        self.target_menu_width = 50
        self.is_show_menu = False
        self.speed_menu = 5

        # вигляд меню
        self.menu_frame = CTkFrame(self, width= self.menu_width, height=600) # fg_color = 
        self.menu_frame.pack_propagate(False)
        self.menu_frame.place(x = 0, y = 0)

        # кнопка "Меню"
        self.btn_menu = CTkButton(self, text='M', width= 50, text_color= "#000000", 
                                  fg_color="#AD80D1", hover_color="#5D397A", command= self.click_menu)
        self.btn_menu.place(x = 0, y = 0)


        #### продовження інтерфейсу
        self.chat_field = CTkTextbox(self, font=('Arial', 14, 'bold'), state='disable')
        self.chat_field.place(x=0, y=0)

        self.message_entry = CTkEntry(self, placeholder_text='Введіть повідомлення', height=40)
        self.btn_send = CTkButton(self, text=">", width=60, height=40, command=self.send_message)

        
        try:
            self.sock = socket(AF_INET, SOCK_STREAM)
            self.sock.connect(('0.tcp.eu.ngrok.io', 14616))
            hello = f'{self.username} приєднався(-лась) до чату!\n'
            self.sock.send(hello.encode('UTF-8'))
            # потік для приймання повідомлень
        except:
            self.chat_field.configure(state = 'normal')
            self.chat_field.insert(END, f'Не вдалося приєднатися на сервер!\n')
            self.chat_field.configure(state = 'disable')
        
        
        self.after(100, self.adaptive_ui)


    def click_menu(self):
        self.is_show_menu = not self.is_show_menu
        self.target_menu_width = 200 if self.is_show_menu else 50 # якщо 50 то стане 200 і навпаки
        self.btn_menu.configure(text = 'Menu' if self.is_show_menu else 'M')

        if self.is_show_menu:
            ###################
            self.label_name = CTkLabel(self.menu_frame, text= "Ім'я")
            self.label_name.pack(pady = 50)
            self.entry_name = CTkEntry(self.menu_frame, placeholder_text="Введіть ім'я")
            self.entry_name.pack()
        
        else:
            ###################
            if self.label_name:
                self.label_name.destroy()
            if self.entry_name:
                self.entry_name.destroy()

        self.animate_menu()
        
    def animate_menu(self):
        if self.menu_width != self.target_menu_width:
            if self.menu_width < self.target_menu_width:
                self.menu_width = min(self.menu_width + self.speed_menu, self.target_menu_width)
            else:
                self.menu_width = max(self.menu_width - self.speed_menu, self.target_menu_width)
            self.menu_frame.configure(width = self.menu_width)
            self.after(10, self.animate_menu)

    def adaptive_ui(self):
        SCALE = 1.25 # 150% = 1.5,  75% = 0.75
        width = window.winfo_width() / SCALE
        height = window.winfo_height() / SCALE

        self.menu_frame.configure(height=height)

        input_panel_height = 60
        spacing = 10

        chat_x = self.menu_width + 10
        chat_width = width - self.menu_width - 30
        chat_height = height - input_panel_height - spacing

        self.chat_field.place(x=chat_x, y=0)
        self.chat_field.configure(width=chat_width, height=chat_height)

        entry_width = width - self.menu_width - 100
        entry_y = height - input_panel_height

        self.message_entry.place(x=chat_x, y=entry_y)
        self.message_entry.configure(width=entry_width)

        self.btn_send.place(x=chat_x + entry_width + 10, y=entry_y)

        self.after(100, self.adaptive_ui)  

        

    def add_message(self, text):
        self.chat_field.configure(state = 'normal')
        self.chat_field.insert(END, f'{self.username}: {text}\n')
        self.chat_field.configure(state = 'disable')

    def send_message(self):
        message = self.message_entry.get()
        self.message_entry.delete(0,END)
        print(message)
        if message:
            self.add_message(f"{message}")
            data = f'TEXT@{self.username}@{message}\n'
            try:
                self.sock.sendall(data.encode())
            except:
                pass
    
    def recv_message(self):
        buffer = ''
        while True:
            try:
                chunk = self.sock.recv(4096)
                if not chunk:
                    break
                buffer += chunk.decode()

                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    self.handle_line(line.strip())
            except:
                break
        self.sock.close()


    def handle_line(self, line):
        if not line:
            return
        parts = line.split('@',3) #'TEXT@stepan@text'
        msg_type = parts[0]

        if msg_type == 'TEXT':
            if len(parts) == 3:
                author = parts[1]
                msg = parts[2]
                self.add_message(f'{msg}')
        else:
            self.add_message(line)


        

window = MainWindow()
window.mainloop()