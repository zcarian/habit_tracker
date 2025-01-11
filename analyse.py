def get_longest_streak(habits):
    """
    Get the habit with the longest streak among all habits.
    :param habits: A list of Habit objects
    :return: A tuple (longest_streak, habit_name)
    """
    longest_streak = 0
    best_habit = None
    for habit in habits:
        streak = habit.getStreak()
        if streak > longest_streak:
            longest_streak = streak
            best_habit = habit.name
    return longest_streak, best_habit


def get_longest_streak_by_frequency(habits, frequency):
    """
    Get the habit with the longest streak with a specific frequency.
    :param habits: A list of Habit objects
    :param frequency: The frequency to filter by
    :return: A tuple (longest_streak, habit_name)
    """
    longest_streak = 0
    best_habit = None
    for habit in habits:
        if habit.frequency == frequency:
            streak = habit.getStreak()
            if streak > longest_streak:
                longest_streak = streak
                best_habit = habit.name
    return longest_streak, best_habit


def get_list_of_habits(habits):
    """
    Get a list of all habit names.
    :param habits: A list of Habit objects
    :return: A list of habit names
    """
    return [habit.name for habit in habits]


def get_list_of_habits_by_frequency(habits, frequency):
    """
    Get a list of all habit names with a specific frequency.
    :param habits: A list of Habit objects
    :param frequency: The frequency to filter by
    :return: A list of habit names
    """
    return [habit.name for habit in habits if habit.frequency == frequency]
