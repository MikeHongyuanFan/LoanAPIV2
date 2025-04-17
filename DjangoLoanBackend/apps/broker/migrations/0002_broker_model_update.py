from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0001_initial'),
        ('bd', '0001_initial'),
        ('broker', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BrokerSpecialization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='BrokerTier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('commission_multiplier', models.DecimalField(decimal_places=2, default=1.0, max_digits=5)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='brokercommission',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='brokercommission',
            name='payment_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='brokercommission',
            name='payment_reference',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='commissionpayment',
            name='broker',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='broker.broker'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='commissionpayment',
            name='payment_method',
            field=models.CharField(choices=[('BANK_TRANSFER', 'Bank Transfer'), ('CHECK', 'Check'), ('CREDIT_CARD', 'Credit Card'), ('OTHER', 'Other')], default='BANK_TRANSFER', max_length=20),
        ),
        migrations.AddField(
            model_name='commissionpayment',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='commissionpaymentitem',
            name='amount_paid',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='broker',
            name='accreditation_expiry',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='broker',
            name='accreditation_number',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='broker',
            name='bd',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='brokers', to='bd.bd'),
        ),
        migrations.AddField(
            model_name='broker',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='broker',
            name='branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='brokers', to='branch.branch'),
        ),
        migrations.AddField(
            model_name='broker',
            name='linkedin_profile',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='broker',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='broker_profiles/'),
        ),
        migrations.AddField(
            model_name='broker',
            name='tier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='brokers', to='broker.brokertier'),
        ),
        migrations.AddField(
            model_name='broker',
            name='website',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='broker',
            name='years_of_experience',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='broker',
            name='specializations',
            field=models.ManyToManyField(blank=True, related_name='brokers', to='broker.brokerspecialization'),
        ),
    ]
