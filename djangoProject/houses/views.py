from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import House, Image, Amenities, Contract
from django.contrib.auth.models import User
from .forms import HouseCreationForm, AmenitiesCreationForm, ContractForm
from django.forms.models import model_to_dict
from datetime import date

# Create your views here.
@login_required
def house_view(request):
    data = House.objects.filter(user=request.user)
    context = {
        'house': data
    }
    return render(request, 'houses/view_houses.html', context)

@login_required
def add_house_view(request):
    if request.method == 'POST':
        house_form = HouseCreationForm(request.POST, request.FILES)
        amenities_form = AmenitiesCreationForm(request.POST)
        if house_form.is_valid() and amenities_form.is_valid():
            house_form = house_form.save(commit=False)
            house_form.user = User.objects.get(username=request.user)
            house_form.save()
            amenities_form = amenities_form.save(commit=False)
            amenities_form.house_id = house_form.pk
            amenities_form.save()
            for file in request.FILES.getlist('house_pics'):
                instance = Image(house=House.objects.get(pk=house_form.pk), image=file)
                instance.save()

            messages.success(request, f'Your house has been successfully added')
            return redirect('profile-view')
    else:
        house_form = HouseCreationForm()
        amenities_form = AmenitiesCreationForm()

    return render(request, 'houses/add_house.html', {'house_form': house_form, 'amenities_form': amenities_form})

@login_required
def update_house(request, single_slug):
    this_house = House.objects.get(id=int(single_slug))
    amenity = Amenities.objects.get(house=this_house)
    if request.method == "POST":
        u_form = HouseCreationForm(request.POST, instance = this_house)
        p_form = AmenitiesCreationForm(request.POST ,instance = amenity)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your House Information has been updated!')
            return redirect('update-house', single_slug = this_house.id)
    else:
        u_form = HouseCreationForm(instance=this_house)
        p_form = AmenitiesCreationForm(instance=amenity)
    context = {
        'u_form' : u_form,
        'p_form' : p_form
    }
    return render(request,'houses/update_house.html',context)

def house_info(request, single_slug):
    houses = [h.id for h in House.objects.all()]
    if int(single_slug) in houses:
        this_house = House.objects.get(id=int(single_slug))
        image_src = Image.objects.filter(house__id=single_slug)
        amenities = Amenities.objects.get(house=this_house)

        temp = model_to_dict(amenities)
        lst = []
        for amenity in temp:
            if temp[amenity] == True and amenity != 'id':
                if amenity == 'lift': lst.append('Lift')
                if amenity == 'air_conditioner': lst.append('Air Conditioner')
                if amenity == 'swimming_pool': lst.append('Swimming Pool')
                if amenity == 'gas_pipeline': lst.append('Gas Pipeline')
                if amenity == 'visitor_parking': lst.append('Visitor Parking')
                if amenity == 'gym': lst.append('Gym')
                if amenity == 'security': lst.append('Security')
                if amenity == 'park': lst.append('Parking')
                if amenity == 'house_keeping': lst.append('House Keeping')
                if amenity == 'internet_services': lst.append('Internet Services')
                if amenity == 'shopping_center': lst.append('Shopping Center')
                if amenity == 'power_backup': lst.append('Power Backup')

        return render(request, "houses/house_page.html", {'house': this_house,
                                                          'image_src': image_src,
                                                          'amenities': lst})
    else:
        return HttpResponse(f"404 error")

@login_required
def delete_house(request, single_slug):
    house_instance = House.objects.get(id = int(single_slug))
    house_instance.delete()
    messages.success(request, f'Your Property has been deleted')
    return redirect('house-view')


def rent_house(request, single_slug):
    if request.method == 'POST':
        form = ContractForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['E_Signature'] == request.user.username:
                form = form.save(commit = False)
                form.user = User.objects.get(username=request.user)
                form.save()
                house = House.objects.get(id=int(single_slug))
                house.tenant_id = request.user.id
                house.occupied = True
                house.save()
                messages.success(request,f'Congratulations! The Contract Agreement was Successful')
                return redirect('profile-view')
            else:
                messages.warning(request,f'Incorrect Information, Please Try Again')
                return redirect('rent-house',single_slug = single_slug)
    else:
        form = ContractForm()

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

    return render(request,'houses/sign_contract.html',context)
