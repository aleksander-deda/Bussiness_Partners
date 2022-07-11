# Generated by Django 4.0.5 on 2022-07-08 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='loanconfig',
            name='bonus',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='loanconfig',
            name='interest',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='loanconfig',
            name='total_sum',
            field=models.FloatField(blank=True, null=True),
        ),
    ]