using System.Text;
using System.Text.Json;

namespace Receiver.MessageFormatters.Ttn;

public class TtnMessageFormatter : IMessageFormatter<TtnMessage>
{
    public TtnMessage Format(string message)
    {
        var deserialized = JsonSerializer.Deserialize<InternalTtnMessage>(message)!;
        var payload = Encoding.UTF8.GetString(Convert.FromBase64String(deserialized.uplink_message.frm_payload));
        var deviceId = deserialized.end_device_ids.device_id;

        return new(deviceId, payload);
    }
}