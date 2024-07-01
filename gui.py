from tkinter import Tk, Frame, Button, Label, Entry, Toplevel, messagebox, Scrollbar, Listbox, END, RIGHT, X, Y, VERTICAL
from PIL import Image, ImageTk
import tkinter.font as tkFont
import os

class MainMenu:
    def __init__(self, master):
        self.master = master
        self.master.title("Celebr")
        self.master.geometry("800x600")
        self.master.configure(background='#FFFFFF')

        # Logo aplikacji
        self.logo_image = Image.open("logo.png")
        self.logo_image = self.logo_image.resize((150, 150), Image.BILINEAR)
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)

        # Logo na górze głównego okna
        self.logo_label = Label(self.master, image=self.logo_photo, background='#FFFFFF')
        self.logo_label.pack()

        # Nagłówek aplikacji
        app_name_font = tkFont.Font(family="Avenir", size=36, weight="bold")
        self.app_name_label = Label(self.master, text="Celebr", font=app_name_font, background='#FFFFFF', fg='#1a3b4c')
        self.app_name_label.pack()

        # Styl dla przycisków menu
        self.button_style = {
            'font': ('Avenir', 14),
            'background': '#1a3b4c',
            'foreground': '#FFFFFF',
            'activebackground': '#2c5d6b',
            'activeforeground': '#FFFFFF',
            'borderwidth': 0,
            'highlightthickness': 0,
            'padx': 10,
            'pady': 5,
        }

        # Przycisk "Rozpocznij"
        self.start_button = Button(self.master, text="Rozpocznij", command=self.show_goal_management_screen, **self.button_style)
        self.start_button.pack(fill='x', padx=10, pady=10)

        # Przyciski menu
        self.help_button = Button(self.master, text="Pomoc", command=self.show_help_content, **self.button_style)
        self.help_button.pack(fill='x', padx=10, pady=10)

        self.author_button = Button(self.master, text="Autor", command=self.show_author_content, **self.button_style)
        self.author_button.pack(fill='x', padx=10, pady=10)

        self.quit_button = Button(self.master, text="Wyjdź", command=self.master.quit, **self.button_style)
        self.quit_button.pack(fill='x', padx=10, pady=(10, 40))

        # Lista celów
        self.goals = []  # Lista przechowująca cele w formacie (nazwa, liczba_dni, ukończone_dni, ukończony)

        # Wczytanie zapisanych celów (jeśli istnieją)
        self.load_goals()

    def show_goal_management_screen(self):
        # Zamknięcie głównego okna menu
        self.master.withdraw()

        # Tworzenie nowego okna Toplevel dla zarządzania celami
        goal_window = Toplevel(self.master)
        goal_window.title("Zarządzanie celami")
        goal_window.geometry("800x600")

        # Ramka dla zawartości
        content_frame = Frame(goal_window, background='#FFFFFF')
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Ramka z przyciskami celów po lewej stronie
        goals_frame = Frame(content_frame, background='#FFFFFF', width=300)
        goals_frame.pack(side='left', fill='y', padx=(0, 10), pady=10)

        Label(goals_frame, text="Twoje cele:", font=('Avenir', 18, 'bold'), background='#FFFFFF').pack(pady=10)

        # Lista przewijana dla przycisków celów
        self.goals_buttons = []
        self.scrollbar = Scrollbar(goals_frame, orient=VERTICAL)
        self.goal_listbox = Listbox(goals_frame, yscrollcommand=self.scrollbar.set, selectmode='single', background='#FFFFFF', exportselection=False)

        for i, goal in enumerate(self.goals, start=1):
            self.goal_listbox.insert(END, f"Cel {i}: {goal[0]}")
            self.goals_buttons.append(goal)

        self.goal_listbox.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.scrollbar.config(command=self.goal_listbox.yview)

        self.goal_listbox.bind('<<ListboxSelect>>', self.on_goal_select)

        # Linia oddzielająca
        separator = Frame(content_frame, width=2, background='#1a3b4c')
        separator.pack(side='left', fill='y', padx=10)

        # Formularz dodawania celu po prawej stronie
        self.add_goal_frame = Frame(content_frame, background='#FFFFFF')
        self.add_goal_frame.pack(side='right', fill='both', expand=True)

        Label(self.add_goal_frame, text="Dodaj nowy cel:", font=('Avenir', 18, 'bold'), background='#FFFFFF').pack(pady=10)

        Label(self.add_goal_frame, text="Nazwa celu:", background='#FFFFFF').pack(anchor='w', padx=10)
        self.goal_name_entry = Entry(self.add_goal_frame)
        self.goal_name_entry.pack(fill='x', padx=10, pady=(0, 10))

        Label(self.add_goal_frame, text="Liczba dni:", background='#FFFFFF').pack(anchor='w', padx=10)
        self.goal_days_entry = Entry(self.add_goal_frame)
        self.goal_days_entry.pack(fill='x', padx=10, pady=(0, 10))

        add_button = Button(self.add_goal_frame, text="Dodaj cel", command=self.add_goal, **self.button_style)
        add_button.pack(fill='x', padx=10, pady=(10, 20))

        # Przycisk "Powrót do menu głównego"
        back_button = Button(content_frame, text="Powrót do menu głównego", command=lambda: self.show_main_menu_and_close_window(goal_window), **self.button_style)
        back_button.pack(side='bottom', fill='x', padx=10, pady=(20, 10))

    def add_goal(self):
        # Dodawanie celu na podstawie danych z formularza
        goal_name = self.goal_name_entry.get()
        goal_days = self.goal_days_entry.get()

        if goal_name and goal_days.isdigit():
            goal_days = int(goal_days)
            self.goals.append((goal_name, goal_days, [], False))
            self.update_goals_list()
            self.save_goals()
            messagebox.showinfo("Dodano cel", f"Dodano nowy cel: {goal_name} na {goal_days} dni.")
            self.goal_name_entry.delete(0, 'end')
            self.goal_days_entry.delete(0, 'end')
        else:
            messagebox.showwarning("Błąd", "Proszę wprowadzić poprawną nazwę celu i liczbę dni.")

    def update_goals_list(self):
        # Aktualizacja listy przycisków celów po lewej stronie
        self.goal_listbox.delete(0, END)
        for i, goal in enumerate(self.goals, start=1):
            status = "(Wykonane)" if goal[3] else ""
            self.goal_listbox.insert(END, f"Cel {i}: {goal[0]} {status}")

    def on_goal_select(self, event):
        # Obsługa zdarzenia wyboru celu z listy
        selected_idx = self.goal_listbox.curselection()
        if selected_idx:
            idx = selected_idx[0]
            self.toggle_goal_details(idx)

    def toggle_goal_details(self, idx):
        # Rozsuwanie/zwijanie szczegółów celu
        if hasattr(self, 'goal_details_frame'):
            self.goal_details_frame.destroy()

        goal_name, goal_days, completed_days, completed = self.goals[idx]

        self.goal_details_frame = Frame(self.add_goal_frame, background='#FFFFFF')
        self.goal_details_frame.pack(fill='both', expand=True, padx=10, pady=10)

        Label(self.goal_details_frame, text=f"Detale celu '{goal_name}':", font=('Avenir', 18, 'bold'), background='#FFFFFF').pack(pady=10)

        goal_days_listbox = Listbox(self.goal_details_frame, selectmode='multiple', background='#FFFFFF')
        goal_days_listbox.pack(fill='both', expand=True, padx=10, pady=(0, 10))

        for day in range(1, goal_days + 1):
            if day in completed_days:
                goal_days_listbox.insert(END, f"Dzień {day} (ukończony)")
                goal_days_listbox.itemconfig(END, {'fg': 'green'})
            else:
                goal_days_listbox.insert(END, f"Dzień {day}")

        toggle_completed_button = Button(self.goal_details_frame, text="Oznacz jako ukończone", command=lambda: self.mark_goal_completed(idx), **self.button_style)
        toggle_completed_button.pack(fill='x', padx=10, pady=(10, 20))

    def mark_goal_completed(self, idx):
        # Oznaczanie celu jako ukończony
        goal_name, goal_days, completed_days, completed = self.goals[idx]
        if not completed:
            self.goals[idx] = (goal_name, goal_days, list(range(1, goal_days + 1)), True)
            self.update_goals_list()
            self.save_goals()
            messagebox.showinfo("Cel ukończony", f"Cel '{goal_name}' został oznaczony jako ukończony.")
        else:
            messagebox.showwarning("Błąd", "Ten cel został już wcześniej oznaczony jako ukończony.")

    def save_goals(self):
        # Zapisywanie celów do pliku goals.txt
        with open("goals.txt", "w") as file:
            for goal in self.goals:
                goal_name, goal_days, completed_days, completed = goal
                completed_str = 'True' if completed else 'False'
                completed_days_str = ','.join(map(str, completed_days))
                file.write(f"{goal_name},{goal_days},{completed_days_str},{completed_str}\n")

    def load_goals(self):
        # Wczytywanie celów z pliku goals.txt
        if os.path.exists("goals.txt"):
            with open("goals.txt", "r") as file:
                for line in file:
                    data = line.strip().split(',')
                    if len(data) == 4:
                        goal_name = data[0]
                        goal_days = int(data[1])
                        completed_days = list(map(int, data[2].split(',')))
                        completed = True if data[3] == 'True' else False
                        self.goals.append((goal_name, goal_days, completed_days, completed))
                    else:
                        print(f"Ignorowanie nieprawidłowej linii w pliku: {line}")

    def show_main_menu_and_close_window(self, window):
        # Powrót do menu głównego i zamknięcie bieżącego okna
        window.destroy()
        self.master.deiconify()

    def show_help_content(self):
        messagebox.showinfo("Pomoc", "Aplikacja do zarządzania celami. Dodawaj nowe cele i śledź ich postęp.")

    def show_author_content(self):
        messagebox.showinfo("Autor", "Aplikacja stworzona przez [Twoje imię/nazwisko].")

if __name__ == "__main__":
    root = Tk()
    app = MainMenu(root)
    root.mainloop()
