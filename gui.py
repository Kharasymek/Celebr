from tkinter import Tk, Frame, Button, Label

class MainMenu:
    def __init__(self, master):
        """
        Inicjalizacja głównego okna aplikacji.
        
        Args:
            master (Tk): Główne okno Tkinter.
        """
        self.master = master
        self.master.title("Menu Aplikacji")
        self.master.geometry("600x400")  # Zwiększenie wymiarów okna głównego
        
        self.frame = Frame(master)
        self.frame.pack(padx=20, pady=50)
        
        self.current_frame = None  # Zmienna przechowująca aktualnie wyświetlany obszar
        
        self.show_main_menu()  # Wyświetlenie głównego menu na starcie
    
    def show_main_menu(self):
        """
        Wyświetlenie głównego menu aplikacji.
        """
        if self.current_frame:
            self.current_frame.destroy()
        
        self.current_frame = Frame(self.frame)
        self.current_frame.pack(padx=20, pady=20)
        
        self.start_button = Button(self.current_frame, text="Rozpocznij", width=20, height=2, command=self.start_application)
        self.start_button.pack(pady=10)
        
        self.help_button = Button(self.current_frame, text="Pomoc", width=20, height=2, command=self.show_help)
        self.help_button.pack(pady=10)
        
        self.author_button = Button(self.current_frame, text="Autor", width=20, height=2, command=self.show_author)
        self.author_button.pack(pady=10)
        
        self.quit_button = Button(self.current_frame, text="Wyjdź", width=20, height=2, command=self.quit_application)
        self.quit_button.pack(pady=10)
    
    def start_application(self):
        """
        Wyświetlenie sekcji rozpoczęcia aplikacji.
        """
        if self.current_frame:
            self.current_frame.destroy()
        
        self.current_frame = Frame(self.frame)
        self.current_frame.pack(padx=20, pady=20)
        
        # Tutaj umieść kod, który przełącza się do głównej części aplikacji
        info_label = Label(self.current_frame, text="Rozpoczęto główną część aplikacji.")
        info_label.pack(pady=20)
        
        back_button = Button(self.current_frame, text="Powrót", command=self.show_main_menu)
        back_button.pack(pady=10)
    
    def show_help(self):
        """
        Wyświetlenie sekcji pomocy.
        """
        if self.current_frame:
            self.current_frame.destroy()
        
        self.current_frame = Frame(self.frame)
        self.current_frame.pack(padx=20, pady=20)
        
        # Tutaj umieść kod, który wyświetli pomoc (np. Lorem Ipsum)
        info_label = Label(self.current_frame, text="Lorem ipsum dolor sit amet, consectetur adipiscing elit.")
        info_label.pack(pady=20)
        
        back_button = Button(self.current_frame, text="Powrót", command=self.show_main_menu)
        back_button.pack(pady=10)
    
    def show_author(self):
        """
        Wyświetlenie sekcji informacji o autorze.
        """
        if self.current_frame:
            self.current_frame.destroy()
        
        self.current_frame = Frame(self.frame)
        self.current_frame.pack(padx=20, pady=20)
        
        info_label = Label(self.current_frame, text="Autor: Krystian Harasymek")
        info_label.pack(pady=20)
        
        back_button = Button(self.current_frame, text="Powrót", command=self.show_main_menu)
        back_button.pack(pady=10)
    
    def quit_application(self):
        """
        Funkcja zamykająca aplikację.
        """
        self.master.destroy()

def main():
    """
    Funkcja uruchamiająca główne okno aplikacji.
    """
    root = Tk()
    app = MainMenu(root)
    root.mainloop()

if __name__ == "__main__":
    main()
