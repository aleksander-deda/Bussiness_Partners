# Generated by Django 4.0.5 on 2022-07-19 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backoffice', '0008_alter_prelead_currency_alter_prelead_doc_1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prelead',
            name='application_status',
            field=models.CharField(blank=True, default='Pending', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='prelead',
            name='contract_status',
            field=models.CharField(blank=True, default='Pending', max_length=20, null=True),
        ),
    ]
