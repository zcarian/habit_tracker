# My habit tracker

## What is it?

This project is a Python-based backend for a habit tracking application. It allows users to:

- Define and manage habits with different periodicities (daily, weekly, monthly).
- Track completion of habits and analyze their progress.
- Get insights such as the longest streaks and completion rates for habits.

The application employs object-oriented and functional programming principles and includes a command-line interface (CLI) for user interaction.

## Features

1. **Habit Management**:

   - Create, delete, and manage habits.
   - Supports multiple frequencies (daily, weekly, monthly).

2. **Tracking**:

   - Mark habits as completed on the current day

3. **Analytics**:

   - View all habits or filter habits by frequency.
   - Analyze the longest streaks for all habits or specific ones.
   - Calculate the completion rate for each habit.

4. **Persistence**:

   - All data is stored in a JSON file (`db.json`) to ensure persistence between sessions.

5. **Testing**:
   - A comprehensive suite of unit tests ensures application reliability.

## Installation

### Prerequisites

- Python 3.7 or later.
- `pip` package manager.

### Setup

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```

## Usage

### CLI Commands

When you run the application, you'll be greeted with a menu allowing you to:

- **Add a new habit**: Specify the name and frequency.
- **Delete a habit**: Remove an existing habit.
- **Check off a habit**: Mark a habit as completed.
- **View habits**: List habits by frequency or view all habits.
- **Analyze habits**: Get detailed analytics about your habits.
- **Exit**: Quit the application.

## Testing

Unit tests are included to validate the application's functionality. Run the tests with:

```bash
pytest
```
