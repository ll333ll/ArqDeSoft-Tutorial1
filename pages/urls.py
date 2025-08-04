from django.urls import path
from .views import (
    HomePageView, 
    AboutPageView, 
    ContactPageView,
    ProductIndexView, 
    ProductShowView, 
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView
)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('contact/', ContactPageView.as_view(), name='contact'),
    path('products/', ProductIndexView.as_view(), name='index'),
    path('products/create', ProductCreateView.as_view(), name='form'),
    path('products/<int:id>', ProductShowView.as_view(), name='show'),
    path('products/<int:id>/update', ProductUpdateView.as_view(), name='update'),
    path('products/<int:id>/delete', ProductDeleteView.as_view(), name='delete'),
]