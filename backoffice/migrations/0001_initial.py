# Generated by Django 4.0.5 on 2022-07-07 22:27

from django.db import migrations, models
import django.db.models.deletion
import partners.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('cocode', models.CharField(blank=True, max_length=9, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_date', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'db_table': 'branches',
            },
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('district_id', models.IntegerField(unique=True)),
                ('name', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_date', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'db_table': 'districts',
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='', max_length=200)),
                ('tmp_pass', models.CharField(max_length=200)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_date', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'db_table': 'members',
            },
        ),
        migrations.CreateModel(
            name='MemberType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, max_length=250, null=True)),
                ('code', models.CharField(max_length=80, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_date', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'db_table': 'member_types',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origination_product_id', models.CharField(blank=True, max_length=15, null=True)),
                ('product_name', models.CharField(max_length=100)),
                ('product_code', models.CharField(max_length=30)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('min_value', models.FloatField(blank=True, null=True)),
                ('max_value', models.FloatField(blank=True, null=True)),
                ('deadline', models.IntegerField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_date', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'db_table': 'products',
            },
        ),
        migrations.CreateModel(
            name='Segment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Consumer Loan', max_length=64)),
                ('code', models.IntegerField(default=21070)),
                ('reference_data_id', models.IntegerField(default=1243)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_date', models.DateTimeField(auto_now=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'segments',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=255)),
                ('code', models.CharField(max_length=255)),
                ('related_to', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_date', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'db_table': 'statuses',
            },
        ),
        migrations.CreateModel(
            name='Prelead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('applied_amount', models.DecimalField(decimal_places=3, max_digits=10)),
                ('approved_amount', models.DecimalField(decimal_places=3, max_digits=10)),
                ('currency', models.CharField(choices=[('ALL', 'ALL'), ('EURO', 'EURO')], max_length=10)),
                ('loan_term', models.IntegerField()),
                ('partner_contract', models.FileField(upload_to='file/partner_contracts/%Y/%m/%d/', validators=[partners.validators.validate_file_extension])),
                ('uw_contract', models.FileField(upload_to='file/uw_contracts/%Y/%m/%d/', validators=[partners.validators.validate_file_extension])),
                ('doc_1', models.FileField(upload_to='file/additional_docs/%Y/%m/%d/', validators=[partners.validators.validate_file_extension])),
                ('doc_2', models.FileField(upload_to='file/additional_docs/%Y/%m/%d/', validators=[partners.validators.validate_file_extension])),
                ('seller_name', models.CharField(max_length=60)),
                ('seller_phone', models.CharField(max_length=16)),
                ('partner_channel', models.CharField(choices=[('WEB', 'WEB'), ('SHOP', 'SHOP')], max_length=10)),
                ('rejection_reason', models.CharField(blank=True, max_length=256, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_date', models.DateTimeField(auto_now=True, null=True)),
                ('application_status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='application_status', to='backoffice.status')),
                ('contract_status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contract_status', to='backoffice.status')),
            ],
            options={
                'db_table': 'preleads',
            },
        ),
    ]
