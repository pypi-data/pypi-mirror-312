from django.test import TestCase

from django_centrifugo.models import Outbox


class OutboxTest(TestCase):
    def test_outbox(self):
        event = Outbox.objects.create(payload={'channel': 'test', 'data': {}})
        self.assertTrue(event.id > 0)
