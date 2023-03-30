# Generated by Django 4.1.7 on 2023-03-30 06:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("authentication", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("userCategory", models.CharField(max_length=20)),
                ("conferenceCode", models.CharField(max_length=20)),
                ("userCountry", models.CharField(max_length=20)),
            ],
            options={
                "verbose_name": "UserProfile",
                "verbose_name_plural": "UserProfiles",
            },
        ),
    ]
