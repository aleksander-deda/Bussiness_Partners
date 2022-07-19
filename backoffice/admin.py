from django.contrib import admin


from .models import Member, MemberType, Product, Status, Prelead


@admin.register(MemberType)
class MemberTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'code']



@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['username', 'member_type', 'tmp_pass']
    
    
@admin.register(Prelead)
class PreleadAdmin(admin.ModelAdmin):
    list_display = [
        'customer',
        'product',
        'applied_amount',
        'approved_amount',
        'currency',
        'loan_term',
        'monthly_loan',
        'partner_contract',
        'uw_contract',
        'doc_1',
        'doc_2',
        'seller_name',
        'seller_phone',
        'partner_channel',
        'contract_status',
        'application_status',
        'rejection_reason',
    ]
    
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['origination_product_id',
                    'product_name',
                    'product_code',
                    'description',
                    'min_value',
                    'max_value',
                    'deadline',   
                    ]
    
@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ['name', 
                    'description', 
                    'code',
                    'related_to', 
                    ]
