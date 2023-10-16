using Microsoft.EntityFrameworkCore;
using Receiver.Database.Models;

namespace Receiver.Database;

public class SoundAnalyzerDbContext : DbContext
{
    public DbSet<DetectableClass> DetectableClasses { get; set; } = null!;
    public DbSet<Notification> Notifications { get; set; } = null!;
    
    public SoundAnalyzerDbContext(DbContextOptions<SoundAnalyzerDbContext> dbContextOptions) : base(dbContextOptions) {}

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Notification>(model =>
        {
            model.ToTable("Notifications");
            // model.B
        });

        modelBuilder.Entity<DetectableClass>(model =>
        {
            model.ToTable("DetectableClasses");
            model.HasMany<Notification>();
        });
        // TODO
    }
}