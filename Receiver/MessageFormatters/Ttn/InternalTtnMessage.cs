namespace Receiver.MessageFormatters.Ttn;

internal record InternalTtnMessage
{
    public UplinkMessage uplink_message { get; set; } = null!;
    public EndDeviceIds end_device_ids { get; set; } = null!;
}

internal record UplinkMessage
{
    public string frm_payload { get; set; } = null!;
}

internal record EndDeviceIds
{
    public string device_id { get; set; } = null!;
}
