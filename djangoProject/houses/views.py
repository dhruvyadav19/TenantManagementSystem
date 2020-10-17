from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import House
from django.contrib.auth.models import User
from .forms import HouseCreationForm
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
        form = HouseCreationForm(request.POST)
        if form.is_valid():
            newForm = form.save(commit=False)
            newForm.user = User.objects.get(username = request.user)
            newForm.save()
            messages.success(request, f'Your house has been successfully added')
            return redirect('home-view')
    else:
        form = HouseCreationForm()

    return render(request,'houses/add_house.html',{'form':form})