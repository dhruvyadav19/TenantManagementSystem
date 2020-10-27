from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import House, Image, Amenities
from django.contrib.auth.models import User
from .forms import HouseCreationForm, AmenitiesCreationForm
# Create your views here.

@login_required
def house_view(request):
    data = House.objects.filter(user = request.user)
    context = {
        'house': data
    }
    return render(request,'houses/view_houses.html',context)

@login_required
def add_house_view(request):
    if request.method == 'POST':
        house_form = HouseCreationForm(request.POST,request.FILES)
        amenities_form = AmenitiesCreationForm(request.POST)
        if house_form.is_valid() and amenities_form.is_valid():
            house_form = house_form.save(commit=False)
            house_form.user = User.objects.get(username = request.user)
            house_form.save()
            amenities_form = amenities_form.save(commit=False)
            amenities_form.house_id = house_form.pk
            amenities_form.save()
            for file in request.FILES.getlist('house_pics'):
                instance = Image(house = House.objects.get(pk = house_form.pk),image=file)
                instance.save()

            messages.success(request, f'Your house has been successfully added')
            return redirect('profile-view')
    else:
        house_form = HouseCreationForm()
        amenities_form = AmenitiesCreationForm()

    return render(request,'houses/add_house.html',{'house_form':house_form, 'amenities_form' : amenities_form })

@login_required
def house_info(request, single_slug):
    houses = [h.id for h in House.objects.all()]
    if int(single_slug) in houses:
        this_house = House.objects.get(id=int(single_slug))
        image_src = Image.objects.filter(house__id = single_slug)
        length = len(image_src)
        return render(request, "houses/house_page.html", {'house':this_house, 'image_src':image_src, 'length':length})
    else:
        return HttpResponse(f"404 error")