from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=10, unique=True)),
                ('address_line1', models.CharField(max_length=255)),
                ('address_line2', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('postal_code', models.CharField(max_length=20)),
                ('country', models.CharField(default='Australia', max_length=100)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('is_active', models.BooleanField(default=True)),
                ('manager_name', models.CharField(blank=True, max_length=255, null=True)),
                ('manager_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('manager_phone', models.CharField(blank=True, max_length=20, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Branch',
                'verbose_name_plural': 'Branches',
                'ordering': ['name'],
            },
        ),
    ]
