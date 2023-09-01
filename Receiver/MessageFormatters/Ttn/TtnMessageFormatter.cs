using System.Text;
using System.Text.Json;

namespace Receiver.MessageFormatters.Ttn;

public class TtnMessageFormatter : IMessageFormatter<string>
{
    public string Format(string message)
    {
        var str = JsonSerializer.Deserialize<TtnMessage>(message)!
            .uplink_message.frm_payload;

        return Encoding.UTF8.GetString(Convert.FromBase64String(str));
    }
}