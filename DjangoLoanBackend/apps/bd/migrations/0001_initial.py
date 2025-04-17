from django.db import migrations, models
import uuid
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('branch', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BD',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(max_length=20)),
                ('employee_id', models.CharField(max_length=50, unique=True)),
                ('position', models.CharField(max_length=100)),
                ('hire_date', models.DateField()),
                ('is_active', models.BooleanField(default=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('linkedin_profile', models.URLField(blank=True, null=True)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='bd_profiles/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='bd_set', to='branch.branch')),
            ],
            options={
                'verbose_name': 'BD',
                'verbose_name_plural': 'BDs',
                'ordering': ['last_name', 'first_name'],
            },
        ),
    ]
