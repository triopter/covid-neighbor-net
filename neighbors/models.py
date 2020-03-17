from django.conf import settings
from django.contrib.gis.db import models as geo_models
from django.db import models


# We may want this data in fixtures or migrations to initially seed the DB
ROLES = [
    # Volunteer
    # Requester
    # Moderator
]


class Role(models.Model):
    name = models.CharField(
        max_length=50
    )  # It seems like in theory someone could switch between roles -- volunteer but eventually have to self-quarantine or vice-versa


class NeighborProfile(geo_models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile')
    given_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)  # blankable because elderly folks may not have one
    phone = models.CharField(
        max_length=50, blank=True
    )  # should this actually be blankable for privacy reasons?  Maybe require that the user provide at least one of email or phone?  Do we need to support multiple phone numbers per person?
    roles = models.ManyToManyField(Role, related_name='profiles')

    # @TODO: vulnerability level
    # @TODO: financial need


class Address(models.Model):
    owner = models.ForeignKey(
        NeighborProfile, related_name='addresses'
    )  # doing this  as a relation because a) then it's OK for volunteers to input a pin drop instead of an address, and b) it's conceivable that we'd want or need multiple addresses for someone

    # This is one part that's going to be a pain to internationalize while also supporting geocoding
    address_line_1 = models.CharField(max_length=100)
    address_line_2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100)
    state_or_province = models.ForeignKey(States)  # or call this 'region'?
    postal_code = models.CharField(max_length=30)

    lat = models.FloatField(
        blank=True, null=True
    )  # nullable so we can save an address even if we have trouble geocoding it
    lng = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # @TODO: geocode if not yet geocoded
        return super().save(*args, **kwargs)
