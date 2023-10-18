﻿// <auto-generated />
using System;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Infrastructure;
using Microsoft.EntityFrameworkCore.Storage.ValueConversion;
using Npgsql.EntityFrameworkCore.PostgreSQL.Metadata;
using Receiver.Database;

#nullable disable

namespace Receiver.Database.Migrations
{
    [DbContext(typeof(SoundAnalyzerDbContext))]
    partial class SoundAnalyzerDbContextModelSnapshot : ModelSnapshot
    {
        protected override void BuildModel(ModelBuilder modelBuilder)
        {
#pragma warning disable 612, 618
            modelBuilder
                .HasAnnotation("ProductVersion", "7.0.12")
                .HasAnnotation("Relational:MaxIdentifierLength", 63);

            NpgsqlModelBuilderExtensions.UseIdentityByDefaultColumns(modelBuilder);

            modelBuilder.Entity("Receiver.Database.Models.DetectableClass", b =>
                {
                    b.Property<int>("Index")
                        .HasColumnType("integer");

                    b.Property<string>("Label")
                        .IsRequired()
                        .HasColumnType("text");

                    b.HasKey("Index");

                    b.ToTable("DetectableClasses", (string)null);

                    b.HasData(
                        new
                        {
                            Index = 0,
                            Label = "machine"
                        },
                        new
                        {
                            Index = 1,
                            Label = "silence"
                        },
                        new
                        {
                            Index = 2,
                            Label = "speech"
                        });
                });

            modelBuilder.Entity("Receiver.Database.Models.Device", b =>
                {
                    b.Property<int>("Id")
                        .ValueGeneratedOnAdd()
                        .HasColumnType("integer");

                    NpgsqlPropertyBuilderExtensions.UseIdentityByDefaultColumn(b.Property<int>("Id"));

                    b.Property<string>("TtnId")
                        .IsRequired()
                        .HasColumnType("text");

                    b.HasKey("Id");

                    b.HasIndex("TtnId")
                        .IsUnique();

                    b.ToTable("Devices", (string)null);
                });

            modelBuilder.Entity("Receiver.Database.Models.Notification", b =>
                {
                    b.Property<int>("Id")
                        .ValueGeneratedOnAdd()
                        .HasColumnType("integer");

                    NpgsqlPropertyBuilderExtensions.UseIdentityByDefaultColumn(b.Property<int>("Id"));

                    b.Property<int>("DetectableClassIndex")
                        .HasColumnType("integer");

                    b.Property<int>("DeviceId")
                        .HasColumnType("integer");

                    b.Property<DateTime>("SentAt")
                        .HasColumnType("timestamp with time zone");

                    b.HasKey("Id");

                    b.HasIndex("DetectableClassIndex");

                    b.HasIndex("DeviceId");

                    b.ToTable("Notifications", (string)null);
                });

            modelBuilder.Entity("Receiver.Database.Models.Notification", b =>
                {
                    b.HasOne("Receiver.Database.Models.DetectableClass", "DetectableClass")
                        .WithMany()
                        .HasForeignKey("DetectableClassIndex")
                        .OnDelete(DeleteBehavior.Cascade)
                        .IsRequired();

                    b.HasOne("Receiver.Database.Models.Device", "Device")
                        .WithMany("Notifications")
                        .HasForeignKey("DeviceId")
                        .OnDelete(DeleteBehavior.Cascade)
                        .IsRequired();

                    b.Navigation("DetectableClass");

                    b.Navigation("Device");
                });

            modelBuilder.Entity("Receiver.Database.Models.Device", b =>
                {
                    b.Navigation("Notifications");
                });
#pragma warning restore 612, 618
        }
    }
}