from customtkinter import *
class App(CTk):
    def __init__(self):
        super().__init__()
        self.text = CTkEntry(self, placeholder_text="how was your day?...")
        self.text.pack(padx=20, pady=20)
if __name__ == "__main__":
    app = App()
    app.mainloop()