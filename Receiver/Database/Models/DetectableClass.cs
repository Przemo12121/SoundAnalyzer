namespace Receiver.Database.Models;

public class DetectableClass
{
    public string Label { get; }
    public int Index { get; }
    
    public DetectableClass(int index, string label)
        => (Index, Label) = (index, label);
}