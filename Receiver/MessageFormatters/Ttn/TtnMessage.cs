namespace Receiver.MessageFormatters.Ttn;

internal record TtnMessage
{
    public UplinkMessage uplink_message { get; set; } = null!;
}

internal record UplinkMessage
{
    public string frm_payload { get; set; } = null!;
}
