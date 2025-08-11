from django.urls import path
from django.urls import path
from .views import (
    HomePageView, 
    AboutPageView, 
    ContactPageView,
    ProductIndexView, 
    ProductShowView, 
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    CartView,
    CartRemoveAllView,
    ImageViewFactory,
    ImageViewNoDI,
    register, # Added for registration
    profile # Added for user profile
)
from .utils import ImageLocalStorage

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('contact/', ContactPageView.as_view(), name='contact'),
    path('products/', ProductIndexView.as_view(), name='index'),
    path('products/create', ProductCreateView.as_view(), name='form'),
    path('products/<int:id>', ProductShowView.as_view(), name='show'),
    path('products/<int:id>/update', ProductUpdateView.as_view(), name='update'),
    path('products/<int:id>/delete', ProductDeleteView.as_view(), name='delete'),
    path('cart/', CartView.as_view(), name='cart_index'),
    path('cart/add/<str:product_id>', CartView.as_view(), name='cart_add'),
    path('cart/removeAll', CartRemoveAllView.as_view(), name='cart_removeAll'),
    path('image/', ImageViewFactory(ImageLocalStorage()).as_view(), name='image_index'),
    path('image/save', ImageViewFactory(ImageLocalStorage()).as_view(), name='image_save'),
    path('imagenotdi/', ImageViewNoDI.as_view(), name='imagenodi_index'),
    path('imagenotdi/save', ImageViewNoDI.as_view(), name='imagenodi_save'),
    path('register/', register, name='register'), # Added for registration
    path('profile/', profile, name='profile'), # Added for user profile
]