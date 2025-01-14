from datetime import datetime, timedelta


def get_longest_streak(habits):
    """
    Get the habit with the longest streak among all habits.
    :param habits: A list of Habit objects
    :return: A tuple (longestStreak, habitName, frequencyOfBestHabit)
    """
    if not habits:
        print("❌ No habits available to evaluate streaks.")
        return 0

    longestStreak = 0
    bestHabit = None
    frequencyOfBestHabit = None
    for habit in habits:
        streak = habit.get_streak()
        if streak > longestStreak:
            longestStreak = streak
            bestHabit = habit.name
            frequencyOfBestHabit = habit.frequency
    return longestStreak, bestHabit, frequencyOfBestHabit


def get_longest_streak_by_frequency(habits, frequency):
    """
    Get the habit with the longest streak with a specific frequency.
    :param habits: A list of Habit objects
    :param frequency: The frequency to filter by
    :return: A tuple (longestStreak, habitName)
    """

    if not habits:
        print("❌ No habits available to evaluate streaks. ❌")
        return 0, None

    if frequency not in ["daily", "weekly", "monthly"]:
        print(
            f"❌ Invalid frequency '{frequency}'. Supported values are: daily, weekly, monthly. ❌")
        return 0, None

    longestStreak = 0
    bestHabit = None
    for habit in habits:
        if habit.frequency == frequency:
            streak = habit.get_streak()
            if streak > longestStreak:
                longestStreak = streak
                bestHabit = habit.name
    return longestStreak, bestHabit


def get_list_of_habits(habits):
    """
    Get a list of all habit names.
    :param habits: A list of Habit objects
    :return: A list of habit names
    """

    if not habits:
        print("❌ No habits available. ❌")
        return []

    return [habit.name for habit in habits]


def get_list_of_habits_by_frequency(habits, frequency):
    """
    Get a list of all habit names with a specific frequency.
    :param habits: A list of Habit objects
    :param frequency: The frequency to filter by
    :return: A list of habit names
    """

    if not habits:
        print("❌ No habits available. ❌")
        return []

    if frequency not in ["daily", "weekly", "monthly"]:
        print(
            f"❌ Invalid frequency '{frequency}'. Supported values are: daily, weekly, monthly. ❌")
        return []

    filteredHabits = [
        habit.name for habit in habits if habit.frequency == frequency]
    if not filteredHabits:
        print(f"❌ No habits with frequency '{frequency}' found. ❌")
        return []
    return filteredHabits


def get_completion_rate_of_habit(habits, habitName):
    """
    Get the completion rate of a specific habit based on whether it was completed
    at least once in each expected time period (week or month).
    :param habits: A list of Habit objects
    :param habitName: The name of the habit to evaluate
    :return: Float representing the completion rate
    """
    if not habits:
        print("❌ No habits available to evaluate. ❌")
        return 0.0

    # Find the habit
    habitToEvaluate = None
    for habit in habits:
        if habit.name == habitName:
            habitToEvaluate = habit
            break

    if not habitToEvaluate:
        print(f"❌ Habit '{habitName}' not found. ❌")
        return 0.0

    if not habitToEvaluate.completionDates:
        print(f"❌ Habit '{habitName}' hasn't been completed yet. ❌")
        return 0.0

    creationDate = datetime.strptime(habitToEvaluate.creationDate, '%Y-%m-%d')
    now = datetime.now()

    # Group completion dates into datetime objects
    completionDates = [
        datetime.strptime(date, '%Y-%m-%d') for date in habitToEvaluate.completionDates
    ]

    if habitToEvaluate.frequency == "daily":
        # Daily habits: Total days since creation
        # Adding 1 to include the current day
        totalPeriods = (now - creationDate).days + 1
        # Counting the number of completion dates
        completedPeriods = len(completionDates)

    elif habitToEvaluate.frequency == "weekly":
        # Weekly habits: Divide into weeks
        totalPeriods = (now - creationDate).days // 7 + 1
        # Adding 1 to include the current week
        completedPeriods = 0
        for weekStart in range(totalPeriods):
            # Adding 7 days to get the beginning of the week(for the first case it will be just creationDAte)
            beginningOfWeek = creationDate + timedelta(days=7 * weekStart)
            endOfWeek = creationDate + timedelta(days=7 * (weekStart + 1))

            if any(beginningOfWeek <= date < endOfWeek for date in completionDates):
                # If there is at least one completion date between the beginning of the week and the end of the week

                completedPeriods += 1

    elif habitToEvaluate.frequency == "monthly":
        # Same logic as in "weekly" but for monthly habits
        totalPeriods = (now - creationDate).days // 30 + 1

        completedPeriods = 0

        for monthStart in range(totalPeriods):
            beginningOfMonth = creationDate + timedelta(days=30 * monthStart)
            endOfMonth = creationDate + timedelta(days=30 * (monthStart + 1))

            if any(beginningOfMonth <= date < endOfMonth for date in completionDates):
                completedPeriods += 1

    else:
        print(
            f"❌ Invalid frequency '{habitToEvaluate.frequency}' for habit '{habitName}'! ❌")
        return 0.0

    # Calculate completion rate
    if totalPeriods == 0:
        print(f"❌ Habit '{habitName}' has no completion dates. ❌")
        return 0.0  # Avoid division by zero

    completionRate = (completedPeriods / totalPeriods) * 100
    return round(completionRate, 2)
