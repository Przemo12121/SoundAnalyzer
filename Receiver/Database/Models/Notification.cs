namespace Receiver.Database.Models;

public class Notification
{
    public int Id { get; set; }
    public int DetectableClassIndex { get; }
    public DetectableClass DetectableClass { get; private set; }
    public DateTime SentAt { get; }

    public Device Device { get; set; }
    
    public Notification(int detectableClassIndex, DateTime sentAt)
        => (DetectableClassIndex, SentAt) = (detectableClassIndex, sentAt);
    
    public Notification(int detectableClassIndex, DateTime sentAt, Device device)
        => (DetectableClassIndex, Device, SentAt) = (detectableClassIndex, device, sentAt);
}