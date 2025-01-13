import questionary
from habit_manager import HabitManager
from analyse import get_list_of_habits, get_list_of_habits_by_frequency, get_longest_streak, get_longest_streak_by_frequency, get_completion_rate_of_habit


def cli():
    print("Welcome to the Habit Tracker❕")
    stop = False
    manager = HabitManager()
    while not stop:

        choice = questionary.select(
            "What do you want to do?",
            choices=["Add new habit", "Delete old habit",
                     "Check habit off", "See habits", "Analyse", "Exit"]
        ).ask()

        if choice == "Add new habit":
            while True:
                name = questionary.text("What's the name of the habit?").ask()
                if name and name.strip():  # Check that name is not empty or just whitespace
                    break
                print("❌ The habit name cannot be empty. Please try again.")

            frequency = questionary.select("What's the frequency of the habit?", choices=[
                                           "daily", "weekly", "monthly"]).ask()
            manager.create_habit(name, frequency)
            answer = questionary.confirm(
                "Do you want to check it off now?").ask()
            if answer:
                manager.check_off_habit(name)
            print(
                f"✅ Habit '{name}' with frequency '{frequency}' has been successfully created!")

        elif choice == "Delete old habit":
            name = questionary.select(
                "What's the name of the habit?", choices=get_list_of_habits(manager.habits)).ask()
            manager.delete_habit(name)
            print(f"✅ Habit '{name}' has been successfully deleted!")

        elif choice == "Check habit off":
            name = questionary.select(
                "What's the name of the habit?", choices=get_list_of_habits(manager.habits)).ask()
            manager.check_off_habit(name)
            print(f"✅ Habit '{name}' has been successfully checked off!")

        elif choice == "See habits":
            seeHabitsChoice = questionary.select(
                "Which habits do you want to see?", choices=["Daily habits", "Weekly habits", "Monthly habits", "All habits"]).ask()

            if seeHabitsChoice == "Daily habits":
                habits = get_list_of_habits_by_frequency(
                    manager.habits, "daily")
                print(habits)

            elif seeHabitsChoice == "Weekly habits":
                habits = get_list_of_habits_by_frequency(
                    manager.habits, "weekly")
                print(habits)

            elif seeHabitsChoice == "Monthly habits":
                habits = get_list_of_habits_by_frequency(
                    manager.habits, "monthly")
                print(habits)

            elif seeHabitsChoice == "All habits":
                habits = get_list_of_habits(manager.habits)
                print(habits)

        elif choice == "Analyse":
            analyseChoice = questionary.select(
                "What do you want to do?", choices=["Analyse paricular habit", "Get longest streak"]).ask()

            if analyseChoice == "Analyse paricular habit":
                name = questionary.select(
                    "What's the name of the habit?", choices=get_list_of_habits(manager.habits)).ask()
                option = questionary.select(
                    "Chose action", choices=["Get longset streak", "Get completion rate"]).ask()

                if option == "Get longset streak":
                    habit = manager.get_habit(name)
                    streak = manager.get_habit(name).get_streak()
                    if habit.frequency == "daily":
                        unit = "days"
                    elif habit.frequency == "weekly":
                        unit = "weeks"
                    elif habit.frequency == "monthly":
                        unit = "months"
                    print(
                        f"✅ Habit '{name}' has a longest streak of {streak} {unit}!")

                elif option == "Get completion rate":
                    completion_rate = get_completion_rate_of_habit(
                        manager.habits, name)
                    print(
                        f"✅ Habit '{name}' has a completion rate of {completion_rate}%"
                    )

            elif analyseChoice == "Get longest streak":
                streakChoice = questionary.select(
                    "Chose action", choices=["Daily habits", "Weekly habits", "Monthly habits", "All habits"]).ask()

                if streakChoice == "Daily habits":
                    longest_streak, best_habit = get_longest_streak_by_frequency(
                        manager.habits, "daily")
                    print(
                        f"✅ The longest streak of daily habits is {longest_streak} days for habit '{best_habit}'!"
                    )

                elif streakChoice == "Weekly habits":
                    longest_streak, best_habit = get_longest_streak_by_frequency(
                        manager.habits, "weekly")
                    print(
                        f"✅ The longest streak of weekly habits is {longest_streak} days for habit '{best_habit}'!"
                    )

                elif streakChoice == "Monthly habits":
                    longest_streak, best_habit = get_longest_streak_by_frequency(
                        manager.habits, "monthly")
                    print(
                        f"✅ The longest streak of monthly habits is {longest_streak} days for habit '{best_habit}'!"
                    )

                elif streakChoice == "All habits":
                    longest_streak, best_habit = get_longest_streak(
                        manager.habits)
                    print(
                        f"✅ The longest streak of all habits is {longest_streak} days for habit '{best_habit}'!"
                    )

        elif choice == "Exit":
            print("Goodbye! 👋")
            stop = True


if __name__ == "__main__":
    cli()
    # manager = HabitManager()
    # print(get_completion_rate_of_habit(manager.habits, "Exercise"))
