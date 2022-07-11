from django.db import models

from django.db import models
from django.db.models.deletion import CASCADE
from backoffice.models import Member


class SuperEasyPay(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        db_table='supereasypays'

    
    def __str__(self):
        return self.name




