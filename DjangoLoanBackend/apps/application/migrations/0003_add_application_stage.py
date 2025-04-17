# Generated manually

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='stage',
            field=models.CharField(choices=[('ENQUIRY', 'Enquiry'), ('INDICATIVE_OFFER', 'Indicative Offer'), ('VALUATION', 'Valuation'), ('DUAL', 'Dual'), ('FORMAL_APPROVAL', 'Formal Approval'), ('LOAN_DOCS_ISSUED', 'Loan Documents Issued'), ('LOAN_DOCS_RETURN', 'Loan Documents Return'), ('SETTLEMENT', 'Settlement'), ('REJECT', 'Reject'), ('WITHDRAWAL', 'Withdrawal')], default='ENQUIRY', max_length=30),
        ),
        migrations.AddField(
            model_name='application',
            name='stage_changed_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='application',
            name='valuer_info',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='qs_info',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]
