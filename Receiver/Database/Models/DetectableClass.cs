namespace Receiver.Database.Models;

public class DetectableClass
{
    public string Label { get; init; }
    public int Index { get; init; }
    
    public DetectableClass(int index, string label)
        => (Index, Label) = (index, label);
}