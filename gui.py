from tkinter import Tk, Frame, Label, Button, Toplevel

class ApplicationGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Menu Wyboru Użytkownika")

        self.frame = Frame(master)
        self.frame.pack()

        self.label = Label(self.frame, text="Menu Wyboru Użytkownika", font=("Helvetica", 16))
        self.label.pack(pady=20)

        self.user_button = Button(self.frame, text="Panel Użytkownika", command=self.open_user_panel)
        self.user_button.pack(pady=10)

    def open_user_panel(self):
        user_panel_window = Toplevel(self.master)
        user_panel_window.title("Panel Użytkownika")
        user_panel_window.geometry("400x300")

        label_user = Label(user_panel_window, text="Witaj w panelu użytkownika!", font=("Helvetica", 14))
        label_user.pack(pady=20)

        button_example = Button(user_panel_window, text="Przykładowy przycisk", command=lambda: print("Akcja przycisku"))
        button_example.pack(pady=10)

def main():
    root = Tk()
    app = ApplicationGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
