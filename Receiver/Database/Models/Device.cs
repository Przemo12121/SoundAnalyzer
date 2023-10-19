namespace Receiver.Database.Models;

public class Device
{
    public int Id { get; set; }
    public string TtnId { get; set; }
    public List<Notification> Notifications { get; set; } = null!;

    public Device(string ttnId)
        => TtnId = ttnId;
}