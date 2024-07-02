from tkinter import Tk, Frame, Button, Label, Entry, Toplevel, messagebox, END
from tkinter import Listbox
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
        self.goal_listbox = Listbox(goals_frame, selectmode='single', background='#FFFFFF', exportselection=False)

        for i, goal in enumerate(self.goals, start=1):
            self.goal_listbox.insert(END, f"Cel {i}: {goal[0]}")
            self.goals_buttons.append(goal)

        self.goal_listbox.pack(fill='both', expand=True, padx=10, pady=(0, 10))

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
        back_button = Button(goals_frame, text="Powrót do menu głównego", command=lambda: self.show_main_menu_and_close_window(goal_window), **self.button_style)
        back_button.pack(side='bottom', fill='x', padx=10, pady=(20, 10))

    def add_goal(self):
        goal_name = self.goal_name_entry.get()
        goal_days = self.goal_days_entry.get()

        if goal_name and goal_days.isdigit():
            goal_days = int(goal_days)
            self.goals.append((goal_name, goal_days, [], False))
            self.save_goals()
            messagebox.showinfo("Dodano cel", f"Dodano nowy cel: {goal_name} na {goal_days} dni.")
            self.goal_name_entry.delete(0, 'end')
            self.goal_days_entry.delete(0, 'end')
            
            # Aktualizacja listy celów w interfejsie użytkownika
            self.update_goals_list()
        else:
            messagebox.showwarning("Błąd", "Proszę wprowadzić poprawną nazwę celu i liczbę dni.")

    def update_goals_list(self):
        # Aktualizacja listy przycisków celów po lewej stronie
        self.goal_listbox.delete(0, END)
        for i, goal in enumerate(self.goals, start=1):
            if goal[3]:  # Sprawdź czy cel został ukończony
                status = "(Wykonane)"
        else:
            remaining_days = goal[1] - len(goal[2])  # Oblicz pozostałe dni do odznaczenia
            if remaining_days > 0:
                status = f"({remaining_days} dni do ukończenia)"
            else:
                status = "(Wykonane)"

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

        Label(self.goal_details_frame, text=f"Informacje o celu: {goal_name}", font=('Avenir', 18, 'bold'), background='#FFFFFF').pack(pady=10)

        goal_days_listbox = Listbox(self.goal_details_frame, selectmode='multiple', background='#FFFFFF')
        goal_days_listbox.pack(fill='both', expand=True, padx=10, pady=(0, 10))

        for day in range(1, goal_days + 1):
            if day in completed_days:
                goal_days_listbox.insert(END, f"Dzień {day} (ukończony)")
                goal_days_listbox.itemconfig(END, {'fg': 'green'})
            else:
                goal_days_listbox.insert(END, f"Dzień {day}")

        # Przycisk "Oznacz dzień jako ukończony"
        oznacz_dzien_button = Button(self.goal_details_frame, text="Ukończ dzień", command=lambda: self.oznacz_dzien_ukonczony(idx, goal_days_listbox.curselection()), **self.button_style)
        oznacz_dzien_button.pack(side='left', fill='x', padx=5, pady=(10, 20))

        # Przycisk "Edytuj cel"
        edytuj_cel_button = Button(self.goal_details_frame, text="Edytuj cel", command=lambda: self.edit_goal(idx), **self.button_style)
        edytuj_cel_button.pack(side='left', fill='x', padx=5, pady=(10, 20))

        # Przycisk "Usuń cel"
        usun_cel_button = Button(self.goal_details_frame, text="Usuń cel", command=lambda: self.delete_goal(idx), **self.button_style)
        usun_cel_button.pack(side='left', fill='x', padx=5, pady=(10, 20))

    def oznacz_dzien_ukonczony(self, goal_idx, selected_days):
        # Oznaczanie wybranego dnia jako ukończonego
        if not selected_days:
            messagebox.showwarning("Błąd", "Proszę wybrać co najmniej jeden dzień do oznaczenia jako ukończony.")
            return

        goal_name, goal_days, completed_days, completed = self.goals[goal_idx]
        for day_idx in selected_days:
            day = day_idx + 1
            if day not in completed_days:
                completed_days.append(day)

        self.goals[goal_idx] = (goal_name, goal_days, completed_days, completed)
        self.toggle_goal_details(goal_idx)
        self.update_goals_list()
        self.save_goals()

        if len(completed_days) == goal_days:
            self.goals[goal_idx] = (goal_name, goal_days, completed_days, True)
            messagebox.showinfo("Cel ukończony", f"Cel '{goal_name}' został oznaczony jako ukończony.")

    def edit_goal(self, idx):
        # Edytowanie danych celu
        goal_name, goal_days, completed_days, completed = self.goals[idx]

        self.edit_goal_window = Toplevel(self.master)
        self.edit_goal_window.title("Edytuj cel")
        self.edit_goal_window.geometry("400x300")

        Label(self.edit_goal_window, text="Edytuj cel:", font=('Avenir', 18, 'bold')).pack(pady=10)

        Label(self.edit_goal_window, text="Nazwa celu:").pack(anchor='w', padx=10)
        self.edit_goal_name_entry = Entry(self.edit_goal_window)
        self.edit_goal_name_entry.pack(fill='x', padx=10, pady=(0, 10))
        self.edit_goal_name_entry.insert(0, goal_name)

        Label(self.edit_goal_window, text="Liczba dni:").pack(anchor='w', padx=10)
        self.edit_goal_days_entry = Entry(self.edit_goal_window)
        self.edit_goal_days_entry.pack(fill='x', padx=10, pady=(0, 10))
        self.edit_goal_days_entry.insert(0, goal_days)

        save_button = Button(self.edit_goal_window, text="Zapisz zmiany", command=lambda: self.save_edited_goal(idx), **self.button_style)
        save_button.pack(fill='x', padx=10, pady=(10, 20))

    def save_edited_goal(self, idx):
        # Zapisywanie edytowanych danych celu
        new_name = self.edit_goal_name_entry.get()
        new_days = self.edit_goal_days_entry.get()

        if new_name and new_days.isdigit():
            new_days = int(new_days)
            _, _, completed_days, completed = self.goals[idx]
            self.goals[idx] = (new_name, new_days, completed_days, completed)
            self.update_goals_list()
            self.save_goals()
            messagebox.showinfo("Zapisano", f"Zapisano zmiany dla celu: {new_name}.")
            self.edit_goal_window.destroy()
        else:
            messagebox.showwarning("Błąd", "Proszę wprowadzić poprawną nazwę celu i liczbę dni.")

    def delete_goal(self, idx):
        # Usuwanie celu
        goal_name, _, _, _ = self.goals[idx]
        confirm = messagebox.askyesno("Usuń cel", f"Czy na pewno chcesz usunąć cel: {goal_name}?")
        if confirm:
            del self.goals[idx]
            self.update_goals_list()
            self.save_goals()
            self.goal_details_frame.destroy()
            messagebox.showinfo("Usunięto", f"Cel '{goal_name}' został usunięty.")

    def load_goals(self):
        if os.path.exists("goals.txt"):
            try:
                with open("goals.txt", "r") as file:
                    for line in file:
                        data = line.strip().split('|')
                        if len(data) == 4:
                            goal_name = data[0]
                            try:
                                goal_days = int(data[1])
                            except ValueError:
                                print(f"Ignorowanie nieprawidłowej linii w pliku (błędna liczba dni): {line}")
                                continue

                            completed_days_str = data[2]
                            if completed_days_str:
                                try:
                                    completed_days = list(map(int, completed_days_str.split(',')))
                                except ValueError:
                                    print(f"Ignorowanie nieprawidłowej linii w pliku (błędne dni ukończone): {line}")
                                    continue
                            else:
                                completed_days = []

                            completed = data[3].strip().lower() == 'true'
                            self.goals.append((goal_name, goal_days, completed_days, completed))
                        else:
                            print(f"Ignorowanie nieprawidłowej linii w pliku (nieprawidłowa liczba pól): {line}")
                # Po wczytaniu celów, aktualizujemy listę w interfejsie użytkownika
                self.update_goals_list()
            except Exception as e:
                print(f"Wystąpił błąd podczas wczytywania danych z pliku goals.txt: {e}")

    def save_goals(self):
        try:
            with open("goals.txt", "w") as file:
                for goal in self.goals:
                    goal_name, goal_days, completed_days, completed = goal
                    completed_days_str = ",".join(map(str, completed_days))
                    file.write(f"{goal_name}|{goal_days}|{completed_days_str}|{completed}\n")
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się zapisać celów: {e}")


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
