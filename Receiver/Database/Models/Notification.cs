namespace Receiver.Database.Models;

public class Notification
{
    public int Id { get; set; }
    public int DetectableClassIndex { get; }
    public DetectableClass DetectableClass { get; private set; }
    public DateTime SentAt { get; }

    
    public Notification(int detectableClassIndex, DateTime sentAt)
        => (DetectableClassIndex, SentAt) = (detectableClassIndex, sentAt);
}