# Generated by Django 4.1.6 on 2023-06-18 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_activities_recipient'),
    ]

    operations = [
        migrations.AddField(
            model_name='students',
            name='image',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]
