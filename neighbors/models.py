from django.conf import settings
from django.contrib.gis.db import models as geo_models
from django.db import models
from django.utils.translation import gettext_lazy as _

# @TODO: we may eventually want to use Django-Cities or the like for this instead, but let's start simple
from localflavor.us.us_states import USPS_CHOICES
from localflavor.ca.ca_provinces import PROVINCE_CHOICES

# We may want this data in fixtures or migrations to initially seed the DB
ROLES = [
    # Volunteer
    # Requester
    # Dispatcher -- someone who accepts calls instead of emails from less tech-savvy participants
    # Moderator
]


class Role(models.Model):
    name = models.CharField(max_length=50)


class NeighborProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile'
    )
    given_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100, blank=True)
    email = models.EmailField(
        blank=True,
        help_text=_(
            "Required to create an account via front end, but allowed to be omitted by dispatchers creating requests on behalf of other neighbors"
        ),
    )
    phone = models.CharField(max_length=50, blank=True)
    roles = models.ManyToManyField(Role, related_name='profiles')

    # @TODO: vulnerability level
    # @TODO: financial need

    # @TDOD: verify that either email or phone is provided


class Address(geo_models.Model):
    owner = models.ForeignKey(NeighborProfile, on_delete=models.CASCADE, related_name='addresses')

    # @TODO: i18n-able version of this
    address_line_1 = models.CharField(max_length=100)
    address_line_2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100)
    region = models.CharField(
        max_length=100,
        choices=(USPS_CHOICES + PROVINCE_CHOICES),
        help_text=_("Starting with US State / Canadian province"),
    )
    postal_code = models.CharField(max_length=30)

    lng_lat = geo_models.PointField(
        geography=True, null=True, help_text=_("Note that longitude comes first")
    )  # nullable so we can store address even if we can't geocode it

    def save(self, *args, **kwargs):
        # @TODO: geocode if not yet geocoded
        return super().save(*args, **kwargs)
