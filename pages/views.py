from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import TemplateView, ListView
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.core.exceptions import ValidationError
from .models import Product
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import UserUpdateForm, ProfileUpdateForm

def ImageViewFactory(image_storage):
    class ImageView(View):
        template_name = 'images/index.html'

        def get(self, request):
            image_url = request.session.get('image_url', '')
            return render(request, self.template_name, {'image_url': image_url})

        def post(self, request):
            image_url = image_storage.store(request)
            request.session['image_url'] = image_url
            return redirect('image_index')
    return ImageView


class HomePageView(TemplateView):
    template_name = 'pages/home.html'

class AboutPageView(TemplateView):
    template_name = 'pages/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Sobre Nosotros - Plug&Ad",
            "subtitle": "Sobre Nosotros",
            "description": "Automatizamos campañas publicitarias con tecnología y diseño.",
            "author": "Desarrollado por: Jose Alejandro Jiménez Vásquez",
        })
        return context

class ContactPageView(TemplateView):
    template_name = 'pages/contact.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Contacto - Plug&Ad",
            "subtitle": "Contáctanos",
            "email": "jose@plugandad.com",
            "address": "Carrera 69 West, Medellín",
            "phone": "+57 3000000000",
        })
        return context

class ProductIndexView(View):
    template_name = 'products/index.html'
    
    def get(self, request):
        viewData = {}
        viewData["title"] = "Paquetes de Anuncios - Plug&Ad"
        viewData["subtitle"] = "Lista de Paquetes de Anuncios"
        viewData["products"] = Product.objects.all()
        return render(request, self.template_name, viewData)

class ProductShowView(View):
    template_name = 'products/show.html'

    def get(self, request, id):
        # Check if product id is valid
        try:
            product_id = int(id)
            if product_id < 1:
                raise ValueError("El ID del paquete de anuncios debe ser 1 o mayor")
            product = get_object_or_404(Product, pk=product_id)
        except (ValueError, IndexError):
            # If the product id is not valid, redirect to the home page
            return HttpResponseRedirect(reverse('home'))
        
        viewData = {}
        viewData["title"] = product.name + " - Plug&Ad"
        viewData["subtitle"] = product.name + " - Información del Paquete de Anuncios"
        viewData["product"] = product
        return render(request, self.template_name, viewData)

class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products' # This will allow you to loop through 'products' in your template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Paquetes de Anuncios - Plug&Ad'
        context['subtitle'] = 'Lista de Paquetes de Anuncios'
        return context

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'image']

    def clean_price(self):
        price = self.cleaned_data['price']
        if price is not None and price <= 0:
            raise ValidationError('El precio debe ser mayor que cero.')
        return price

class ProductCreateView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff
    template_name = 'products/create.html'
    
    def get(self, request):
        form = ProductForm()
        viewData = {}
        viewData["title"] = "Crear Paquete de Anuncios"
        viewData["form"] = form
        return render(request, self.template_name, viewData)
    
    def post(self, request):
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Paquete de anuncios creado exitosamente!')
            return redirect('index') # Redirige a la lista de productos
        else:
            viewData = {}
            viewData["title"] = "Crear Paquete de Anuncios"
            viewData["form"] = form
            return render(request, self.template_name, viewData)

class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff
    def post(self, request, id):
        product = get_object_or_404(Product, pk=id)
        product.delete()
        messages.success(request, '¡Paquete de anuncios eliminado exitosamente!')
        return redirect('index')

class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff
    template_name = 'products/update.html'

    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        form = ProductForm(instance=product)
        viewData = {}
        viewData["title"] = "Actualizar Paquete de Anuncios"
        viewData["form"] = form
        viewData["product"] = product
        return render(request, self.template_name, viewData)

    def post(self, request, id):
        product = get_object_or_404(Product, pk=id)
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Paquete de anuncios actualizado exitosamente!')
            return redirect('show', id=product.id)
        else:
            viewData = {}
            viewData["title"] = "Actualizar Paquete de Anuncios"
            viewData["form"] = form
            viewData["product"] = product
            return render(request, self.template_name, viewData)

class CartView(View):
    template_name = 'cart/index.html'

    def get(self, request):
        print("--- CartView GET ---")
        print(f"Contenido de la sesión en GET: {request.session.items()}")
        # Obtener productos del carrito de la sesión
        productos_en_carrito_ids = request.session.get('cart_product_data', {}).keys()
        print(f"IDs de productos en carrito (GET): {list(productos_en_carrito_ids)}")
        productos_en_carrito = Product.objects.filter(pk__in=productos_en_carrito_ids)
        print(f"Productos encontrados en DB (GET): {productos_en_carrito}")

        # Preparar datos para la vista
        datos_vista = {
            'title': 'Carrito - Plug&Ad',
            'subtitle': 'Tu Carrito de Compras',
            'products': Product.objects.all(), # Todos los productos disponibles
            'cart_products': productos_en_carrito
        }

        return render(request, self.template_name, datos_vista)

    def post(self, request, product_id):
        print("--- CartView POST ---")
        print(f"ID de producto recibido en POST: {product_id}")
        # Obtener productos del carrito de la sesión y añadir el nuevo producto
        datos_productos_carrito = request.session.get('cart_product_data', {})
        print(f"Datos de carrito antes de añadir (POST): {datos_productos_carrito}")
        datos_productos_carrito[int(product_id)] = int(product_id)
        request.session['cart_product_data'] = datos_productos_carrito
        request.session.modified = True # Asegurarse de que la sesión se guarde
        print(f"Datos de carrito después de añadir (POST): {datos_productos_carrito}")
        print(f"Contenido de la sesión después de añadir (POST): {request.session.items()}")

        return redirect('index')

class CartRemoveAllView(View):
    def post(self, request):
        # Eliminar todos los productos del carrito en la sesión
        if 'cart_product_data' in request.session:
            del request.session['cart_product_data']

        return redirect('cart_index')

class ImageViewNoDI(View):
    template_name = 'imagesnotdi/index.html'

    def get(self, request):
        image_url = request.session.get('image_url', '')
        return render(request, self.template_name, {'image_url': image_url})

    def post(self, request):
        image_storage = ImageLocalStorage()
        image_url = image_storage.store(request)
        request.session['image_url'] = image_url
        return redirect('image_index')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso!')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, '¡Tu perfil ha sido actualizado exitosamente!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'profile.html', context)