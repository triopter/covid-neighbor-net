from model_mommy import mommy

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

from neighbors.models import Role, NeighborProfile, Country, Address
from engagements.models import EngagementStatus, Engagement


class RequesterRegistrationTest(TestCase):
    fixtures = ['roles.json']

    # @TODO: test options other than the happy path
    def test_registration_creates_objects_and_redirects(self):
        User = get_user_model()

        self.assertEqual(0, User.objects.count())
        self.assertEqual(0, NeighborProfile.objects.count())
        self.assertEqual(0, Address.objects.count())
        self.assertEqual(0, Engagement.objects.count())

        url = reverse('register_and_create_engagement')
        data = {
            'description': 'Bring me groceries, yo!',
            'address_line_1': '500 Broadway',
            'address_line_2': '',
            'city': 'New York',
            'region': 'NY',
            'postal_code': '10011',
            'country': Country.USA,
            'given_name': 'Mickey',
            'surname': 'Mouse',
            'email': 'mickey@example.com',
            'phone': '212-867-5309',
            'password': 's3kr1t',
            'terms': True,
        }

        response = self.client.post(url, data)

        self.assertEqual(1, User.objects.count())
        self.assertEqual(1, NeighborProfile.objects.count())
        self.assertEqual(1, Address.objects.count())
        self.assertEqual(1, Engagement.objects.count())

        engagement = Engagement.objects.all().first()
        self.assertEqual(engagement.status, EngagementStatus.REQUESTED)
        self.assertIn(Role.objects.get(name='Requester'), engagement.requester.profile.roles.all())

        self.assertRedirects(
            response, reverse('create_engagement_thanks', kwargs={'engagement_id': engagement.id})
        )
