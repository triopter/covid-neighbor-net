import datetime

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from neighbors.models import Address


class EngagementStatus(models.TextChoices):
    REQUESTED = ('requested', _('Requested'))
    CLAIMED = ('claimed', _('Claimed'))
    COMPLETED = ('completed', _('Completed'))


class Engagement(models.Model):
    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='requested_engagements'
    )
    submitted_at = models.DateTimeField(auto_now_add=True, blank=True)
    expires_at = models.DateTimeField(
        blank=True,
        help_text=_(
            "If omitted, will be set to time at creation plus the value specified in settings.DEFAULT_ENGAGEMENT_EXPIRATION",
        ),
    )
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='engagements')
    description = models.TextField()
    status = models.CharField(
        choices=EngagementStatus.choices, max_length=20, default=EngagementStatus.REQUESTED
    )
    claimed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='claimed_engagements',
    )
    claimed_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.expires_at is None:
            self.expires_at = (self.submitted_at or timezone.now()) + datetime.timedelta(
                **settings.DEFAULT_ENGAGEMENT_EXPIRATION
            )
        super().save(*args, **kwargs)
