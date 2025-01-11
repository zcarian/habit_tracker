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
        self.creationDate = datetime.now().strftime('%Y-%m-%d')
        self.completionDates = completionDates

    def checkOff(self):
        """
        Adds the current date to the list of completion dates
        """
        currentDate = datetime.now().strftime(
            '%Y-%m-%d')  # Changing the format from timedate object to string
        if currentDate not in self.completionDates:
            self.completionDates.append(currentDate)

    def getStreak(self):
        if not self.completionDates:
            return 0
        else:
            sortedDates = sorted(datetime.strptime(date, '%Y-%m-%d')
                                 for date in self.completionDates)

            streak = 1  # If completionDates is not empty then there is a minimum of 1 streak
            maxStreak = 1

            frequency_map = {
                'daily': timedelta(days=1),
                'weekly': timedelta(weeks=1),
                'monthly': timedelta(days=30)  # Approximation for a month
            }

            interval = frequency_map.get(self.frequency)

            print(interval)
            for i in range(1, len(sortedDates)):
                if sortedDates[i] - sortedDates[i - 1] <= interval:
                    streak += 1
                    maxStreak = max(maxStreak, streak)
                else:
                    streak = 1

            return maxStreak


# date = datetime.now().strftime('%Y-%m-%d')
# print(date)
# print(type(date))
newHabit1 = Habit('Run', 'daily', "2024-12-10", [
    "2024-12-10", "2024-12-11", "2024-12-12", "2024-12-13", "2024-12-15"
])

newHabit2 = Habit('Read', 'weekly', "2024-12-10", [
    "2024-12-10", "2024-12-17", "2024-12-30", "2024-12-31", "2025-01-05",
])
print(newHabit2.getStreak())
