def book_slot(employee_id: int, booking_reason: str, start_date: str, slot_length: int) -> str:
    """Books a meeting slot for another employee at a given date for a given length of time.
    
    Args:
        employee_id: The employee id of the person to book a slot for
        booking_reason: The title of the booking slot, Example: 'Meeting with John', 'Lunch with Customer'
        start_date: The datetime when the slot should start, in ISO 8601 format. Example: 2021-09-01T10:00:00+02:00
        slot_length: The length of the slot in minutes
        
    Returns:
        A confirmation message for the booking
    """
    print(f"BookSlot function called with parameters: {employee_id}, {booking_reason}, {start_date}, {slot_length}")
    return f"Booked '{booking_reason}' slot for employee {employee_id} on {start_date} for {slot_length} minutes."
