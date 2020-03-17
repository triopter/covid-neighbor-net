from django.conf import settings
from django.db import models

from neighbors.models import Address


STATUSES = Choices(
    # requested
    # claimed
    # completed
)


class Engagement(models.Model):
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='requested_engagements')
    submitted_at = models.DateTimeField(auto_now_add=True, blank=True)
    expires = models.DateTimeField(
        blank=True
    )  # allow entry, or if omitted, set automatically to N days after submission
    address = models.ForeignKey(Address, related_name='engagements')
    description = models.TextField()
    status = models.CharField(choices=STATUSES, max_length=20)
    claimed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='claimed_engagements', null=True, blank=True
    )
    claimed_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # @TODO: set expiration timestamp
        super().save(*args, **kwargs)
