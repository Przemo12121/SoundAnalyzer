using Microsoft.EntityFrameworkCore;
using MQTTnet;
using Receiver;
using Receiver.Database;
using Receiver.MessageFormatters.Ttn;
using Receiver.MessageHandlers;
using Receiver.Mqtt;

var environmentalVariables = EnvLoader.Load(
    Path.Combine(Directory.GetCurrentDirectory(), ".env"));

var dbConnectionString =
    $"Username={environmentalVariables["DATABASE_USER"]};" +
    $"Password={environmentalVariables["DATABASE_PASSWORD"]};" +
    $"Host=localhost:{environmentalVariables["DATABASE_PORT"]};" +
    $"Database={environmentalVariables["DATABASE_NAME"]}";

var messageFormatter = new TtnMessageFormatter();
var dbContext = new SoundAnalyzerDbContext(
    new DbContextOptionsBuilder<SoundAnalyzerDbContext>()
        .UseNpgsql(dbConnectionString)
    .Options);
var messageHandler = new SoundAnalyzerMessageHandler(dbContext);

MqttClientWrapper client = new(
    environmentalVariables["TTN_USERNAME"],
    environmentalVariables["TTN_PASSWORD"],
    environmentalVariables["TTN_CLIENT_ID"],
    environmentalVariables["TTN_URI"], 
    Convert.ToInt32(environmentalVariables["TTN_PORT"]),
    environmentalVariables["TTN_SUBSCRIPTION_TOPIC"],
    eventArgs =>
    {
        var jsonMessage = eventArgs.ApplicationMessage.ConvertPayloadToString()!;
        var message = messageFormatter.Format(jsonMessage); 
        messageHandler.Handle(message);        
        
        return Task.CompletedTask;
    });
    
await client.ConnectAsync();

Console.CancelKeyPress += async delegate
{
    await client.DisconnectAsync();
};

while (true) { }