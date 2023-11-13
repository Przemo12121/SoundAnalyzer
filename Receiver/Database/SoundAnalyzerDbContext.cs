using Microsoft.EntityFrameworkCore;
using Receiver.Database.Models;

namespace Receiver.Database;

public class SoundAnalyzerDbContext : DbContext
{
    public DbSet<DetectableClass> DetectableClasses { get; set; } = null!;
    public DbSet<Notification> Notifications { get; set; } = null!;
    public DbSet<Device> Devices { get; set; } = null!;
    
    public SoundAnalyzerDbContext(DbContextOptions<SoundAnalyzerDbContext> dbContextOptions) : base(dbContextOptions) {}

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Device>(model =>
        {
            model.ToTable("Devices");

            model.Property(device => device.TtnId)
                .IsRequired();

            model.HasIndex(device => device.TtnId)
                .IsUnique();
        });
        
        modelBuilder.Entity<Notification>(model =>
        {
            model.ToTable("Notifications");

            model.Property(notification => notification.SentAt)
                .IsRequired();
            
            model.Property(notification => notification.DetectableClassIndex)
                .IsRequired();
        });

        modelBuilder.Entity<DetectableClass>(model =>
        {
            model.ToTable("DetectableClasses");

            model.Property(detectableClass => detectableClass.Index)
                .IsRequired()
                .ValueGeneratedNever();
            model.Property(detectableClass => detectableClass.Label)
                .IsRequired();

            model.HasKey(detectableClass => detectableClass.Index);

            model.HasMany<Notification>()
                .WithOne(notification => notification.DetectableClass)
                .HasForeignKey(notification => notification.DetectableClassIndex)
                .IsRequired();
        });

        Seed(modelBuilder, new [] { "clapping", "machine", "silence", "speech", "whistling" });
    }

    private static void Seed(ModelBuilder modelBuilder, IEnumerable<string> labels)
        => labels.Select((label, index) => new DetectableClass(index, label))
            .ToList()
            .ForEach(detectableClass => modelBuilder.Entity<DetectableClass>().HasData(detectableClass));
}