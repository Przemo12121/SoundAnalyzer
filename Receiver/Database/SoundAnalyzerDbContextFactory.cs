using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Design;

namespace Receiver.Database;

// Only used for dotnet ef tools
file class SoundAnalyzerDbContextFactory : IDesignTimeDbContextFactory<SoundAnalyzerDbContext>
{
    private readonly string _connectionString;

    public SoundAnalyzerDbContextFactory()
    {
        var environment = EnvLoader.Load();
        
        _connectionString =
            $"Username={environment["DATABASE_USER"]};" +
            $"Password={environment["DATABASE_PASSWORD"]};" +
            $"Host={environment["DATABASE_HOST"]};" +
            $"Database={environment["DATABASE_NAME"]};";
    } 

    public SoundAnalyzerDbContext CreateDbContext(string[] args)
        => new(
            new DbContextOptionsBuilder<SoundAnalyzerDbContext>()
                .UseNpgsql(_connectionString)
                .Options);
}