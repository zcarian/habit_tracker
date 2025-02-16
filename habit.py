from datetime import datetime, timedelta


class Habit:
    def __init__(self, name: str, frequency: str, creationDate: str, completionDates: list):
        """
        :param name: The name of the habit
        :param frequency: The frequency of the habit eg. daily, weekly, monthly
        :param creationDate: The date the habit was created
        :param completionDates: The dates the habit was completed
        """
        self.name = name
        self.frequency = frequency
        self.creationDate = creationDate or datetime.now().strftime('%Y-%m-%d')
        self.completionDates = completionDates or []

    def check_off(self):
        """
        Adds the current date to the list of completion dates
        """
        currentDate = datetime.now().strftime(
            '%Y-%m-%d')  # Changing the format from timedate object to string
        if currentDate not in self.completionDates:
            # Adding the current date to the list
            self.completionDates.append(currentDate)

    def get_streak(self):
        """
        Returns the longest streak of the habit
        """
        if not self.completionDates:
            return 0
        else:
            sortedDates = sorted(datetime.strptime(date, '%Y-%m-%d')
                                 for date in self.completionDates)  # Converting the list of strings to a list of datetime objects and sorting

            streak = 1  # If completionDates is not empty then there is a minimum of 1 streak
            maxStreak = 1

            frequency_map = {
                'daily': timedelta(days=1),
                'weekly': timedelta(weeks=1),
                'monthly': timedelta(days=31)  # Approximation for a month
            }

            interval = frequency_map.get(self.frequency)

            for i in range(1, len(sortedDates)):
                # Check if the difference between the current date and the previous date is less than or equal to the interval
                if sortedDates[i] - sortedDates[i - 1] <= interval:
                    streak += 1
                    maxStreak = max(maxStreak, streak)
                else:
                    streak = 1

            return maxStreak
