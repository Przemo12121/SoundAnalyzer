using System.Text.RegularExpressions;
using Receiver.Database;
using Receiver.Database.Models;
using Receiver.MessageFormatters.Ttn;

namespace Receiver.MessageHandlers;

public partial class SoundAnalyzerMessageHandler
{
    private readonly SoundAnalyzerDbContext _dbContext;
    
    public SoundAnalyzerMessageHandler(SoundAnalyzerDbContext soundAnalyzerDbContext)
        => _dbContext = soundAnalyzerDbContext;

    public void Handle(TtnMessage message)
    {
        Verify(message);

        var device = _dbContext.Devices.FirstOrDefault(device => device.TtnId.Equals(message.DeviceId));
        if (device is null)
        {
            device = new Device(message.DeviceId);
            _dbContext.Devices.Add(device);
        }
        
        var notifications = ConvertToNotifications(message.Payload, device);
        _dbContext.Notifications.AddRange(notifications);
        _dbContext.SaveChanges();
    }

    private static void Verify(TtnMessage message)
    {
        var match = SoundAnalyzerMessageRegex().Match(message.Payload);
        if (match.Success is false)
        {
            throw new ArgumentException("Receiver message string not matching correct format.");
        }
    }

    private static List<Notification> ConvertToNotifications(string messagePayload, Device device)
    {
        var split = messagePayload.Split(':');
        
        var timestamp = DateTimeOffset.FromUnixTimeSeconds(Convert.ToInt64(split[1]))
            .ToUniversalTime().UtcDateTime;
        var notifications = split[0].Split(',')
            .Select(str => new Notification(Convert.ToInt32(str), timestamp, device))
            .ToList();
        
        return notifications;
    }

    [GeneratedRegex(@"^\d+(,\d+)+:\d+$")]
    private static partial Regex SoundAnalyzerMessageRegex();
}