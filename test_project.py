import json
from habit import Habit

# Load habits from JSON


def load_habits_from_json(filename):
    """
    Load habits from a JSON file and create Habit objects.
    :param filename: The JSON file containing habit data
    :return: A list of Habit objects
    """
    with open(filename, 'r') as file:
        data = json.load(file)
        return [
            Habit(
                name=item["name"],
                frequency=item["frequency"],
                creationDate=item["creationDate"],
                completionDates=item["completionDates"],
            )
            for item in data["habits"]
        ]

# Test streaks for each habit


def test_habit_streaks(habits):
    """
    Test the streak function for each habit.
    :param habits: A list of Habit objects
    """
    for habit in habits:
        streak = habit.getStreak()
        print(
            f"Habit: {habit.name}, Frequency: {habit.frequency}, Longest Streak: {streak}")


# Main script
# if __name__ == "__main__":
#     habits = load_habits_from_json('db.json')  # Load data from JSON file
#     test_habit_streaks(habits)  # Test streak function
