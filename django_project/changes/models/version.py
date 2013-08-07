import os
import logging
logger = logging.getLogger(__name__)
from django.conf.global_settings import MEDIA_ROOT
from django.db import models
from audited_models.models import AuditedModel
from .entry import Entry


class ApprovedVersionManager(models.Manager):
    """Custom version manager that shows only approved records."""

    def get_query_set(self):
        """Query set generator"""
        return super(
            ApprovedVersionManager, self).get_query_set().filter(
                approved=True)


class UnapprovedVersionManager(models.Manager):
    """Custom version manager that shows only unapproved records."""

    def get_query_set(self):
        """Query set generator"""
        return super(
            UnapprovedVersionManager, self).get_query_set().filter(
                approved=False)


class Version(AuditedModel):
    """A version model that the changelog is associated with.."""
    name = models.CharField(
        help_text='Name of this release e.g. 1.0.1.',
        max_length=255,
        null=False,
        blank=False,
        unique=False)

    approved = models.BooleanField(
        help_text=(
            'Whether this version has been approved for use by the '
            'project owner.'),
        default=False)

    image_file = models.ImageField(
        help_text='An optional logo image for this version.',
        upload_to=os.path.join(MEDIA_ROOT, 'images/projects'),
        blank=True)

    project = models.ForeignKey('Project')

    objects = ApprovedVersionManager()
    all_objects = models.Manager()
    unapproved_objects = UnapprovedVersionManager()

    class Meta:
        """Meta options for the version class."""
        unique_together = ('name', 'project')
        app_label = 'changes'

    def __unicode__(self):
        return u'%s : %s' % (self.project.name, self.name)

    def entries(self):
        """Get the entries for this version."""
        qs = Entry.objects.filter(version=self).order_by('category')
        return qs
