from django.db import models
import uuid
from django.utils import timezone
from django.conf import settings

class CustomAdminFilter(models.Model):
    uuid = models.UUIDField( primary_key = True, default =uuid.uuid4, editable = False)
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    model = models.CharField('Model', max_length=128)
    filters = models.JSONField('Filters', null=True, blank=True)
    searches = models.JSONField('Searches', null=True, blank=True)
    displays = models.JSONField('List Display', null=True, blank=True)
    link_fields = models.JSONField('List Display links', null=True, blank=True)
    date_hierarchy = models.CharField('Date Hierarchy', max_length=128, null=True, blank=True)
    list_per_page = models.IntegerField('List Per Page', default=50)
    order_by = models.CharField('Order By', max_length=128, null=True, blank=True)
    created_at = models.DateTimeField('created at', default=timezone.now)
    modified_at = models.DateTimeField('modified at', default=timezone.now)

    def __str__(self):
        return f"{self.admin.email} filter for model {self.model}"
    
    class Meta:
        verbose_name = "Custom Admin Filters"
        verbose_name_plural = "Custom Admins Filters" 


class CustomAdminFilter(models.Model):
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    model = models.CharField('Model', max_length=128)
    filters = models.JSONField('Filters', null=True, blank=True)
    searches = models.JSONField('Searches', null=True, blank=True)
    displays = models.JSONField('List Display', null=True, blank=True)
    link_fields = models.JSONField('List Display links', null=True, blank=True)
    date_hierarchy = models.CharField('Date Hierarchy', max_length=128, null=True, blank=True)
    list_per_page = models.IntegerField('List Per Page', default=50)
    order_by = models.CharField('Order By', max_length=128, null=True, blank=True)

    def __str__(self):
        return f"{self.admin.email} filter for model {self.model}"