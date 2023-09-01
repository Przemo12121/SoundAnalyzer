namespace Receiver.MessageFormatters;

public interface IMessageFormatter<T>
{
    T Format(string message);
}