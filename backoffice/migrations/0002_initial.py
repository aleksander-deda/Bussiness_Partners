# Generated by Django 4.0.5 on 2022-07-07 22:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('partners', '0001_initial'),
        ('backoffice', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='prelead',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='partners.customer'),
        ),
        migrations.AddField(
            model_name='prelead',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='partners.partnerproduct'),
        ),
        migrations.AddField(
            model_name='member',
            name='member_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backoffice.membertype'),
        ),
        migrations.AddField(
            model_name='member',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
