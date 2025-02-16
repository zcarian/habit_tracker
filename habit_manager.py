import json
from habit import Habit


class HabitManager:
    def __init__(self, dbFile='db.json'):
        self.dbFile = dbFile
        self.habits = self.load_from_file()

    def get_habit(self, name: str):
        """
        Returns the habit with the given name
        """
        for habit in self.habits:
            if habit.name == name:
                return habit

    def check_off_habit(self, name: str):
        """
        Checks off a habit and saves the changes
        """
        for habit in self.habits:
            if habit.name == name:
                habit.check_off()
                self.save_to_file()
                break

    def load_from_file(self):
        """
        Loads the habits from the file
        """
        try:
            with open(self.dbFile, 'r') as f:
                data = json.load(f)
                return [
                    Habit(
                        name=data['name'],
                        frequency=data['frequency'],
                        creationDate=data['creationDate'],
                        completionDates=data['completionDates']
                    )
                    for data in data['habits']
                ]
        except FileNotFoundError:
            return []

    def save_to_file(self):
        """
        Saves the habits to the file
        """
        habits_data = [
            {
                'name': habit.name,
                'frequency': habit.frequency,
                'creationDate': habit.creationDate,
                'completionDates': habit.completionDates
            }
            for habit in self.habits
        ]
        with open(self.dbFile, 'w') as f:
            json.dump({'habits': habits_data}, f, indent=4)

    def create_habit(self, name: str, frequency: str, creationDate: str = "", completionDates: list = []):
        """
        Creates a new habit
        """
        new_habit = Habit(
            name, frequency, creationDate, completionDates)
        self.habits.append(new_habit)
        self.save_to_file()

    def delete_habit(self, name: str):
        """
        Deletes a habit
        """
        for habit in self.habits:
            if habit.name == name:
                self.habits.remove(habit)
                self.save_to_file()
                break
