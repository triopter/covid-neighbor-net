import datetime
import pytz

from freezegun import freeze_time
from model_mommy import mommy

from django.conf import settings
from django.test import TestCase, override_settings
from django.utils import timezone

from engagements.models import Engagement


# @TODO: move into a testing utils module somewhere
def local_dt(*args, **kwargs):
    return timezone.localtime(
        datetime.datetime(*args, **kwargs).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
    )


@freeze_time('2020-03-18 16:43:00')
@override_settings(
    DEFAULT_ENGAGEMENT_EXPIRATION={'days': 3}
)  # regardless of how we configure the site, this test should still work
class EngagementTest(TestCase):
    def test_sets_correct_expiration_if_omitted(self):
        eng = mommy.make(Engagement, expires_at=None)
        self.assertEqual(local_dt(2020, 3, 21, 16, 43, 0), eng.expires_at)

    def test_does_not_override_existing_expiration(self):
        eng = mommy.make(Engagement, expires_at=local_dt(2020, 4, 12, 10, 7, 6))
        eng.refresh_from_db()
        self.assertEqual(local_dt(2020, 4, 12, 10, 7, 6), eng.expires_at)
