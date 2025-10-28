from customtkinter import *
from PIL import Image

class AuthWindow(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("700x400")
        self.title("LogiTalk - Вхід")
        self.resizable(False, False)

        #ЛІВА ЧАСТИНА
        self.left_frame = CTkFrame(self)
        self.left_frame.pack(side = "left", fill = "both")

        img_ctk = CTkImage(light_image=Image.open("bg444.jpg"), size = (450, 400))
        self.img_lbl = CTkLabel(self.left_frame, text = "Welcome", image= img_ctk,font= ("Helvetica", 60, "bold"),text_color="white")
        self.img_lbl.pack()
        #ПРАВА ЧАСТИНА
        self.right_frame = CTkFrame(self, fg_color="grey")
        self.right_frame.pack_propagate(False)
        self.right_frame.pack(side = "right", fill = "both",expand = "True")

        self.title_lbl = CTkLabel(self.right_frame, text = "LogiTalk",font= ("Helvetica", 30, "bold"),text_color="#fffdf7")
        self.title_lbl.pack(pady = 60)

        self.entry_name = CTkEntry(self.right_frame,placeholder_text="Введіть ім'я", placeholder_text_color="white", text_color="white",
                                   fg_color="#383735", border_color="#383735",font= ("Helvetica", 20, "bold"), corner_radius=25)
        self.entry_name.pack(fill = "x", padx = 15, pady = 15)

        self.login_btn = CTkButton(self.right_frame, text="Увійти", height=45,font= ("Helvetica", 20, "bold"),text_color="white", fg_color="#333231",hover_color="#1a1918")
        self.login_btn.pack(fill = "x",padx = 45,pady = 10)

win = AuthWindow()
win.mainloop()