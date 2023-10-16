using System.Text.RegularExpressions;
using Receiver.Database;
using Receiver.Database.Models;

namespace Receiver.MessageHandlers;

public partial class SoundAnalyzerMessageHandler
{
    private readonly SoundAnalyzerDbContext _dbContext;

    public SoundAnalyzerMessageHandler(SoundAnalyzerDbContext soundAnalyzerDbContext)
        => _dbContext = soundAnalyzerDbContext;

    public void Handle(string message)
    {
        Verify(message);
        var notifications = ConvertToEntities(message);
        _dbContext.Notifications.AddRange(notifications);
    }

    private static void Verify(string message)
    {
        var match = SoundAnalyzerMessageRegex().Match(message);
        if (match.Success is false)
        {
            throw new ArgumentException("Receiver message string not matching correct format.");
        }
    }

    private static List<Notification> ConvertToEntities(string message)
    {
        var split = message.Split(':');
        
        var timestamp = DateTimeOffset.FromUnixTimeSeconds(Convert.ToInt64(split[1]))
            .ToUniversalTime().UtcDateTime;
        var notifications = split[0].Split(',')
            .Select(str => new Notification(Convert.ToInt32(str), timestamp))
            .ToList();
        
        return notifications;
    }

    [GeneratedRegex(@"^(\d+(,\d+)?)+:\d+$")]
    private static partial Regex SoundAnalyzerMessageRegex();
}