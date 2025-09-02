from datetime import date, timedelta

def get_tuesdays_of_year_to_now():
    """
    Returns a list of all Tuesdays from the first Tuesday of the current year
    up to the current date.
    """
    today = date.today()
    current_year = today.year

    # Find the first day of the current year
    first_day_of_year = date(current_year, 1, 1)

    # Calculate the offset to the first Tuesday of the year
    # weekday() returns 0 for Monday, 1 for Tuesday, ..., 6 for Sunday
    # We want the offset to Tuesday (1)
    offset = (1 - first_day_of_year.weekday() + 7) % 7
    first_tuesday_of_year = first_day_of_year + timedelta(days=offset)

    tuesdays = []
    current_tuesday = first_tuesday_of_year

    # Iterate through Tuesdays until the current date is reached
    while current_tuesday <= today:
        tuesdays.append(current_tuesday)
        current_tuesday += timedelta(weeks=1) # Move to the next Tuesday

    return tuesdays

