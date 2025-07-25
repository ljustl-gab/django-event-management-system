# Generated by Django 4.2.7 on 2025-07-22 18:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('description', models.TextField(verbose_name='description')),
                ('date', models.DateField(verbose_name='date')),
                ('time', models.TimeField(verbose_name='time')),
                ('location', models.CharField(max_length=500, verbose_name='location')),
                ('max_participants', models.PositiveIntegerField(blank=True, help_text='Leave empty for unlimited participants', null=True, verbose_name='maximum participants')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
            ],
            options={
                'verbose_name': 'event',
                'verbose_name_plural': 'events',
                'db_table': 'events',
                'ordering': ['-date', '-time'],
            },
        ),
        migrations.CreateModel(
            name='EventParticipant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registered_at', models.DateTimeField(auto_now_add=True, verbose_name='registered at')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participants', to='events.event', verbose_name='event')),
            ],
            options={
                'verbose_name': 'event participant',
                'verbose_name_plural': 'event participants',
                'db_table': 'event_participants',
                'ordering': ['-registered_at'],
            },
        ),
    ]
