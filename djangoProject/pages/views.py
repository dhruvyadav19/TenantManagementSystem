from django.shortcuts import render
from houses.models import House,Image,Amenities
# Create your views here.
def home_view(request):
    return render(request,'pages/home.html')

def about_view(request):
    return render(request,'pages/about.html')

def search_view(request):
    query = request.GET['query']
    house_house_number = House.objects.filter(house_number__icontains=query)
    house_city = House.objects.filter(city__icontains=query)
    house_state = House.objects.filter(state__icontains=query)
    house_property_type = House.objects.filter(property_type__icontains=query)
    house_lankmark = House.objects.filter(landmark__icontains=query)
    allHouses = house_house_number | house_city | house_state | house_property_type | house_lankmark
    context = {
        'house' : allHouses
    }
    return render(request,'pages/search.html',context)



