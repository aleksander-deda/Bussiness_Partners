# Generated by Django 4.0.5 on 2022-07-07 22:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('backoffice', '0001_initial'),
        ('accountmanagers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountmanager',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backoffice.member'),
        ),
    ]