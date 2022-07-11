from django.contrib import admin


from .models import Member, MemberType, Product, Status


@admin.register(MemberType)
class MemberTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'code']



@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['username', 'member_type', 'tmp_pass']
    
    
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
