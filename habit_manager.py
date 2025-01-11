import json
from habit import Habit
from datetime import datetime


class HabitManager:
    def __init__(self, db_file='db.json'):
        self.db_file = db_file
        self.habits = self.load_from_file()

    def load_from_file(self):
        try:
            with open(self.db_file, 'r') as f:
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
        habits_data = [
            {
                'name': habit.name,
                'frequency': habit.frequency,
                'creationDate': habit.creationDate,
                'completionDates': habit.completionDates
            }
            for habit in self.habits
        ]
        with open(self.db_file, 'w') as f:
            json.dump({'habits': habits_data}, f, indent=4)

    def create_habit(self, name: str, frequency: str):
        new_habit = Habit(
            name, frequency, datetime.now().strftime('%Y-%m-%d'), [])
        self.habits.append(new_habit)
        self.save_to_file()

    def delete_habit(self, name: str):
        for habit in self.habits:
            if habit.name == name:
                self.habits.remove(habit)
                self.save_to_file()
                break

    def list_habits(self):
        return [habit.name for habit in self.habits]


manager = HabitManager()
print(manager.list_habits())


manager.delete_habit('Run')

print(manager.list_habits())
