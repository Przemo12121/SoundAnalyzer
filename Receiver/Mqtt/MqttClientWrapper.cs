using MQTTnet;
using MQTTnet.Client;

namespace Receiver.Mqtt;

public sealed class MqttClientWrapper : IClient, IDisposable
{
    private readonly IMqttClient _client;
    private readonly MqttClientOptions _clientOptions;
    private readonly MqttClientSubscribeOptions _subscriptionOptions;
    private readonly MqttClientDisconnectOptions _disconnectOptions;
    
    public MqttClientWrapper(
        string username,
        string password,
        string clientId,
        string uri,
        int port,
        string subscriptionTopic, 
        Func<MqttApplicationMessageReceivedEventArgs, Task> messageHandler)
    {
        _clientOptions = new MqttClientOptionsBuilder()
            .WithTcpServer(uri, port)
            .WithTls()
            .WithCredentials(username, password)
            .WithClientId(clientId)
            .WithCleanSession(false)
            .Build();
        
        _subscriptionOptions = new MqttFactory().CreateSubscribeOptionsBuilder()
            .WithTopicFilter(filter => filter.WithTopic(subscriptionTopic))
            .Build();
        
        _disconnectOptions = new MqttClientDisconnectOptionsBuilder()
            .WithReason(MqttClientDisconnectOptionsReason.NormalDisconnection)
            .Build();
        
        _client = new MqttFactory().CreateMqttClient();

        _client.ApplicationMessageReceivedAsync += messageHandler;
    }

    public async Task ConnectAsync()
    {
        Console.WriteLine("Connecting...");
        await _client.ConnectAsync(_clientOptions);
        Console.WriteLine("Connection established");
        
        await _client.SubscribeAsync(_subscriptionOptions);
        Console.WriteLine("Subscription established");
    }

    public async Task DisconnectAsync()
    {
        Console.WriteLine("Disconnecting...");
        await _client.DisconnectAsync(_disconnectOptions);
        Console.WriteLine("Disconnected");
    }

    public async void Dispose()
    {
        if (_client.IsConnected)
        {
            await _client.TryDisconnectAsync();
        }
        
        _client.Dispose();
    }
}