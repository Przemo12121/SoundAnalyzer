using Microsoft.EntityFrameworkCore;
using MQTTnet;
using Receiver;
using Receiver.Database;
using Receiver.MessageFormatters.Ttn;
using Receiver.MessageHandlers;
using Receiver.Mqtt;

var environment = EnvLoader.Load();
var dbConnectionString =
    $"Username={environment["DATABASE_USER"]};" +
    $"Password={environment["DATABASE_PASSWORD"]};" +
    $"Host={environment["DATABASE_HOST"]};" +
    $"Database={environment["DATABASE_NAME"]};";

var messageFormatter = new TtnMessageFormatter();
var dbContext = new SoundAnalyzerDbContext(
    new DbContextOptionsBuilder<SoundAnalyzerDbContext>()
        .UseNpgsql(dbConnectionString)
    .Options);
dbContext.Database.Migrate();

var messageHandler = new SoundAnalyzerMessageHandler(dbContext);
MqttClientWrapper client = new(
    $"{environment["TTN_USERNAME"]}@ttn",
    environment["TTN_PASSWORD"],
    environment["TTN_CLIENT_ID"],
    environment["TTN_URI"], 
    Convert.ToInt32(environment["TTN_PORT"]),
    environment["TTN_SUBSCRIPTION_TOPIC"],
    eventArgs =>
    {
        try
        {
            var jsonMessage = eventArgs.ApplicationMessage.ConvertPayloadToString()!;
            var message = messageFormatter.Format(jsonMessage); 
            messageHandler.Handle(message);
        }
        catch (Exception exception)
        {
            Console.WriteLine(exception);   
        }
        
        return Task.CompletedTask;
    });
    
await client.ConnectAsync();

Console.CancelKeyPress += async delegate
{
    await client.DisconnectAsync();
};

while (true) { }