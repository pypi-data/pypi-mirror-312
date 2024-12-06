from django.contrib import admin

from django_centrifugo.models import Outbox


@admin.register(Outbox)
class OutboxAdmin(admin.ModelAdmin): ...
