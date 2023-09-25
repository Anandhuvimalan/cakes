from django.db import models
from django.urls import reverse
from PIL import Image

class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='category', blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image()

    def resize_image(self):
        if self.image:
            img = Image.open(self.image.path)
            output_size = (640, 200)
            img = img.resize(output_size)
            img.save(self.image.path)

    def get_url(self):
        return reverse('shop:products_by_category', args=[self.slug])

class Product(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product', blank=True)
    stock = models.IntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image()

    def resize_image(self):
        if self.image:
            img = Image.open(self.image.path)
            output_size = (640, 640)
            img = img.resize(output_size)
            img.save(self.image.path)

    def get_url(self):
        return reverse('shop:prodCatdetail', args=[self.category.slug, self.slug])
