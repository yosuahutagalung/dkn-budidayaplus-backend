# Generated by Django 5.1.1 on 2024-09-28 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pond', '0003_alter_pond_image_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pond',
            name='image_name',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]