from tkinter import Tk, Frame, Button, Label, Entry, Toplevel, messagebox, Scrollbar, Listbox, END, Canvas
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

        # Formularz dodawania celu
        Label(content_frame, text="Dodaj nowy cel:", font=('Avenir', 18, 'bold'), background='#FFFFFF').grid(row=0, column=0, columnspan=3, pady=10)

        Label(content_frame, text="Nazwa celu:", background='#FFFFFF').grid(row=1, column=0, sticky='w')
        self.goal_name_entry = Entry(content_frame)
        self.goal_name_entry.grid(row=1, column=1, padx=10, pady=10, columnspan=2)

        Label(content_frame, text="Liczba dni:", background='#FFFFFF').grid(row=2, column=0, sticky='w')
        self.goal_days_entry = Entry(content_frame)
        self.goal_days_entry.grid(row=2, column=1, padx=10, pady=10)

        add_button = Button(content_frame, text="Dodaj cel", command=self.add_goal, **self.button_style)
        add_button.grid(row=3, columnspan=3, pady=10)

        # Lista celów
        self.goals_frame = Frame(content_frame, background='#FFFFFF')
        self.goals_frame.grid(row=4, column=0, columnspan=3, pady=20)

        # Wczytanie zapisanych celów (jeśli istnieją)
        self.goals = []  # Lista przechowująca cele w formacie (nazwa, liczba_dni, ukończone_dni)
        self.load_goals()
        self.update_goals_list()

        # Przycisk "Powrót do menu głównego"
        back_button = Button(content_frame, text="Powrót do menu głównego", command=lambda: self.show_main_menu_and_close_window(goal_window), **self.button_style)
        back_button.grid(row=5, column=0, columnspan=3, pady=20)

    def add_goal(self):
        # Dodawanie celu na podstawie danych z formularza
        goal_name = self.goal_name_entry.get()
        goal_days = self.goal_days_entry.get()

        if goal_name and goal_days.isdigit():
            goal_days = int(goal_days)
            self.goals.append((goal_name, goal_days, []))
            self.update_goals_list()
            self.save_goals()
            messagebox.showinfo("Dodano cel", f"Dodano nowy cel: {goal_name} na {goal_days} dni.")
            self.goal_name_entry.delete(0, 'end')
            self.goal_days_entry.delete(0, 'end')
        else:
            messagebox.showwarning("Błąd", "Proszę wprowadzić poprawną nazwę celu i liczbę dni.")

    def update_goals_list(self):
        # Aktualizacja listy celów na ekranie zarządzania celami
        for widget in self.goals_frame.winfo_children():
            widget.destroy()

        for i, (goal_name, goal_days, completed_days) in enumerate(self.goals, start=1):
            goal_frame = Frame(self.goals_frame, background='#FFFFFF')
            goal_frame.pack(fill='x', padx=10, pady=5)

            days_left = goal_days - len(completed_days)
            Label(goal_frame, text=f"Cel {i}: {goal_name} na {goal_days} dni (Pozostało: {days_left} dni)", background='#FFFFFF').grid(row=0, column=0, sticky='w')

            # Scrollbar i lista dni
            days_frame = Frame(goal_frame, background='#FFFFFF')
            days_frame.grid(row=1, column=0, columnspan=3, pady=10)

            scrollbar = Scrollbar(days_frame, orient="vertical")
            scrollbar.pack(side='right', fill='y')

            goal_days_listbox = Listbox(days_frame, width=20, height=10, selectmode='multiple', background='#FFFFFF', yscrollcommand=scrollbar.set)
            goal_days_listbox.pack(side='left', fill='both', expand=True)

            for j in range(1, goal_days + 1):
                goal_days_listbox.insert(END, f"Dzień {j}")
                if j in completed_days:
                    goal_days_listbox.itemconfig(j-1, {'bg':'green'})

            goal_days_listbox.bind('<<ListboxSelect>>', lambda event, idx=i-1, listbox=goal_days_listbox: self.mark_completed_days(idx, listbox))

            scrollbar.config(command=goal_days_listbox.yview)

            # Przyciski edycji i usuwania
            edit_button = Button(goal_frame, text="Edytuj", command=lambda idx=i-1: self.edit_goal(idx), **{**self.button_style, 'padx': 5, 'pady': 2})
            edit_button.grid(row=2, column=1, padx=5)

            delete_button = Button(goal_frame, text="Usuń", command=lambda idx=i-1: self.delete_goal(idx), **{**self.button_style, 'padx': 5, 'pady': 2})
            delete_button.grid(row=2, column=2, padx=5)

    def mark_completed_days(self, idx, listbox):
        # Odznaczanie wykonanych zadań dla danego celu
        selected_indices = listbox.curselection()
        completed_days = self.goals[idx][2]

        for index in selected_indices:
            day = index + 1
            if day not in completed_days:
                completed_days.append(day)
                listbox.itemconfig(index, {'bg':'green'})
            else:
                completed_days.remove(day)
                listbox.itemconfig(index, {'bg':'white'})

        self.goals[idx] = (self.goals[idx][0], self.goals[idx][1], completed_days)
        self.save_goals()
        self.update_goals_list()

    def edit_goal(self, idx):
        # Okno edycji celu na podstawie jego indeksu
        edit_window = Toplevel(self.master)
        edit_window.title("Edytuj cel")
        edit_window.geometry("300x150")

        content_frame = Frame(edit_window, background='#FFFFFF')
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)

        goal_name_label = Label(content_frame, text="Nowa nazwa celu:", background='#FFFFFF')
        goal_name_label.grid(row=0, column=0, padx=10, pady=10)

        goal_name_entry = Entry(content_frame)
        goal_name_entry.insert(0, self.goals[idx][0])
        goal_name_entry.grid(row=0, column=1, padx=10, pady=10)

        goal_days_label = Label(content_frame, text="Nowa liczba dni:", background='#FFFFFF')
        goal_days_label.grid(row=1, column=0, padx=10, pady=10)

        goal_days_entry = Entry(content_frame)
        goal_days_entry.insert(0, self.goals[idx][1])
        goal_days_entry.grid(row=1, column=1, padx=10, pady=10)

        save_button = Button(content_frame, text="Zapisz zmiany", command=lambda: self.save_edited_goal(idx, goal_name_entry.get(), goal_days_entry.get(), edit_window), **self.button_style)
        save_button.grid(row=2, columnspan=2, pady=10)

    def save_edited_goal(self, idx, new_goal_name, new_goal_days, window):
        # Zapisanie edytowanego celu na podstawie indeksu w liście celów
        if new_goal_name and new_goal_days.isdigit():
            self.goals[idx] = (new_goal_name, int(new_goal_days), self.goals[idx][2])
            self.update_goals_list()
            self.save_goals()
            messagebox.showinfo("Zapisano zmiany", "Zapisano zmiany w celu.")
            window.destroy()
        else:
            messagebox.showwarning("Błąd", "Proszę wprowadzić poprawną nazwę celu i liczbę dni.")

    def delete_goal(self, idx):
        # Usunięcie celu na podstawie indeksu w liście celów
        del self.goals[idx]
        self.update_goals_list()
        self.save_goals()
        messagebox.showinfo("Usunięto cel", "Usunięto wybrany cel.")

    def save_goals(self):
        # Zapisanie listy celów do pliku tekstowego
        with open("goals_save.txt", "w") as f:
            for goal_name, goal_days, completed_days in self.goals:
                completed_days_str = ','.join(map(str, completed_days))
                f.write(f"{goal_name},{goal_days},{completed_days_str}\n")

    def load_goals(self):
        # Wczytanie listy celów z pliku tekstowego (jeśli istnieje)
        if os.path.exists("goals_save.txt"):
            with open("goals_save.txt", "r") as f:
                for line in f:
                    goal_name, goal_days, *completed_days = line.strip().split(',')
                    self.goals.append((goal_name, int(goal_days), list(map(int, completed_days))))

    def show_main_menu_and_close_window(self, window):
        # Powrót do głównego menu i zamknięcie okna podrzędnego
        window.destroy()
        self.master.deiconify()

    def show_help_content(self):
        messagebox.showinfo("Pomoc", "Lorem ipsum dolor sit amet, consectetur adipiscing elit.")

    def show_author_content(self):
        messagebox.showinfo("Autor", "Autor: Krystian Harasymek")

def main():
    root = Tk()
    app = MainMenu(root)
    root.mainloop()

if __name__ == "__main__":
    main()
