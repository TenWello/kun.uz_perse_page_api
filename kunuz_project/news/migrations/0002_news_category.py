# Generated by Django 5.2.3 on 2025-06-22 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='category',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
