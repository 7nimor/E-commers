from django.urls import path,include
from . import views

app_name = 'home'

bucket_urls = [
    path('', views.BucketView.as_view(), name='bucket'),
    path('delete_obj/<str:key>',views.DeleteObjectBucket.as_view(), name='delete_obj_bucket'),
    path('download_obj/<str:key>',views.DownloadObjectBucket.as_view(), name='download_obj_bucket'),
    path('upload_obj/',views.UploadObjectBucket.as_view(), name='upload_obj_bucket'),

]

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('bucket/',include(bucket_urls)),
    path('<slug:slug>/', views.ProductsDetailView.as_view(), name='product_detail'),
]
