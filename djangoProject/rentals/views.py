from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from houses.models import House, Image, Amenities
from django.contrib.auth.models import User
from datetime import date
from users.models import Profile
from houses.forms import ContractCreationForm
from .models import Payment, Complaint
from .forms import PayRentForm, ComplaintsForm
from users.forms import UserUpdateForm, ProfileUpdateForm

# Create your views here.
@login_required
def rent_house(request, single_slug):
    if request.method == 'POST':
        form = ContractCreationForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['E_Signature'] == request.user.username:
                e_sig = form.cleaned_data['E_Signature']
                this_house = House.objects.get(id = int(single_slug))
                this_house.tenant_id = request.user.id
                this_house.occupied = True
                this_house.E_Signature = e_sig
                this_house.save()
                today_date = date.today()
                payment_obj = Payment.objects.create(house=this_house,start_date=today_date,is_rent_due=True,total_amount_paid=0,tenant_id=request.user.id
                                       , due_money = this_house.rent, last_payment_date = None)
                payment_obj.save()
                messages.success(request,f'Congratulations! The Contracpythont Agreement was Successful')
                return redirect('pay-rent-view',single_slug=single_slug)
            else:
                messages.warning(request,f'Incorrect Information, Please Try Again')
                return redirect('rent-house',single_slug = single_slug)
    else:
        form = ContractCreationForm()

    today = date.today()
    house = House.objects.get(id = int(single_slug))
    landowner_name = User.objects.get(id = house.user_id).username
    tenant_name = request.user.username

    context = {
        'form' : form,
        'date' : today,
        'landowner_name' : landowner_name,
        'tenant_name' : tenant_name,
        'house' : house,
        'security' : house.rent//10
    }

    return render(request,'rentals/sign_contract.html',context)

@login_required
def view_rented_house(request):
    allHouses = House.objects.filter(tenant_id = request.user.id)
    allImages = []
    for each_house in allHouses:
        image = Image.objects.filter(house_id=each_house.id).first()
        allImages.append(image)
    allCombined = []
    for i in range(len(allImages)):
        allCombined.append((allHouses[i], allImages[i]))
    context = {
        'house': allCombined
    }
    return render(request,'rentals/view_rented_houses.html', context)

@login_required
def vacate_house(request,single_slug):
    house = House.objects.get(id = int(single_slug))
    house.tenant_id = None
    house.occupied = False
    house.E_Signature = None
    payment = Payment.objects.get(house = house)
    payment.delete()
    house.save()
    messages.success(request, f"House Vacated Successfully")
    return redirect('rented-house-view')


def calculate_dues(payment_instance, house_instance):
    if payment_instance.last_payment_date is not None:
        curr_date = date.today()
        last_date = payment_instance.last_payment_date
        curr_month = curr_date.strftime("%m")
        last_month = last_date.strftime("%m")
        if int(curr_month) == int(last_month) + 1:
            curr_day = curr_date.strftime("%d")
            last_day = last_date.strftime("%d")
            if curr_day >= last_day:
                payment_instance.due_money = house_instance.rent * (abs(int(curr_month) - int(last_month)))
                payment_instance.is_rent_due = True

        elif curr_month != last_month:
            payment_instance.due_money = house_instance.rent * (abs(int(curr_month) - int(last_month)))
            payment_instance.is_rent_due = True

    return payment_instance, house_instance


@login_required
def tenant_report(request):
    house_tenant_pair = []
    for single_entry in House.objects.all():
        if single_entry.user_id == request.user.id:
            tenant_obj = User.objects.filter(id=single_entry.tenant_id).first()
            if tenant_obj is not None:
                profile_obj = Profile.objects.filter(user_id=tenant_obj.id).first()
                payment_obj = Payment.objects.filter(house_id = single_entry.id).first()
                if tenant_obj is not None and profile_obj is not None and payment_obj is not None:
                    pair = single_entry,tenant_obj,profile_obj,payment_obj
                    payment_obj,single_entry = calculate_dues(payment_obj, single_entry)
                    payment_obj.save()
                    house_tenant_pair.append(pair)
                #print(pair)
    context = {
        'curr_date' : date.today(),
        'my_houses' : house_tenant_pair,
    }
    return render(request,'rentals/tenant_report.html',context)

@login_required
def pay_rent(request,single_slug):
    house_instance = House.objects.get(id = single_slug)
    payment_instance = Payment.objects.get(house = house_instance)
    if request.method == 'POST':
        form = PayRentForm(request.POST)
        if form.is_valid():
            amount_submitted = form.cleaned_data['rent']
            if amount_submitted != payment_instance.due_money:
                messages.warning(request,f'Enter correct amount')
                redirect('pay-rent-view',single_slug=single_slug)
            else:
                payment_instance.due_money = 0
                payment_instance.total_amount_paid  = payment_instance.total_amount_paid + amount_submitted
                payment_instance.last_payment_date = date.today()
                payment_instance.is_rent_due = False
                payment_instance.save()
                messages.success(request, f'Rent Paid Successfully !!')
                return redirect('house-info', single_slug=single_slug)
    else:
        form = PayRentForm()
        payment_instance, house_instance = calculate_dues(payment_instance,house_instance)
        payment_instance.save()

    context = {
        'form' : form,
        'house_rent' : payment_instance.due_money,
        'payment_details' : payment_instance
    }

    return render(request,'rentals/pay_rent.html',context)

@login_required
def contact_owner(request, single_slug):
    house = House.objects.get(id=single_slug)
    user = house.user
    profile = user.profile
    return render(request, 'rentals/contact_owner.html', {'user':user,
                                                          'profile':profile})

@login_required
def complaints(request, single_slug):
    my_house = House.objects.get(id=single_slug)
    if request.method == 'POST': 
        complaints_form = ComplaintsForm(request.POST)
        #print('error')
        if complaints_form.is_valid():
            complaints_form = complaints_form.save(commit=False)
            complaints_form.house_id = my_house.id
            complaints_form.save()
            messages.success(request, f'Your Complaint has been successfully added')
            return redirect('house-info', single_slug=single_slug)
    else:
        complaints_form = ComplaintsForm()

    return render(request, 'rentals/complaints.html', {'c_form': complaints_form})

@login_required
def view_complaints(request,single_slug):
    allComplaints = Complaint.objects.filter(house_id = single_slug)
    myHouse = House.objects.get(id = single_slug)
    tenant = User.objects.get(id = myHouse.tenant_id)
    context = {
        'complaints' : allComplaints,
        'house' : myHouse,
        'tenant' : tenant
    }

    return render(request, 'rentals/view_complaints.html',context)






