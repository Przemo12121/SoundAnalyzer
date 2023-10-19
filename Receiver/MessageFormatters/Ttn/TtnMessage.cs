namespace Receiver.MessageFormatters.Ttn;

public record TtnMessage(string DeviceId, string Payload);
