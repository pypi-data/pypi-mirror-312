from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Outbox',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                (
                    'method',
                    models.CharField(
                        choices=[
                            ('publish', 'Publish'),
                            ('broadcast', 'Broadcast'),
                            ('subscribe', 'Subscribe'),
                            ('unsubscribe', 'Unsubscribe'),
                            ('disconnect', 'Disconnect'),
                            ('refresh', 'Refresh'),
                            ('presence', 'Presence'),
                            ('presence_stats', 'Presence Stats'),
                            ('history', 'History'),
                            ('history_remove', 'History Remove'),
                            ('channels', 'Channels'),
                            ('info', 'Info'),
                        ],
                        default='publish',
                        max_length=14,
                        verbose_name='Method',
                    ),
                ),
                ('payload', models.JSONField(verbose_name='Payload')),
                ('partition', models.BigIntegerField(default=0, verbose_name='Partition')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
            ],
            options={
                'verbose_name': 'Outbox',
                'verbose_name_plural': 'Outboxes',
            },
        ),
    ]
