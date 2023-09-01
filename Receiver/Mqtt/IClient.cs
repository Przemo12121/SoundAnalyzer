namespace Receiver.Mqtt;

public interface IClient
{
    Task ConnectAsync();
    Task DisconnectAsync();
}