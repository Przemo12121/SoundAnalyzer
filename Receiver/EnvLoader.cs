namespace Receiver;

public static class EnvLoader
{
    public static Dictionary<string, string> Load(string path)
        => File.ReadAllLines(path)
            .Select(line => line.Trim())
            .Where(line => line.Length > 0)
            .Where(line => line.First() != '#').Select(line => line.Split('='))
            .ToDictionary(str => str[0], str => str[1]);
}