from django.shortcuts import render


def index(request):
    return render(request, 'index.html')

def product(request):
    return render(request, 'product-details.html')

def cart(request):
    return render(request, 'cart.html')