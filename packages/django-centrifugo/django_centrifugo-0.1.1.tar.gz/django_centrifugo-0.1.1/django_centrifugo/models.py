from django.db import models


class Outbox(models.Model):
    """See https://centrifugal.dev/docs/server/consumers#postgresql-outbox-consumer"""

    class Method(models.TextChoices):
        PUBLISH = 'publish'
        BROADCAST = 'broadcast'
        SUBSCRIBE = 'subscribe'
        UNSUBSCRIBE = 'unsubscribe'
        DISCONNECT = 'disconnect'
        REFRESH = 'refresh'
        PRESENCE = 'presence'
        PRESENCE_STATS = 'presence_stats'
        HISTORY = 'history'
        HISTORY_REMOVE = 'history_remove'
        CHANNELS = 'channels'
        INFO = 'info'
        # BATCH = 'batch'  # not supported

    method = models.CharField('Method', max_length=14, choices=Method.choices, default=Method.PUBLISH)
    payload = models.JSONField('Payload')
    partition = models.BigIntegerField('Partition', default=0)
    created_at = models.DateTimeField('Created at', auto_now_add=True)

    class Meta:
        verbose_name = 'Outbox'
        verbose_name_plural = 'Outboxes'
