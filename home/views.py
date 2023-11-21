from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Product
from . import tasks
from . import forms


# Create your views here.
class HomeView(View):
    def get(self, request):
        products = Product.objects.filter(available=True)
        return render(request, 'home/home.html', {'products': products})


class ProductsDetailView(View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        return render(request, 'home/details.html', {'product': product})


class BucketView(View):
    def get(self, request):
        form = forms.UploadObjBucket()
        objects = tasks.all_bucket_object_task()
        return render(request, 'home/bucket.html', {'objects': objects,'form':form})


class DeleteObjectBucket(View):
    def get(self, request, key):
        tasks.delete_bucket_object_task.delay(key)
        messages.success(request, 'your image will be delete', 'info')
        return redirect('home:bucket')


class DownloadObjectBucket(View):
    def get(self, request, key):
        tasks.download_bucket_object_task.delay(key)
        messages.success(request, 'your file will be downloaded', 'info')
        return redirect('home:bucket')


class UploadObjectBucket(View):
    def get(self, request):
        tasks.upload_bucket_object_task.delay(req=request.GET['upload_file'])
        messages.success(request, 'your file will be uploaded', 'info')
        return redirect('home:bucket')
