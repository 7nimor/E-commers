from django.urls import path
from . import views


app_name = 'home'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('bucket/',views.BucketView.as_view(), name='bucket'),
    path('<slug:slug>/',views.ProductsDetailView.as_view(),name='product_detail'),
]