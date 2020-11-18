from django.shortcuts import render
from houses.models import House,Image,Amenities
# Create your views here.
def home_view(request):
    house_list = House.objects.filter(tenant_id = None)[:3]
    first_image = Image.objects.filter(house_id = house_list[0].id).first()
    second_image = Image.objects.filter(house_id = house_list[1].id).first()
    third_image = Image.objects.filter(house_id = house_list[2].id).first()
    image_list = [first_image,second_image,third_image]
    combined_list = []
    for i in range(3):
        combined_list.append((house_list[i],image_list[i]))
    context = {
        'house' : combined_list
    }
    return render(request,'pages/home.html',context)


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
    allImages = []
    for each_house in allHouses:
        image = Image.objects.filter(house_id = each_house.id).first()
        allImages.append(image)
    allCombined = []
    for i in range(len(allImages)):
        allCombined.append((allHouses[i],allImages[i]))
    context = {
        'house' : allCombined
    }
    return render(request,'pages/search.html',context)

'''def all_houses(request):
    allHouses = House.objects.filter(occupied = False)
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
    return render(request, 'pages/search.html', context)'''




