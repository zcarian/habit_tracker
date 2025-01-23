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
    # Testing creation of a habit
    habit = Habit(name="Exercise", frequency="daily",
                  creationDate="2025-01-01", completionDates=[])
    assert habit.name == "Exercise"
    assert habit.frequency == "daily"
    assert habit.creationDate == "2025-01-01"
    assert habit.completionDates == []


def test_habit_check_off():
    # Testing check_off method
    habit = Habit(name="Exercise", frequency="daily",
                  creationDate="2025-01-01", completionDates=[])
    habit.check_off()
    today = datetime.now().strftime("%Y-%m-%d")
    assert today in habit.completionDates


def test_habit_streak():
    # Testing get_streak method
    manager = HabitManager("db.json")
    habit = manager.get_habit("Exercise")
    assert habit.get_streak() == 20


# Test the HabitManager class
def test_habitManager_create_delete(testManager):
    # Testing create_habit and delete_habit methods
    testManager.create_habit(name="Read", frequency="daily")
    assert any(habit.name == "Read" for habit in testManager.habits)

    testManager.delete_habit(name="Read")
    assert not any(habit.name == "Read" for habit in testManager.habits)


def test_habitManager_persistence(testManager):
    # Testing persistence
    testManager.create_habit(name="Sleep Early", frequency="daily")
    testManager.save_to_file()

    # Create a new HabitManager instance to validate loading
    new_manager = HabitManager(dbFile="test_db.json")
    assert any(habit.name == "Sleep Early" for habit in new_manager.habits)


# Test analytics functions
def test_analytics_list_of_habits(testManager):
    # Testing get_list_of_habits function
    testManager.create_habit(name="Go for a walk", frequency="daily")
    testManager.create_habit(name="Read", frequency="weekly")
    assert get_list_of_habits(testManager.habits) == [
        "Go for a walk", "Read"]


def test_analytics_list_of_habits_by_frequency(testManager):
    # Testing get_list_of_habits_by_frequency function
    testManager.create_habit(name="Go for a walk", frequency="daily")
    testManager.create_habit(name="Read", frequency="weekly")
    assert get_list_of_habits_by_frequency(testManager.habits, "daily") == [
        "Go for a walk"]
    assert get_list_of_habits_by_frequency(testManager.habits, "weekly") == [
        "Read"]


def test_analytics_longest_streak():
    # Testing get_longest_streak function
    manager = HabitManager("db.json")
    assert get_longest_streak(manager.habits) == (20, "Exercise", "daily")


def test_analytics_longest_streak_by_frequency():
    # Testing get_longest_streak_by_frequency function
    manager = HabitManager("db.json")
    assert get_longest_streak_by_frequency(
        manager.habits, "daily") == (20, "Exercise")
    assert get_longest_streak_by_frequency(
        manager.habits, "weekly") == (5, "Go hiking")
    assert get_longest_streak_by_frequency(
        manager.habits, "monthly") == (7, "Budget review")


def test_completion_rate(testManager):
    # Testing get_completion_rate_of_habit function
    # Due to the fact that get_completion_rate_of_habit function measures from the acctual today date,
    # the habit "Dance" cannot have static data and has to be measured from today
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
