from django.shortcuts import render, redirect
from .models import Customer, Partner, PartnerProduct, LoanConfig
from backoffice.models import Prelead, Member, Product
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.views.generic import UpdateView
from .forms import PartnerForm, UserForm
from django.contrib.auth import get_user_model

User = get_user_model()


# @login_required(login_url='login')
def partner_dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'partners/partner_dashboard.html')
    else:
        return redirect('login')
    


class MyProfile( DetailView):
    model = Partner
    context_object_name = 'partner'
    template_name = 'partners/partner_profile.html'
    
    def get_object(self):
        user = User.objects.get(id=self.request.user.id)
        member = Member.objects.filter(user_id=user).first()
        partner = Partner.objects.filter(member_id=member).first()
        return partner
    
    
    
class ProfileUpdate(UpdateView):
    model = Partner
    form_class = PartnerForm
    user_form_class = UserForm
   
    # context_object_name = 'partner'
    success_url = reverse_lazy('my-profile')

    def get_object(self):
        user = User.objects.get(id=self.request.user.id)
        member = Member.objects.filter(user_id=user.id).first()
        partner = Partner.objects.filter(member_id=member.id).first()
        
        return partner
    
    def get_context_data(self, **kwargs):
        context = super(ProfileUpdate, self).get_context_data(**kwargs)        
        context['users'] = User.objects.all()
        context['member'] = context['users'].filter(username=self.request.user.username).first()
        print(context['member'])
       
        
        # context['user'] = context['users'].filter(id=self.request.user.id, is_active=True)
        
        # context['users'] = User.objects.get(id=self.request.user.id)
        
        
        return context


    

class CustomerList( ListView):
    model = Customer
    context_object_name = 'customers'               
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(id=self.request.user.id)
        member = Member.objects.filter(user_id=user).first()
        partner = Partner.objects.filter(member_id=member).first()
        context['customers'] = context['customers'].filter(partner_id=partner, is_active=True)
        # context['count'] = context['customers'].filter( is_active=True).count()
        
        # search_input = self.request.GET.get('search-area') or ''
        # if search_input:
        #     context['tasks'] = context['tasks'].filter(
        #         title__startswith=search_input)
        # context['search_input'] = search_input
        
        return context         





# def customers_list(request, id):
#     customers = Customer.objects.filter(partner=id).order_by('first_name')
#     context = {
#         'customers': customers,
#     }
#     return render(request, 'partners/customers_list.html', context)


def new_application(request):
    user = User.objects.get(id=request.user.id)
    member = Member.objects.filter(user_id=user).first()
    partner = Partner.objects.filter(member_id=member, is_active=True).first()
    print('partner ', partner)
    # partner_products = PartnerProduct.objects.filter(partner_id=2, is_active=True).first()
    partner_products = PartnerProduct.objects.filter(partner_id=partner.id, is_active=True).first()
    products = PartnerProduct.objects.filter(partner_id=partner.id, is_active=True)
    print('partner_products ', partner_products)
    
    loan_month = 0.0
    total = 0.0
    
    context = {
        'products': products,
    }
    
    
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        personal_id = request.POST.get('personal_id')
        id_card_doc = request.FILES['id_card_doc']
        klauzole_doc = request.FILES['klauzole_doc']
        birthdate = request.POST.get('birthdate')
        mobile = request.POST.get('mobile')
        seller_name = request.POST.get('seller_name')
        seller_phone = request.POST.get('seller_phone')
        selected_product = request.POST.get('product_id')
        applied_amount = float(request.POST.get('applied_amount'))
        loan_term = float(request.POST.get('loan_term'))
        loan_confirm = request.POST.get('loan_confirm')
        
        print("Selected Produvt: ", selected_product)
        
        
        context_1 = {
            'loan_month': loan_month,
            'total': total,
            'first_name': first_name,
            'last_name': last_name,
            'personal_id': personal_id,
            'id_card_doc': id_card_doc,
            'klauzole_doc': klauzole_doc,
            'birthdate': birthdate,
            'mobile': mobile,
            'seller_name': seller_name,
            'seller_phone': seller_phone,
            'selected_product': selected_product,
            'applied_amount': applied_amount,
            'loan_term': loan_term,
            'loan_confirm': loan_confirm,
        }
        
        if first_name is not None and last_name is not None and personal_id is not None and id_card_doc is not None and klauzole_doc is not None and birthdate is not None and mobile is not None:
            customer = Customer(partner=partner, first_name=first_name, last_name=last_name, personal_id=personal_id,
                                    id_card_doc=id_card_doc, klauzole_doc=klauzole_doc, birthdate=birthdate, mobile=mobile)
            print('customer ', customer)
            customer.save()
            
        
            if seller_name is not None and seller_phone is not None and selected_product is not None and applied_amount is not None and loan_term is not None:
                loan_config = LoanConfig.objects.filter(product_id=selected_product, min_loan_term__lte=loan_term, max_loan_term__gte=loan_term).first()
                print("loan_config: ", loan_config)
                if loan_config is not None:
                    interest = float(loan_config.customer_interest)
                    fee = float(loan_config.partner_fee_without_bonus)
                    total = float(applied_amount + applied_amount*interest + applied_amount*fee)
                    print(total)
                    
                    loan_month = float(total/loan_term)
                    print(loan_month)
                    
                    if loan_confirm is True:
                    
                        prelead = Prelead(customer_id=customer.id, product_id=partner_products.id, 
                                        seller_name=seller_name, seller_phone=seller_phone, applied_amount=applied_amount, 
                                        approved_amount=total, monthly_loan=loan_month, loan_term=loan_term)
                        prelead.save()
                        return redirect('customers-list')
                    # else:
                    #     return redirect ('new-application')
                    
                else:
                    print("No loan config!!!")
        
           
    return render(request, 'partners/new_application_customer_details.html', context)

    
    
