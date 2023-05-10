# Generated by Django 4.1.7 on 2023-05-07 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conference',
            name='conferenceName',
            field=models.CharField(default='adminConference', max_length=100),
        ),
        migrations.AlterField(
            model_name='paper',
            name='paperTitle',
            field=models.CharField(max_length=200),
        ),
    ]