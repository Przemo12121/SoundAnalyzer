namespace Receiver.Database.Models;

public class Notification
{
    public int DetectableClass { get; init; }
    public DateTime SentAt { get; init; }

    public Notification(int detectableClass, DateTime dateTime)
        => (DetectableClass, SentAt) = (detectableClass, dateTime);
}