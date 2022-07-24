from django.shortcuts import render, redirect
from partners.models import Partner, PartnerProduct
from underwriters.models import UnderWriter
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy, reverse
from backoffice.models import Member, MemberType, Product
from .models import AccountManager
from django.contrib.auth.models import User
import random, string
from django.contrib import messages 
import json
import datetime
# from django.contrib.auth.decorators import login_required


def generate_random_password(length):
    str = "".join(random.choice(string.ascii_letters) for i in range(length))
    return str



# @login_required(login_url='login')
def account_manager_dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'accountmanagers/account_manager_dashboard.html')
    else:
        return redirect('login')
    

class MyProfile( DetailView):
    model = AccountManager
    context_object_name = 'accountmanager'
    template_name = 'accountmanagers/account_manager_profile.html'
    
    def get_object(self):
        user = User.objects.get(id=self.request.user.id)
        member = Member.objects.filter(user_id=user).first()
        account_manager = AccountManager.objects.filter(member_id=member).first()
        return account_manager  
    
 
   
def add_partner(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['name']
        last_name = request.POST['surname']
        email = request.POST['email']
        
                
        if username is None or username == "":
            messages.error(request, 'Username nuk mund te jete bosh!')
        elif password is None or password =="":
            messages.error(request, 'Passwordi nuk mund te jete bosh!')
        elif email is None or email =="":
            messages.error(request, 'Email nuk mund te jete bosh!')
        else:
            user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
            
            if user is not None:
                member = Member.objects.create(username=username, tmp_pass=generate_random_password(8), member_type=MemberType.objects.get(code="partner"), user=user)
                                
                if member is not None:
                    name = request.POST['name']
                    personal_id = request.POST['personal_id']
                    nr_tel = request.POST['phone']
                    nipt = request.POST['nipt']
                    
                    if name is None or name == "":
                        messages.error(request, 'Emri i partnerit nuk mund te jete bosh!')
                    elif personal_id  is None or personal_id =="":
                        messages.error(request, 'Numri personal nuk mund te jete bosh!')
                    elif nr_tel  is None or nr_tel =="":
                        messages.error(request, 'Numri i Telefonit nuk mund te jete bosh!')
                    elif nipt  is None or nipt =="":
                        messages.error(request, 'Nipti nuk mund te jete bosh!')  
                    else:
                        Partner.objects.create(name=name, personal_id=personal_id, nr_tel=nr_tel, nipt=nipt, member=member)
                        return redirect('partners-list')
                        messages.success(request, 'Partneri u regjistrua me sukses !')
                else:
                    messages.error(request, 'Partneri nuk mund te regjistrohet!')
            else:
                messages.error(request, 'Partneri nuk mund te regjistrohet!')
    
    return render(request, 'accountmanagers/create_partner.html')   



def underwriters(request):
    underwriters = UnderWriter.objects.all().order_by('name')
    context = {
        'underwriters': underwriters
    }
    return render(request, 'accountmanagers/underwriters_list.html', context)



def partners(request):
    partners = Partner.objects.all().order_by('name')
    context = {
        'partners': partners
    }
    return render(request, 'accountmanagers/partners_list.html', context)



def validate_products(end_date):
    # today = datetime.datetime.today().now().strftime('%Y-%m-%d %H:%M:%S')
    today = datetime.datetime.strftime(datetime.datetime.today().now(), '%Y-%m-%d %H:%M:%S') 
    
    if end_date < today:
        return True
    return False


def add_products_to_partners(request, id):    
    partner = Partner.objects.filter(id=id, is_active=True).first()
    products = Product.objects.filter(is_active=True).order_by("product_name")
    partner_products = PartnerProduct.objects.filter(partner_id=id, is_active=True)
    
    
    for assigned_products in partner_products:       
        current_end_date = datetime.datetime.strftime(assigned_products.end_date, '%Y-%m-%d %H:%M:%S')
        current_id = assigned_products.id
        print("current_id: " ,current_id) 
        expire_validation = validate_products(current_end_date)
        if expire_validation == True:
            PartnerProduct.objects.filter(id=current_id).delete()

    partner_product_list = []
    index = 0
    
    for product in products:
        index += 1    
        product_id = product.id
        partner_product_obj = PartnerProduct.objects.filter(partner_id=id, product=product_id).first()
        
        if partner_product_obj is not None:
            start_date = partner_product_obj.start_date.strftime('%Y-%m-%d %H:%M:%S')
            end_date = partner_product_obj.end_date.strftime('%Y-%m-%d %H:%M:%S')
            print(end_date)
            is_assigned = json.dumps(partner_product_obj.is_assigned)
            
        else:
            start_date = ""
            end_date = ""
            is_assigned = json.dumps(False)
                      
        product_obj = {
            'id': product.id,
            'origination_product_id': product.origination_product_id,
            'product_name': product.product_name,
            'product_code': product.product_code,
            'start_date': start_date,
            'end_date': end_date,
            'is_assigned': is_assigned,
            'índex': index
        } 
        partner_product_list.append(product_obj)
    
    context = {
        'partner': partner,
        'products': partner_product_list
    }
      
    productcounter = len(partner_product_list)

    if request.method == "POST":
        if productcounter > 0:
            PartnerProduct.objects.filter(partner_id=id).delete()
            for i in range(productcounter):
                product_id = request.POST.get('checkbox_' + str(i+1), None)
                print(product_id)
                start_date = request.POST.get('start_date_' + str(i+1), None)
                end_date = request.POST.get('end_date_' + str(i+1), None)
                
                if product_id is not None and start_date is not None and end_date is not None:
                    partnerProductObj = PartnerProduct(
                        partner_id=id,
                        product_id=product_id, 
                        start_date=start_date, 
                        end_date=end_date
                    )
                    partnerProductObj.save()            
            return redirect(add_products_to_partners, id=id)
                
        else:
            messages.error(request, 'Nuk ka produkte per partnerin!')
    else:
       messages.error(request, 'Nuk ka produkte per partnerin!')
    
    return render(request, 'accountmanagers/add_products_to_partner.html', context)


    





