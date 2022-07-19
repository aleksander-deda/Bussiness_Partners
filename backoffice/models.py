from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User
from partners.validators import validate_file_extension
from partners.models import Customer, Partner, PartnerProduct



CURRENCY = (('ALL', 'ALL'), 
            ('EURO', 'EURO'))



class Status(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(max_length= 255, null=False, blank=False)
    code = models.CharField(max_length= 255, null=False, blank=False)
    related_to = models.CharField(max_length=100, null=False, blank=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    class Meta:
            db_table='statuses'

    def __str__(self):
        return self.name


class Product(models.Model):
    origination_product_id = models.CharField(max_length=15, null=True, blank=True)
    product_name = models.CharField(max_length= 100, null=True, blank=True)
    product_code = models.CharField(max_length=30, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    min_value = models.FloatField(null=True, blank=True)
    max_value = models.FloatField(null=True, blank=True)
    deadline = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        db_table='products'

    def __str__(self):
        return self.product_name



class Prelead(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,null=True, blank=True)
    product = models.ForeignKey(PartnerProduct, on_delete=models.CASCADE,null=True, blank=True)
    applied_amount = models.DecimalField(max_digits= 10, decimal_places=3, null=True, blank=True)
    approved_amount = models.DecimalField(max_digits= 10, decimal_places=3, null=True, blank=True)
    currency = models.CharField(choices= CURRENCY, max_length=10, null=True, blank=True, default="ALL")
    loan_term = models.IntegerField(null=True, blank=True)
    monthly_loan = models.FloatField(null=True, blank=True)
    partner_contract = models.FileField(upload_to="file/partner_contracts/%Y/%m/%d/",validators=[validate_file_extension], null=True, blank=True)
    uw_contract = models.FileField(upload_to="file/uw_contracts/%Y/%m/%d/",validators=[validate_file_extension], null=True, blank=True)
    doc_1 = models.FileField(upload_to="file/additional_docs/%Y/%m/%d/",validators=[validate_file_extension], null=True, blank=True)
    doc_2 = models.FileField(upload_to="file/additional_docs/%Y/%m/%d/",validators=[validate_file_extension], null=True, blank=True)
    seller_name = models.CharField(max_length=60, null=True, blank=True)
    seller_phone = models.CharField(max_length=16, null=True, blank=True)
    partner_channel = models.CharField(max_length=15, null=True)
    contract_status = models.CharField(null=True, blank=True, max_length=20, default="Pending")
    application_status = models.CharField(null=True, blank=True, max_length=20, default="Pending")
    rejection_reason = models.CharField(max_length=256, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        db_table='preleads'

    def __str__(self):
        return str(self.id)
    
    
    
class MemberType(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(max_length=250, null=True, blank=True)
    code = models.CharField(max_length=80, unique=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        db_table='member_types'

    def __str__(self):
        return self.name



class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=200, null=False, blank=False, default="")
    member_type = models.ForeignKey(MemberType, on_delete=models.CASCADE)
    tmp_pass = models.CharField(max_length=200, null=False, blank=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    class Meta:
        db_table='members'

    def __str__(self):
        return self.username
    
    
    
class Segment(models.Model):
    title = models.CharField(max_length=64, default='Consumer Loan')
    code = models.IntegerField(default=21070)
    reference_data_id = models.IntegerField(default=1243)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    class Meta:
        db_table = 'segments'

    def __str__(self):
        return self.title
    
    
    
class District(models.Model):
    district_id = models.IntegerField(unique=True, null=False, blank=False)
    name =  models.CharField(max_length=100, null=False, blank=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, blank=True, null=True)
   
    class Meta:
        db_table='districts'

    def __str__(self):
        return self.name


class Branch(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    cocode = models.CharField(max_length=9, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
            db_table='branches'

    def __str__(self):
        return self.username




