from django.contrib import admin
from partners.models import Customer, Partner, PartnerProduct, LoanConfig


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = [ 'name', 'nr_tel', 'nipt', 'member']


@admin.register(PartnerProduct)
class PartnerProductAdmin(admin.ModelAdmin):
    list_display = ['partner', 'product','start_date', 'end_date','is_active', 'is_deleted', 'created_date', 'updated_date']



@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'personal_id', 'id_card_doc','klauzole_doc', 'birthdate', 'status', 'consent_boa']


@admin.register(LoanConfig)
class LoanConfig(admin.ModelAdmin):
    list_display = [
        'product',
        'min_loan_term',
        'max_loan_term',
        'customer_interest',
        'partner_fee_without_bonus',
        'partner_fee_with_bonus',
        'application_commission',
        'bonus',
        'total_sum',
        ]