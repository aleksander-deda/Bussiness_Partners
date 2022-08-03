# Generated by Django 4.0.5 on 2022-08-03 11:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0004_rename_partner_fee_loanconfig_partner_fee_without_bonus_and_more'),
        ('backoffice', '0010_alter_prelead_partner_channel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prelead',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='partners.partnerproduct'),
        ),
    ]