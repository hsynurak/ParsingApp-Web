# Generated by Django 4.2.4 on 2024-09-24 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ParsingApp", "0011_rmkrskonutcs0301"),
    ]

    operations = [
        migrations.CreateModel(
            name="RMKRSKONUTCS0000",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Versiyon Numarası", models.CharField(max_length=255)),
                ("Üye Kodu", models.CharField(max_length=255)),
                ("Portföy Kodu", models.CharField(max_length=255)),
                ("Rezerve Alan", models.CharField(max_length=255)),
                ("Üye Adı", models.CharField(max_length=255)),
                ("Oluşturma Tarihi", models.CharField(max_length=255)),
                ("Bildirim Tarihi", models.CharField(max_length=255)),
                ("Rezerve Alan 2", models.CharField(max_length=255)),
            ],
        ),
    ]
