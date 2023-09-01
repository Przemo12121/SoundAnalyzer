using MQTTnet;
using Receiver.MessageFormatters.Ttn;
using Receiver.Mqtt;

var x = new TtnMessageFormatter();

MqttClientWrapper client = new(
    "sound-analyzer-eng-degree@ttn",
    "test",
    "sound-analyzer-eng-degree",
    "eu1.cloud.thethings.network", 
    8883,
    "v3/+/devices/+/up",
    eventArgs =>
    {
        var msg = eventArgs.ApplicationMessage.ConvertPayloadToString();
        
        Console.WriteLine($"Message received: {x.Format(msg)}");
        return Task.CompletedTask;
    });
    
await client.ConnectAsync();

Console.CancelKeyPress += async delegate
{
    await client.DisconnectAsync();
};

while (true) { }