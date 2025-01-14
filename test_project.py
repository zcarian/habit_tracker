import pytest
from datetime import datetime, timedelta
from habit import Habit
from habit_manager import HabitManager
from analyse import (
    get_list_of_habits,
    get_list_of_habits_by_frequency,
    get_longest_streak,
    get_longest_streak_by_frequency,
    get_completion_rate_of_habit,
)

import os


@pytest.fixture
def testManager():
    """Fixture to create a HabitManager with a temporary database."""
    # Use test_db.json as the temporary database
    testDbFile = "test_db.json"
    manager = HabitManager(dbFile=testDbFile)
    yield manager  # Provide the manager to tests
    # Cleanup: Remove the test_db.json file after the test
    if os.path.exists(testDbFile):
        os.remove(testDbFile)


# Test the Habit class
def test_habit_creation():

    habit = Habit(name="Exercise", frequency="daily",
                  creationDate="2025-01-01", completionDates=[])
    assert habit.name == "Exercise"
    assert habit.frequency == "daily"
    assert habit.creationDate == "2025-01-01"
    assert habit.completionDates == []


def test_habit_check_off():
    habit = Habit(name="Exercise", frequency="daily",
                  creationDate="2025-01-01", completionDates=[])
    habit.check_off()
    today = datetime.now().strftime("%Y-%m-%d")
    assert today in habit.completionDates


def test_habit_streak():
    habit = Habit(
        name="Exercise",
        frequency="daily",
        creationDate="2025-01-01",
        completionDates=["2025-01-01", "2025-01-02"],
    )
    assert habit.get_streak() == 2


# Test the HabitManager class
def test_habitManager_create_delete(testManager):
    testManager.create_habit(name="Read", frequency="daily")
    assert any(habit.name == "Read" for habit in testManager.habits)

    testManager.delete_habit(name="Read")
    assert not any(habit.name == "Read" for habit in testManager.habits)


def test_habitManager_persistence(testManager):
    testManager.create_habit(name="Sleep Early", frequency="daily")
    testManager.save_to_file()

    # Create a new HabitManager instance to validate loading
    new_manager = HabitManager(dbFile="test_db.json")
    assert any(habit.name == "Sleep Early" for habit in new_manager.habits)


# Test analytics functions
def test_analytics_list_of_habits(testManager):
    testManager.habits = []
    testManager.create_habit(name="Go for a walk", frequency="daily")
    testManager.create_habit(name="Read", frequency="weekly")
    assert get_list_of_habits(testManager.habits) == [
        "Go for a walk", "Read"]


def test_analytics_list_of_habits_by_frequency(testManager):
    testManager.habits = []
    testManager.create_habit(name="Go for a walk", frequency="daily")
    testManager.create_habit(name="Read", frequency="weekly")
    assert get_list_of_habits_by_frequency(testManager.habits, "daily") == [
        "Go for a walk"]
    assert get_list_of_habits_by_frequency(testManager.habits, "weekly") == [
        "Read"]


def test_analytics_longest_streak(testManager):
    testManager.habits = []
    testManager.create_habit(name="Exercise", frequency="daily", creationDate="2025-01-01",
                             completionDates=["2025-01-01", "2025-01-02", "2025-01-03"])
    testManager.create_habit(name="Brush teeth", frequency="daily", creationDate="2025-01-01",
                             completionDates=["2025-01-01", "2025-01-02", "2025-01-03", "2025-01-04"])
    assert get_longest_streak(testManager.habits) == (
        4, "Brush teeth", "daily")


def test_analytics_longest_streak_by_frequency(testManager):
    testManager.habits = []
    testManager.create_habit(name="Exercise", frequency="daily", creationDate="2025-01-01",
                             completionDates=["2025-01-01", "2025-01-02", "2025-01-03"])
    testManager.create_habit(name="Brush teeth", frequency="daily", creationDate="2025-01-01",
                             completionDates=["2025-01-01", "2025-01-02", "2025-01-03", "2025-01-04"])
    testManager.create_habit(name="Riding a bike", frequency="weekly", creationDate="2024-12-10",
                             completionDates=["2024-12-10", "2024-12-17", "2024-12-24", "2024-12-31", "2025-01-07"])
    assert get_longest_streak_by_frequency(
        testManager.habits, "daily") == (4, "Brush teeth")
    assert get_longest_streak_by_frequency(
        testManager.habits, "weekly") == (5, "Riding a bike")


def test_completion_rate(testManager):
    # Due to the fact that get_completion_rate_of_habit function measures from the acctual today date,
    # the habit "Dance" can't have static data and has to be measured from today
    testManager.habits = []
    twoDaysAgo = (datetime.now() - timedelta(days=2)
                  ).strftime("%Y-%m-%d")  # Date from 2 days ago
    oneDayAgo = (datetime.now() - timedelta(days=1)
                 ).strftime("%Y-%m-%d")  # Date from yesterday
    today = datetime.now().strftime("%Y-%m-%d")  # Today's date
    testManager.create_habit(name="Dance", frequency="daily", creationDate=twoDaysAgo,
                             completionDates=[oneDayAgo, today])
    rate = get_completion_rate_of_habit(testManager.habits, "Dance")
    # We have Danced on 2 days in the last 3 days so 66.67%
    assert rate == pytest.approx(66.67, 0.01)
