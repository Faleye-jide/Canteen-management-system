# Generated by Django 3.2 on 2021-12-02 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Customer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='image',
            field=models.ImageField(upload_to='image/'),
        ),
    ]
