from firebase import FirebaseApp
from errors import ErrorLogger

error_logger = ErrorLogger()

class Habit:
    def __init__(self, name):
        self.name = name
        self.dates_completed = []

    def mark_completed(self, date):
        self.dates_completed.append(date)

class Goal:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.habits = []

    def add_habit(self, habit):
        self.habits.append(habit)

class ApplicationLogic:
    def __init__(self):
        self.goals = []
        self.firebase_app = FirebaseApp()

    def add_goal(self, name, description):
        goal = Goal(name, description)
        self.goals.append(goal)
        self.firebase_app.add_goal(name, description)

    def get_goals(self):
        return self.firebase_app.get_goals()
