# Generated by Django 3.0.4 on 2020-03-18 20:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('neighbors', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Engagement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('expires', models.DateTimeField(blank=True, help_text='If omitted, will be set to submission timestamp plus the value specified in settings.DEFAULT_ENGAGEMENT_EXPIRATION')),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('requested', 'Requested'), ('claimed', 'Claimed'), ('completed', 'Completed')], default='requested', max_length=20)),
                ('claimed_at', models.DateTimeField(blank=True, null=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='engagements', to='neighbors.Address')),
                ('claimed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='claimed_engagements', to=settings.AUTH_USER_MODEL)),
                ('requester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requested_engagements', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
