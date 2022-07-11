from django.db import models
from django.db.models.deletion import CASCADE
from backoffice.models import Member



class UnderWriter(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True, null=False)
    is_deleted = models.BooleanField(default=False, null=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        db_table='underwriters'

    
    def __str__(self):
        return self.name