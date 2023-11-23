from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from utils import IsAdminMixin
from .models import Product, Category
from . import tasks
from . import forms


# Create your views here.
class HomeView(View):
    def get(self, request, category_slug=None):
        products = Product.objects.filter(available=True)
        categories = Category.objects.all()
        if category_slug:
            category=Category.objects.get(slug=category_slug)
            products = products.filter(category=category)
        return render(request, 'home/home.html', {'products': products,'categories': categories})


class ProductsDetailView(View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        return render(request, 'home/details.html', {'product': product})


class BucketView(IsAdminMixin, View):
    def get(self, request):
        form = forms.UploadObjBucket()
        objects = tasks.all_bucket_object_task()
        return render(request, 'home/bucket.html', {'objects': objects, 'form': form})


class DeleteObjectBucket(IsAdminMixin, View):
    def get(self, request, key):
        tasks.delete_bucket_object_task.delay(key)
        messages.success(request, 'your image will be delete', 'info')
        return redirect('home:bucket')


class DownloadObjectBucket(IsAdminMixin, View):
    def get(self, request, key):
        tasks.download_bucket_object_task.delay(key)
        messages.success(request, 'your file will be downloaded', 'info')
        return redirect('home:bucket')


class UploadObjectBucket(View):
    def get(self, request):
        tasks.upload_bucket_object_task.delay(req=request.GET['upload_file'])
        messages.success(request, 'your file will be uploaded', 'info')
        return redirect('home:bucket')
