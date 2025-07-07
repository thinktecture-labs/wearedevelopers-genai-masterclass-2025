using System.ComponentModel;
using Microsoft.SemanticKernel;

public class BookingPlugin
{
    [
        KernelFunction,
        Description(
            "Books a meeting slot for another employee at a given date for a given length of time."
        )
    ]
    public string BookSlot(
        [Description("The employee id of the person to book a slot for.")] int employeeId,
        [Description(
            "The title of the booking slot, Example: 'Meeting with John', 'Lunch with Customer'"
        )]
            string bookingReason,
        [Description(
            "The datetime when the slot should start, in ISO 8601 format. Example: 2021-09-01T10:00:00+02:00"
        )]
            string startDate,
        [Description("The length of the slot in minutes.")] int slotLength
    )
    {
        Console.WriteLine(
            $"BookSlot function called with parameters: {employeeId}, {bookingReason}, {startDate}, {slotLength}"
        );
        return $"Booked '{bookingReason}' slot for employee {employeeId} on {startDate} for {slotLength} minutes.";
    }
}
