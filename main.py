import questionary
from habit_manager import HabitManager
from analyse import get_list_of_habits


def cli():
    print("Welcome to the Habit Tracker❕")
    stop = False
    manager = HabitManager()
    while not stop:

        choice = questionary.select(
            "What do you want to do?",
            choices=["Add new habit", "Check habit off", "Analyse", "Exit"]
        ).ask()

        if choice == "Add new habit":
            name = questionary.text("What's the name of the habit?").ask()
            frequency = questionary.select("What's the frequency of the habit?", choices=[
                                           "daily", "weekly", "monthly"]).ask()
            manager.create_habit(name, frequency)
            answer = questionary.confirm(
                "Do you want to check it off now?").ask()
            if answer:
                manager.check_off_habit(name)
            print(
                f"✅ Habit '{name}' with frequency '{frequency}' has been successfully created!")

        elif choice == "Check habit off":
            name = questionary.select(
                "What's the name of the habit?", choices=get_list_of_habits(manager.habits)).ask()
            manager.check_off_habit(name)
            print(f"✅ Habit '{name}' has been successfully checked off!")

        elif choice == "Exit":
            print("Goodbye! 👋")
            stop = True


if __name__ == "__main__":
    cli()
