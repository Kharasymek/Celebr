import json
import os
from tkinter import Tk, Frame, Label, Entry, Toplevel, messagebox, END, Listbox, MULTIPLE, Button
from PIL import Image, ImageTk
import tkinter.font as tkFont

class DepthButton(Button):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.default_bg = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<ButtonPress-1>", self.on_press)
        self.bind("<ButtonRelease-1>", self.on_release)

    def on_enter(self, event):
        self["relief"] = "raised"
        self["background"] = "#2c5d6b"

    def on_leave(self, event):
        self["relief"] = "flat"
        self["background"] = self.default_bg

    def on_press(self, event):
        self["relief"] = "sunken"
        self["background"] = "#1a3b4c"

    def on_release(self, event):
        self["relief"] = "raised"
        self["background"] = "#2c5d6b"
        if self["command"]:
            self["command"]()

class MainMenu:
    def __init__(self, master):
        self.master = master
        self.master.title("Celebr")
        self.master.geometry("1000x800")
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
            'borderwidth': 2,
            'highlightthickness': 0,
            'padx': 10,
            'pady': 5,
        }

        # Przycisk "Rozpocznij"
        self.start_button = DepthButton(self.master, text="Rozpocznij", command=self.show_goal_management_screen, **self.button_style)
        self.start_button.pack(fill='x', padx=10, pady=10)

        # Przyciski menu
        self.help_button = DepthButton(self.master, text="Pomoc", command=self.show_help_content, **self.button_style)
        self.help_button.pack(fill='x', padx=10, pady=10)

        self.author_button = DepthButton(self.master, text="Autor", command=self.show_author_content, **self.button_style)
        self.author_button.pack(fill='x', padx=10, pady=10)

        self.quit_button = DepthButton(self.master, text="Wyjdź", command=self.master.quit, **self.button_style)
        self.quit_button.pack(fill='x', padx=10, pady=(10, 40))

        # Lista celów
        self.goals = []  # Lista przechowująca cele

        # Wczytanie zapisanych celów (jeśli istnieją)
        self.load_goals()

    def show_goal_management_screen(self):
        # Zamknięcie głównego okna menu
        self.master.withdraw()

        # Tworzenie nowego okna Toplevel dla zarządzania celami
        goal_window = Toplevel(self.master)
        goal_window.title("Zarządzanie celami")
        goal_window.geometry("1000x800")

        # Ramka dla zawartości
        content_frame = Frame(goal_window, background='#FFFFFF')
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Ramka z przyciskami celów po lewej stronie
        goals_frame = Frame(content_frame, background='#FFFFFF', width=300)
        goals_frame.pack(side='left', fill='y', padx=(0, 10), pady=10)

        Label(goals_frame, text="Twoje cele:", font=('Avenir', 18, 'bold'), background='#FFFFFF').pack(pady=10)

        # Lista przewijana dla przycisków celów
        self.goal_listbox = Listbox(goals_frame, selectmode='single', background='#FFFFFF', exportselection=False)
        self.goal_listbox.pack(fill='both', expand=True, padx=10, pady=(0, 10))

        self.goal_listbox.bind('<<ListboxSelect>>', self.on_goal_select)

        # Pobranie listy celów do wyświetlenia
        self.update_goals_list()

        # Linia oddzielająca
        separator = Frame(content_frame, width=2, background='#1a3b4c')
        separator.pack(side='left', fill='y', padx=10)

        # Formularz dodawania celu po prawej stronie
        self.add_goal_frame = Frame(content_frame, background='#FFFFFF', highlightbackground='#1a3b4c', highlightthickness=2, padx=10, pady=10)
        self.add_goal_frame.pack(side='right', fill='both', expand=True, padx=20, pady=20)

        Label(self.add_goal_frame, text="Dodaj nowy cel:", font=('Avenir', 18, 'bold'), background='#FFFFFF').pack(pady=10)

        Label(self.add_goal_frame, text="Nazwa celu:", background='#FFFFFF').pack(anchor='w', padx=10)
        self.goal_name_entry = Entry(self.add_goal_frame, font=('Avenir', 12), relief="solid", bd=2)
        self.goal_name_entry.pack(fill='x', padx=10, pady=(0, 10))

        Label(self.add_goal_frame, text="Liczba dni:", background='#FFFFFF').pack(anchor='w', padx=10)
        self.goal_days_entry = Entry(self.add_goal_frame, font=('Avenir', 12), relief="solid", bd=2)
        self.goal_days_entry.pack(fill='x', padx=10, pady=(0, 10))

        add_button = DepthButton(self.add_goal_frame, text="Dodaj cel", command=self.add_goal, **self.button_style)
        add_button.pack(fill='x', padx=10, pady=(10, 20))

        # Przycisk "Powrót do menu głównego"
        back_button = DepthButton(goals_frame, text="Powrót do menu głównego", command=lambda: self.show_main_menu_and_close_window(goal_window), **self.button_style)
        back_button.pack(side='bottom', fill='x', padx=10, pady=(20, 10))

    def add_goal(self):
        goal_name = self.goal_name_entry.get()
        goal_days = self.goal_days_entry.get()

        if goal_name and goal_days.isdigit():
            goal_days = int(goal_days)
            new_goal = {
                'name': goal_name,
                'days': goal_days,
                'completed_days': [],
                'completed': False
            }
            self.goals.append(new_goal)
            self.save_goals()
            messagebox.showinfo("Dodano cel", f"Dodano nowy cel: {goal_name} na {goal_days} dni.")
            self.goal_name_entry.delete(0, 'end')
            self.goal_days_entry.delete(0, 'end')
            self.update_goals_list()
        else:
            messagebox.showwarning("Błąd", "Proszę wprowadzić poprawną nazwę celu i liczbę dni.")

    def update_goals_list(self):
        # Wyczyść listę celów przed aktualizacją
        self.goal_listbox.delete(0, END)

        # Dodaj cele do listy
        for i, goal in enumerate(self.goals, start=1):
            goal_name = goal['name']
            goal_days = goal['days']
            completed_days = goal['completed_days']
            days_left = goal_days - len(completed_days)
            
            if days_left <= 0:
                goal['completed'] = True
                self.goal_listbox.insert(END, f"Cel {i}: {goal_name} na {goal_days} dni (Ukończony)")
                self.goal_listbox.itemconfig(END, {'fg': 'green'})
            else:
                self.goal_listbox.insert(END, f"Cel {i}: {goal_name} na {goal_days} dni (Pozostało: {days_left} dni)")

    def on_goal_select(self, event):
        # Obsługa zdarzenia wyboru celu z listy
        selected_indices = self.goal_listbox.curselection()
        if selected_indices:
            idx = selected_indices[0]
            self.show_goal_details(idx)

    def show_goal_details(self, idx):
        goal_name = self.goals[idx]['name']
        goal_days = self.goals[idx]['days']
        completed_days = self.goals[idx]['completed_days']

        self.goal_details_frame = Frame(self.add_goal_frame, background='#FFFFFF')
        self.goal_details_frame.pack(fill='both', expand=True, padx=10, pady=10)

        Label(self.goal_details_frame, text=f"Informacje o celu: {goal_name}", font=('Avenir', 18, 'bold'), background='#FFFFFF').pack(pady=10)

        self.goal_days_listbox = Listbox(self.goal_details_frame, selectmode=MULTIPLE, background='#FFFFFF')
        self.goal_days_listbox.pack(fill='both', expand=True, padx=10, pady=10)

        # Aktualizacja listy dni ukończonych
        self.update_goal_days_listbox(goal_days, completed_days)

        # Przycisk "Oznacz dzień ukończony"
        oznacz_dzien_button = DepthButton(self.goal_details_frame, text="Ukończ dzień", command=lambda: self.oznacz_dzien_ukonczony(idx), **self.button_style)
        oznacz_dzien_button.pack(side='left', fill='x', padx=5, pady=(10, 20))

        # Przycisk "Edytuj cel"
        edit_button = DepthButton(self.goal_details_frame, text="Edytuj cel", command=lambda: self.edit_goal(idx), **self.button_style)
        edit_button.pack(side='left', fill='x', padx=5, pady=(10, 20))

        # Przycisk "Usuń cel"
        remove_button = DepthButton(self.goal_details_frame, text="Usuń cel", command=lambda: self.remove_goal(idx), **self.button_style)
        remove_button.pack(side='left', fill='x', padx=5, pady=(10, 20))

    def update_goal_days_listbox(self, goal_days, completed_days):
        self.goal_days_listbox.delete(0, END)
        for day in range(1, goal_days + 1):
            if day in completed_days:
                self.goal_days_listbox.insert(END, f"Dzień {day} (ukończony)")
                self.goal_days_listbox.itemconfig(END, {'fg': 'green'})
            else:
                self.goal_days_listbox.insert(END, f"Dzień {day}")

    def oznacz_dzien_ukonczony(self, idx):
        selected_indices = self.goal_days_listbox.curselection()
        selected_days = [int(self.goal_days_listbox.get(idx).split()[1]) for idx in selected_indices]

        for day_number in selected_days:
            if day_number in self.goals[idx]['completed_days']:
                self.goals[idx]['completed_days'].remove(day_number)
            else:
                self.goals[idx]['completed_days'].append(day_number)

        self.save_goals()
        self.update_goal_days_listbox(self.goals[idx]['days'], self.goals[idx]['completed_days'])
        self.update_goals_list()  # Dodajemy aktualizację listy celów po zaktualizowaniu dni ukończonych
        self.check_goal_completion(idx)

    def check_goal_completion(self, idx):
        goal = self.goals[idx]
        if not goal['completed']:
            days_left = goal['days'] - len(goal['completed_days'])
            if days_left <= 0:
                goal['completed'] = True
                self.goal_listbox.delete(idx)
                self.goal_listbox.insert(idx, f"Cel {idx + 1}: {goal['name']} na {goal['days']} dni (Ukończony)")
                self.goal_listbox.itemconfig(idx, {'fg': 'green'})
                messagebox.showinfo("Cel ukończony", f"Cel '{goal['name']}' został ukończony!")

    def remove_goal(self, idx):
        del self.goals[idx]
        self.save_goals()
        self.update_goals_list()

    def edit_goal(self, idx):
        selected_goal = self.goals[idx]

        edit_window = Toplevel(self.master)
        edit_window.title(f"Edytuj cel: {selected_goal['name']}")
        edit_window.geometry("400x200")

        Label(edit_window, text="Nowa nazwa celu:", background='#FFFFFF').pack(anchor='w', padx=10)
        new_name_entry = Entry(edit_window)
        new_name_entry.pack(fill='x', padx=10, pady=(0, 10))
        new_name_entry.insert(END, selected_goal['name'])

        Label(edit_window, text="Nowa liczba dni:", background='#FFFFFF').pack(anchor='w', padx=10)
        new_days_entry = Entry(edit_window)
        new_days_entry.pack(fill='x', padx=10, pady=(0, 10))
        new_days_entry.insert(END, str(selected_goal['days']))

        save_button = DepthButton(edit_window, text="Zapisz zmiany", command=lambda: self.save_edited_goal(idx, new_name_entry.get(), new_days_entry.get()), **self.button_style)
        save_button.pack(pady=10)

    def save_edited_goal(self, idx, new_name, new_days):
        if new_name and new_days.isdigit():
            new_days = int(new_days)
            self.goals[idx]['name'] = new_name
            self.goals[idx]['days'] = new_days
            self.save_goals()
            self.update_goals_list()
            messagebox.showinfo("Zapisano zmiany", "Zaktualizowano dane celu.")
        else:
            messagebox.showwarning("Błąd", "Proszę wprowadzić poprawną nazwę celu i liczbę dni.")

    def save_goals(self):
        # Zapisywanie celów do pliku JSON
        with open("goals.json", "w") as file:
            json.dump(self.goals, file, indent=4)

    def load_goals(self):
        # Ładowanie celów z pliku JSON (jeśli istnieją)
        if os.path.exists("goals.json"):
            with open("goals.json", "r") as file:
                self.goals = json.load(file)

    def show_main_menu_and_close_window(self, window):
        window.destroy()
        self.master.deiconify()

    def show_help_content(self):
        messagebox.showinfo("Pomoc", "To jest ekran pomocy. Brak konkretnych informacji.")

    def show_author_content(self):
        messagebox.showinfo("Autor", "Autor: Twoje imię i nazwisko. Kontakt: Twój adres e-mail.")

if __name__ == "__main__":
    root = Tk()
    app = MainMenu(root)
    root.mainloop()
