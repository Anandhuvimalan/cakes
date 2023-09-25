from django.db import models
from django.shortcuts import render
from shop.models import Product


def product_search(request):
    query = request.GET.get('q')
    results = []

    if query:
        results = Product.objects.filter(
            models.Q(name__icontains=query) | models.Q(description__icontains=query),
            available=True
        )
    return render(request, 'search.html', {'query': query, 'results': results})
