from django.db import models
from django.db.models.deletion import CASCADE
from .validators import validate_file_extension



class Partner(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    personal_id = models.CharField(max_length=10, null=False, blank=False)
    nr_tel = models.CharField(max_length=16, null=False, blank=False)
    nipt = models.CharField(max_length=12, null=False, blank=False, unique=True)
    member = models.ForeignKey('backoffice.Member', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    class Meta:
        db_table='partners'

    
    def __str__(self):
        return self.name
    
    
    
class PartnerProduct(models.Model):
    partner = models.ForeignKey('partners.Partner', on_delete=models.CASCADE)
    product = models.ForeignKey('backoffice.Product', on_delete=models.CASCADE)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True, blank=True)
    is_deleted = models.BooleanField(default=False, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    is_assigned = models.BooleanField(default=True)
    
    class Meta:
        db_table='partner_products'


    def __str__(self):
        return str(self.id)
    


class LoanConfig(models.Model):
    product = models.ForeignKey('backoffice.Product', on_delete=models.CASCADE)
    min_loan_term = models.IntegerField(null=True, blank=True)
    max_loan_term = models.IntegerField(null=True, blank=True)
    customer_interest = models.FloatField(null=True, blank=True)
    partner_fee_without_bonus = models.FloatField(null=True, blank=True)
    partner_fee_with_bonus = models.FloatField(default=0, null=True, blank=True)
    application_commission = models.FloatField(null=True, blank=True)
    bonus = models.FloatField(null=True, blank=True)
    total_sum = models.FloatField(null=True, blank=True)
    is_active = models.BooleanField(default=True, blank=True)
    is_deleted = models.BooleanField(default=False, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    class Meta:
        db_table='loan_configs'


    def __str__(self):
        return str(self.id)


class Customer(models.Model):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=128, null=False, blank=False)
    last_name = models.CharField(max_length=128, null=False, blank=False)
    personal_id = models.CharField(max_length=11, null=False, blank=False)
    id_card_doc = models.FileField(upload_to="file/id_cards/%Y/%m/%d/",validators=[validate_file_extension], null=False, blank=False, )
    klauzole_doc = models.FileField(upload_to="file/clausoles/%Y/%m/%d/" ,validators=[validate_file_extension], null=False, blank=False)
    birthdate = models.DateField()
    mobile = models.CharField(max_length=16)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    changed_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    is_active = models.BooleanField(default=True, blank=True)
    status = models.CharField(max_length=50)
    consent_boa = models.CharField(max_length=10)
    
    class Meta:
        db_table='customers'

    
    def __str__(self):
        return self.first_name + " " + self.last_name


