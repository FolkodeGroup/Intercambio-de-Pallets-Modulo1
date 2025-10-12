from django.shortcuts import render

def home(request):
    # Esta función simplemente le dice a Django que muestre la siguiente plantilla:
    return render(request, 'dashboard/home.html')