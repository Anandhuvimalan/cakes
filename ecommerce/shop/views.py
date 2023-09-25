from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from django.http import HttpResponse

def allProdCat(request, c_slug=None):
    c_page = None
    products = None

    if c_slug is not None: 
        c_page = get_object_or_404(Category, slug=c_slug)  
        products_list = Product.objects.filter(category=c_page, available=True)  
    else:
        products_list = Product.objects.filter(available=True)

    paginator = Paginator(products_list, 8)
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    return render(request, "category.html", {'category': c_page, 'products': products})

def proDetail(request, c_slug, product_slug):
    try:
        product = get_object_or_404(Product, category__slug=c_slug, slug=product_slug)
    except Exception as e:
        raise e
    return render(request, 'product.html', {'product': product})


