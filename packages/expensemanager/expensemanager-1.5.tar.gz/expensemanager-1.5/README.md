README.md file with the provided content

readme_content = """
# ExpenseManager Library

## Overview
ExpenseManager is a Python library designed to simplify expense management in group activities, such as trips or events. 
It provides an intuitive interface to split expenses among participants, calculate balances, and generate balance summaries.

This library is tailored for applications like **Travel Budget Management Systems**, where shared expense tracking is essential.

---

## Features
1. **Split Expenses**:
   - Dynamically split expenses among participants.
   - Supports equal or custom splits.

2. **Balance Calculation**:
   - Calculate how much each participant owes or is owed.

3. **Summary Generation**:
   - Generate a detailed summary of participant balances.

4. **Integration**:
   - Easy to integrate into Django or other Python-based projects.

---

## Installation
Install the library using pip:

```bash
pip install expensemanager
```

# Usage Example for `ExpenseManager` Library

## Scenario:
A group of three friends — **Alice**, **Bob**, and **Charlie** — are on a weekend trip. During the trip:
1. **Alice** pays $100 for groceries.
2. **Bob** pays $150 for accommodation.
3. The expense for both items needs to be split equally among all three participants.

The `ExpenseManager` library will help track these expenses and calculate the balances for each participant.

---

## 1. Setup the Trip and Participants

Assume you already have a `Trip` model and participants linked to it.

```python
from django.contrib.auth.models import User
from travel_budget.models import Trip

```
# Create users
``` python
alice = User.objects.create(username="Alice")
bob = User.objects.create(username="Bob")
charlie = User.objects.create(username="Charlie")
```
# Create a trip and add participants
``` python
trip = Trip.objects.create(trip_name="Weekend Getaway", start_date="2024-12-01", end_date="2024-12-03", user=alice)
trip.participants.add(alice, bob, charlie)

```

Use the ExpenseManager to Split Expenses
Use the ExpenseManager library to record the expenses and update balances.

```python

from expensemanager.expensemanager import ExpenseManager

```

# Initialize the ExpenseManager for the trip
manager = ExpenseManager(trip)

# Alice pays $100 for groceries
manager.split_expense(payer=alice, amount=100)

# Bob pays $150 for accommodation
manager.split_expense(payer=bob, amount=150)

# Retrieve balances
balances = manager.get_balances()

print(balances)


Expected Output:

The balances after splitting expenses equally among the three participants will be:


{
    "Alice": 50.0,    # Alice is owed $50.00
    "Bob": 100.0,     # Bob is owed $100.00
    "Charlie": -150.0 # Charlie owes $150.00
}


4. Generate a Human-Readable Summary

Use the generate_balance_summary method to display a detailed summary.

``` python 

summary = manager.generate_balance_summary()
print(summary)

```


5. Pay a Balance

Charlie decides to pay $100 to Bob. You can record this transaction in your system and update the balances accordingly.

from travel_budget.models import Payment

``` python
# Create a payment record
Payment.objects.create(trip=trip, paid_by=charlie, paid_to=bob, amount=100)

# Update balances in the ExpenseManager (if integrated with payment processing)
manager.split_expense(payer=charlie, amount=100, split_among=[bob])

```

Benefits of This Use Case:

    Simplifies Expense Management: Automatically calculates and updates balances for participants.
    Handles Real-World Scenarios: Supports equal and custom splits.
    Integrates Seamlessly with Django: Works with Django models for trips, users, and payments.




