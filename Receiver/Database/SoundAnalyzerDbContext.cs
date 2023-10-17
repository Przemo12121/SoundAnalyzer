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
                .HasForeignKey(notification => notification.DetectableClassIndex);
        });

        Seed(modelBuilder, new [] { "machine", "silence", "speech" });
    }

    private static void Seed(ModelBuilder modelBuilder, IEnumerable<string> labels)
        => labels.Select((label, index) => new DetectableClass(index, label))
            .ToList()
            .ForEach(detectableClass => modelBuilder.Entity<DetectableClass>().HasData(detectableClass));
}